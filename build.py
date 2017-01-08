# Directory
PATH_OUT = "_out"
PATH_SRC = "source"
PATH_AST = "asset"

# External exes
EXE_MOONC = "moonc"
EXE_ASPRITE = "TODO"
EXE_TILED = "TODO"

import os
# import sys
import shutil
import subprocess

# Helpers

get_ext = lambda file_name: os.path.splitext(
    file_name)[1]  # get ext from file name
get_fname = lambda path: os.path.split(path)[1]  # get file name from path
get_extp = lambda path: get_ext(get_fname(path))  # get ext from path
get_dir = lambda path: os.path.split(path)[0]  # get dir from path


def change_ext(file_name, new_ext):
    before_ext, ext = os.path.splitext(file_name)
    return before_ext + new_ext

# Acceptable File Ext and Copy Function


def copy_moon(src, dst, *, follow_symlinks=True):
    subprocess.call([EXE_MOONC, "-o", change_ext(dst, ".lua"), src], timeout=1)

EXT_SRC = {
    "": None,  # should be directory
    ".lua": shutil.copy2,
    ".moon": copy_moon,
}

# Copying/Compiling source code


def ignore_func_helper(file_name):
    return get_ext(file_name) not in EXT_SRC


def ignore_func(src, file_names):
    print("listing", file_names)
    names = filter(ignore_func_helper, file_names)
    return names


def copy_func(src, dst, *, follow_symlinks=True):
    print("Copying", src, dst)
    ext = get_extp(src)
    EXT_SRC[ext](src, dst, follow_symlinks=follow_symlinks)

if os.path.exists(PATH_OUT):
    shutil.rmtree(PATH_OUT)

shutil.copytree(PATH_SRC, PATH_OUT, symlinks=True,
                ignore=ignore_func, copy_function=copy_func)
