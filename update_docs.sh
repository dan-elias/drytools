#!/usr/bin/env bash
set -e

# build docs
cd docs
make clean
make html
cd ..

# Open docs in browser
./open_docs.sh
