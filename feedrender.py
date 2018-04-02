import markdown
import sys
import re
import os
import jinja2
import datetime
import time

base_url = "http://www.sagargv.com"
template = "atom.xml"
blogs_dir = "blog/"
output_feed = "blog/atom.xml"

def main():
    items = []

    for blog in os.walk(blogs_dir).next()[1]:
        blog_md_path = blogs_dir + blog + "/index.md"
        with open(blog_md_path) as f_blog_md:
            content = markdown.markdown(f_blog_md.read(), extensions=['markdown.extensions.fenced_code'], output_format='html5')
            title = re.search(r'<h1>([^<]+)</h1>', content)
            title = title.group(1)
            pub_date = re.search(r'<p><em>([^<]+, 20[0-9][0-9])</em></p>', content)
            pub_date = datetime.datetime.strptime(pub_date.group(1), '%b %d, %Y')
            desc = re.search(r'20[0-9][0-9]</em></p>([\s\S]+)', content) # look for content after the date
            desc = desc.group(1)
            item = {
                'title': title,
                'pub_date': pub_date.strftime("%a, %d %b %Y %H:%M:%S") + " +0000",
                'pub_time': pub_date,
                'desc': '<![CDATA['+desc+']]>',
                'link': base_url + "/blog/" + blog + "/"
            }
            items.append(item)

    items = sorted(items, key=lambda item: item['pub_time'], reverse=True)
    items = items[:10]
    rendered = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates')).get_template(template).render({
        'blog_url': base_url + "/blog/",
        'feed_url': base_url + "/blog/atom.xml",
        'last_build_date': datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " +0000",
        'items': items,
    })
    with open(output_feed, 'w') as f:
        f.write(rendered)

if __name__ == '__main__':
    main()
