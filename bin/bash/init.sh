#!/usr/bin/env bash

set -e

virtualenv -ppython3 venv
source venv/bin/activate
pip install -r requirements.txt