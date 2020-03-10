#!/bin/bash

pip install -U pywin32
pip install -U pyinstaller
pip install -Ur requirements.txt

pyinstaller --clean --name diffmanifests --upx-dir /path/to/upx -F diff.py
