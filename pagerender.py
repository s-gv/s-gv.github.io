import markdown
import sys

template = '''
'''

def main():
    if len(sys.argv) != 3:
        print "Incorrent number of arguments.\n"
        print "Usage: python pagerender.py input.md template.html > output.html"
        print "Parse markdown and generate HTML."
        exit(1)

    with open(sys.argv[2]) as f_template:
        with open(sys.argv[1]) as f_ip:
            template = f_template.read()
            print template % {'content': markdown.markdown(f_ip.read(), output_format='html5')}

if __name__ == '__main__':
    main()
