import markdown
import sys
import re
import os
import jinja2
from PIL import Image

def main():
    if len(sys.argv) != 3:
        print("Incorrent number of arguments.\n")
        print("Usage: python pagerender.py input.md template.html > output.html")
        print("Parse markdown and generate HTML.")
        sys.exit(1)

    with open(sys.argv[1]) as f_ip:
        content = markdown.markdown(f_ip.read(), extensions=['markdown.extensions.fenced_code', 'markdown.extensions.tables'], output_format='html5')
        for match in re.finditer(r'<img[^>]+src="([^"]+)"[^>]*>', content):
            img_tag = match.group(0)
            img_src = match.group(1)
            if 'youtube.com/embed' in img_src:
                new_img_tag = '<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%;"><iframe src="'+img_src+'" frameborder="0" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;" allowfullscreen></iframe></div>'
            else:
                filename, file_extension = os.path.splitext(img_src)
                crushed_img_src = filename + '-crushed' + file_extension
                img = Image.open(re.sub(r'[^/]+\.md','', sys.argv[1]) + img_src)
                img_w, img_h = img.size
                # Prevent layout shift in image by specifying width and height. See https://www.smashingmagazine.com/2020/03/setting-height-width-images-important-again/
                new_img_tag = img_tag.replace('src="'+img_src+'"', 'width="'+str(img_w)+'" height="'+str(img_h)+'" src="'+crushed_img_src+'"')
                new_img_tag = '<a href="'+img_src+'">'+new_img_tag+'</a>'
            content = content.replace(img_tag, new_img_tag)
        title = re.search(r'<h1>([^<]+)</h1>', content)
        if title:
            title = title.group(1)
        else:
            title = 'Sagar Gubbi'
        rendered = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates')).get_template(sys.argv[2]).render(content=content, title=title)
        print(rendered)

if __name__ == '__main__':
    main()
