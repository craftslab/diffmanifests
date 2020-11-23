#!/bin/bash

pip3 install -U pywin32
pip3 install -U pyinstaller
pip3 install -Ur requirements.txt

pyinstaller --clean --name diffmanifests --upx-dir /usr/bin/upx -F diff.py
