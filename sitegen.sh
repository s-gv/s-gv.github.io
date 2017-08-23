#!/bin/bash

python pagerender.py index.md home.html > index.html
python pagerender.py blog/index.md blogindex.html > blog/index.html

find proj -mindepth 1 -maxdepth 1 -type d -exec sh -c "python pagerender.py {}/index.md proj.html > {}/index.html" \;

find blog -mindepth 1 -maxdepth 1 -type d -exec sh -c "python pagerender.py {}/index.md blog.html > {}/index.html" \;
