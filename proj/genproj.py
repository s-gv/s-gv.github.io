import sys
import datetime
import re

mainHTML = '''
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>Flat HN</title>

        <!-- Bootstrap -->
        <link href="/static/css/bootstrap.min.css" rel="stylesheet">
        <link href="/static/css/lightbox.css" rel="stylesheet">

        <style media="screen">
            body {
              padding-top: 20px;
              padding-bottom: 20px;
            }
            .navbar {
              margin-bottom: 20px;
            }
            #maintitle {
                font-size: 40px;
            }
            .jumbotron {
                padding-left: 10px;
                padding-right: 10px;
            }
            /* Customize container */
            @media (min-width: 768px) {
                .container {
                    max-width: 730px;
                }
            }
            .footer {
                margin-top: 25px;
            }
            .img-full {
                width: 100%%;
            }
        </style>

        <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
        <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
        <![endif]-->
    </head>
    <body>
        <!-- Static navbar -->
        <div class="container">
            <nav class="navbar navbar-default">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                </div>
                <div id="navbar" class="navbar-collapse collapse">
                    <ul class="nav navbar-nav navbar-right">
                        <li><a href="/">Home</a></li>
                        <li><a href="http://blog.sagargv.com">Blog</a></li>
                        <li><a href="http://github.com/s-gv">Github</a></li>
                        <li><a href="https://twitter.com/gv_sagar">Twitter</a></li>
                    </ul>
                </div><!--/.nav-collapse -->
            </nav>
        </div>

        <div class="container">
            %(content)s
        </div> <!-- /container -->

        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <footer class="footer">
                        <p class="text-muted">Last updated on %(date)s.</p>
                    </footer>
                </div>
            </div>
        </div>

        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
        <script src="/static/js/jquery.min.js"></script>
        <!-- Include all compiled plugins (below), or include individual files as needed -->
        <script src="/static/js/bootstrap.min.js"></script>
        <script src="/static/js/lightbox.min.js"></script>
        <script>
            (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
            })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

            ga('create', 'UA-69020583-1', 'auto');
            ga('send', 'pageview');
        </script>
    </body>
</html>

'''

mainHeadingHTML = '''
<div class="row">
    <div class="col-md-12">
        <div class="jumbotron">
            <h1 id="maintitle">%(heading)s</h1>
            <br />
            %(content)s
        </div>
    </div>
</div>
'''

subHeadingHTML = '''
<div class="row">
    <div class="col-md-12">
        <div class="page-header">
            <h2>%(heading)s</h2>
        </div>
        %(content)s
    </div>
</div>
'''

paragraphHTML = '''
<p class="lead">
    %(content)s
</p>
'''

imgHTML = '''
<p>
    <a href="%(imgURL)s" data-lightbox="proj-img"><img class="img-full img-responsive" src="%(crushedImgURL)s" alt="%(altText)s"></a>
</p>
'''

githubButtonHTML = '''
<p>
    <a class="btn btn-lg btn-primary" href="%(githubURL)s" role="button">View in GitHub</a>
</p>
'''

linkHTML = '''<a href="%(url)s">%(text)s</a>'''

def makeHTML(parseTree):
    contents = [makeHTML(childTree) for childTree in parseTree['children']]
    if parseTree['type'] == 'main':
        return mainHTML % {'date': parseTree['date'], 'content': '\n'.join(contents)}
    elif parseTree['type'] == 'h1':
        return mainHeadingHTML % {'heading': parseTree['heading'], 'content': '\n'.join(contents)}
    elif parseTree['type'] == 'h2':
        return subHeadingHTML % {'heading': parseTree['heading'], 'content': '\n'.join(contents)}
    elif parseTree['type'] == 'p':
        return paragraphHTML % {'content': ''.join(contents)}
    elif parseTree['type'] == 'plain':
        return parseTree['text']
    elif parseTree['type'] == 'link':
        return linkHTML % {'url': parseTree['url'], 'text': parseTree['text']}
    elif parseTree['type'] == 'github':
        return githubButtonHTML % {'githubURL': parseTree['url']}
    elif parseTree['type'] == 'img':
        return imgHTML % {'imgURL': parseTree['imgURL'], 'crushedImgURL': parseTree['crushedImgURL'], 'altText': parseTree['txt']}
    assert False, "Unrecognized node type '%s' in parse tree" % parseTree['type']

def parseMarkdown(mkdown):
    tree = {'type': 'main', 'date': datetime.datetime.now().strftime('%B %-d, %Y'), 'children': []}
    lastChildren = None
    lines = mkdown.split('\n')
    for line in lines:
        l = line.strip()
        if len(l) > 0:
            words = l.split()
            first_word = words[0]
            if len(set(first_word)) == 1 and '#' in first_word:
                tree['children'].append({'type': 'h' + str(len(first_word)), 'heading': ' '.join(words[1:]), 'children': []})
                lastChildren = tree['children'][-1]['children']
            elif re.match(r'^!\[github\]\((.+)\)', l):
                m = re.match(r'^!\[github\]\((.+)\)', l)
                lastChildren.append({'type': 'github', 'url': m.group(1), 'children': []})
            elif re.match(r'^!\[(.+)\]\((.+)\)', l):
                m = re.match(r'^!\[(.+)\]\((.+)\)', l)
                imgURL = m.group(2)
                dotPosition = imgURL.rfind('.')
                crushedURL = imgURL[:dotPosition] + '_crushed' + imgURL[dotPosition:]
                lastChildren.append({'type': 'img', 'txt': m.group(1), 'imgURL': imgURL, 'crushedImgURL': crushedURL, 'children': []})
            else:
                lastChildren.append({'type': 'p', 'children': []})
                currentChildren = lastChildren[-1]['children']

                linkRegEx = r'\[([^\[\]]+)\]\(([^\s]+)\)'
                links = re.findall(linkRegEx, l)
                nonLinks = re.sub(linkRegEx, chr(27), l).split(chr(27))

                for idx, (linkText, url) in enumerate(links):
                    currentChildren.append({'type': 'plain', 'text': nonLinks[idx], 'children': []})
                    currentChildren.append({'type': 'link', 'text': linkText, 'url': url, 'children': []})

                currentChildren.append({'type': 'plain', 'text': nonLinks[-1], 'children': []})


    return tree

def main():
    if len(sys.argv) != 2:
        print "Incorrent number of arguments.\n"
        print "Usage: python genproj.py projname.md > projname.html"
        print "Parse markdown project description and generate HTML."
        exit(1)

    mkdown = '\n'.join([line.strip() for line in open(sys.argv[1])])
    parseTree = parseMarkdown(mkdown)
    print makeHTML(parseTree)


if __name__ == '__main__':
    main()
