#!/bin/bash

python pagerender.py index.md templates/base.html > index.html

python pagerender.py proj/flathn/flathn.md templates/base.html > proj/flathn/index.html
python pagerender.py proj/ntsc/ntsc.md templates/base.html > proj/ntsc/index.html
