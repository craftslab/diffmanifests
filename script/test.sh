#!/bin/bash

coverage run --source=diffmanifests,tests -m pytest -v --capture=no
