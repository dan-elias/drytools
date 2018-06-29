#!/usr/bin/env bash
set -e

for dir in build dist
do
  rm -r -f $dir
done

python setup.py sdist bdist_wheel
twine upload -r pypi dist/*
