@echo off
python build.py
pushd _out
love .
popd