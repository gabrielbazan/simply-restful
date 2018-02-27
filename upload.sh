#!/usr/bin/env bash

rm -fr build/ dist/ *.egg-info/

python setup.py bdist_wheel --universal
twine upload dist/*
