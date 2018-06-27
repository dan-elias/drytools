#!/usr/bin/env bash
set -e

rm tests/test_example.py
rm drytools/example.py
rm docs/source/example.rst

echo "Manual step:  edit docs/source/index.rst and remove 'example' from the table of contents"

rm $0
