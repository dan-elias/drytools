#!/usr/bin/env bash
set -e

# build docs
cd docs
make clean
make html
cd ..

# Prepare requirements.txt for ReadThedocs
requirements_rtd=requirements_rtd.txt
cat requirements_doc.txt > $requirements_rtd
cat requirements_package.txt >> $requirements_rtd

# Open docs in browser
./open_docs.sh
