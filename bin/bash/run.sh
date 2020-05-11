#!/usr/bin/env bash

set -e

FLASK_APP=app/main.py FLASK_ENV=development python -m flask run