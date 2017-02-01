import os
import shutil
import build

## Change these
EXE_LOVE_DIR = r"C:\Program Files\LOVE" + "\\" # directory containing LÖVE executable
EXE_LOVE_EXE = "love.exe" # the name of LÖVE executable
EXE_OUT_EXE  = "game.exe" # the name of result executable

PATH_OUT_FUSED    = "__pycache__/fused/"
PATH_OUT_EXTERNAL = "__pycache__/external/"
PATH_OUT_LOVEZIP  = "__pycache__/lovezip"
PATH_OUT_BUILD    = "__pycache__/win32"

build.build(PATH_OUT_FUSED, PATH_OUT_EXTERNAL)

file_name_lovezip = shutil.make_archive(PATH_OUT_LOVEZIP, "zip", PATH_OUT_FUSED)

build.copytree(EXE_LOVE_DIR, PATH_OUT_EXTERNAL, ignore=lambda _,x:[i for i in x if i[-4:]!=".dll"])

with open(file_name_lovezip, "rb") as lovezip:
    with open(EXE_LOVE_DIR+EXE_LOVE_EXE, "rb") as loveexe:
        with open(PATH_OUT_EXTERNAL+EXE_OUT_EXE, "wb") as gameexe:
            gameexe.write(loveexe.read())
            gameexe.write(lovezip.read())

shutil.make_archive(PATH_OUT_BUILD, "zip", PATH_OUT_EXTERNAL)
