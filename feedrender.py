import markdown
import sys
import re
import os
import jinja2

def main():
    if len(sys.argv) != 2:
        print "Incorrent number of arguments.\n"
        print "Usage: python feedrender.py template.xml > atom.xml"
        print "Generate RSS feed."
        exit(1)

    template_file_name = sys.argv[1]

    items = []

    rendered = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates')).get_template(template_file_name).render({
        'base_url': "http://www.sagargv.com",
        'last_build_date': 'today',
        'items': items,
    })
    print rendered

if __name__ == '__main__':
    main()
