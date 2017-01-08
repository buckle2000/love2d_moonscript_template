# Directory
PATH_DYNAMIC = "dynamic/"
PATH_STATIC  = "static/"
PATH_OUT     = "_out/"

# External exes
EXE_MOONC = "moonc"
EXE_ASPRITE = "TODO"
EXE_TILED = "TODO"

import os
# import sys
import shutil
import subprocess

def copytree(src, dst, symlinks=False, ignore=None, copy_function=shutil.copy2):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()
    os.makedirs(dst, exist_ok=True)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if os.path.islink(srcname):
                linkto = os.readlink(srcname)
                if symlinks:
                    os.symlink(linkto, dstname)
                    shutil.copystat(srcname, dstname, follow_symlinks=not symlinks)
                else:
                    if os.path.isdir(srcname):
                        copytree(srcname, dstname, symlinks, ignore,
                                 copy_function)
                    else:
                        copy_function(srcname, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore, copy_function)
            else:
                copy_function(srcname, dstname)
        except shutil.Error as err:
            errors.extend(err.args[0])
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
    try:
        shutil.copystat(src, dst)
    except OSError as why:
        if getattr(why, 'winerror', None) is None:
            errors.append((src, dst, str(why)))
    if errors:
        raise shutil.Error(errors)
    return dst

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

# TODO add asset pipelines

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

copytree(PATH_DYNAMIC, PATH_OUT, ignore=ignore_func, copy_function=copy_func)

copytree(PATH_STATIC, PATH_OUT)
