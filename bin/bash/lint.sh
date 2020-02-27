#!/usr/bin/env bash

set -e

git diff --cached --name-status | awk '$1 != "D" { print $2 }' | grep .py | \
  xargs pylint --ignore-patterns=test_