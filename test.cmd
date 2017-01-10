@echo off
python build.py
pushd _out\src
love .
popd