#!/bin/bash

chmod 644 .dockerignore .gitignore .travis.yml
chmod 644 LICENSE MANIFEST.in README.md requirements.txt setup.cfg tox.ini
chmod 644 setup.py diff.py

find diffmanifests tests -name "*.json" -exec chmod 644 {} \;
find diffmanifests tests -name "*.py" -exec chmod 644 {} \;
find . -name "*.pyc" -exec rm -rf {} \;
find . -name "*.sh" -exec chmod 755 {} \;
find . -name "__pycache__" -exec rm -rf {} \;
