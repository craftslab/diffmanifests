#!/bin/bash

pip install --break-system-packages coverage
python -m coverage run --source=diffmanifests,tests -m pytest -v --capture=no
