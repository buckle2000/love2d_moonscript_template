@echo off
python build.py
pushd __pycache__\src
love .
popd