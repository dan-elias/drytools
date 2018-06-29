#!/usr/bin/env bash
set -e

# build docs
cd docs
make clean
make html
cd ..

# Prepare requirements.txt for ReadThedocs
cat requirements_doc.txt > requirements.txt
cat requirements_package.txt >> requirements.txt

# Open docs in browser
./open_docs.sh
