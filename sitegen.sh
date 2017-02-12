#!/bin/bash

python pagerender.py index.md home.html > index.html

python pagerender.py proj/cookoo2/cookoo.md proj.html > proj/cookoo2/index.html
python pagerender.py proj/flathn/flathn.md proj.html > proj/flathn/index.html
python pagerender.py proj/ntsc/ntsc.md proj.html > proj/ntsc/index.html
