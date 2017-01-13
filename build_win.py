import os
import shutil
import build

## Change these
EXE_LOVE_DIR = r"C:\Program Files\LOVE" + "\\" # directory containing LÖVE executable
EXE_LOVE_EXE = "love.exe" # the name of LÖVE executable
EXE_OUT_EXE  = "game.exe" # the name of result executable

PATH_OUT_FUSED    = "_out/fused/"
PATH_OUT_EXTERNAL = "_out/external/"
PATH_OUT_LOVEZIP  = "_out/lovezip"
PATH_OUT_BUILD    = "_out/win32"

build.build(PATH_OUT_FUSED, PATH_OUT_EXTERNAL)

file_name_lovezip = shutil.make_archive(PATH_OUT_LOVEZIP, "zip", PATH_OUT_FUSED)

with open(file_name_lovezip, "rb") as lovezip:
    with open(EXE_LOVE_DIR+EXE_LOVE_EXE, "rb") as loveexe:
        with open(PATH_OUT_EXTERNAL+EXE_OUT_EXE, "wb") as gameexe:
            gameexe.write(loveexe.read())
            gameexe.write(lovezip.read())

build.copytree(EXE_LOVE_DIR, PATH_OUT_EXTERNAL, ignore=lambda _,x:[i for i in x if i[-4:]!=".dll"])

shutil.make_archive(PATH_OUT_BUILD, "zip", PATH_OUT_EXTERNAL)
