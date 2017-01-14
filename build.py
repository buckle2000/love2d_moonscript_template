# Directory
PATH_DYNAMIC = "dynamic/"
PATH_STATIC = "static/"
PATH_EXTERNAL = "external/"
PATH_OUT = "_out/src"

# External executables
# Make sure you can run these in shell;
# otherwise, put full path here (e.g. "C:/path/to/moonc.exe" or
# "/path/to/moonc")
EXE_MOONC = "moonc"
EXE_ASEPRITE = "aseprite"
EXE_TILED = "tiled"

import os
import shutil
import subprocess
import IPython


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
                    shutil.copystat(srcname, dstname,
                                    follow_symlinks=not symlinks)
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


def make_archive(base_name, format, root_dir=None, base_dir=None, verbose=0, dry_run=0, owner=None, group=None, logger=None):
    save_cwd = os.getcwd()
    if root_dir is not None:
        if logger is not None:
            logger.debug("changing into '%s'", root_dir)
        base_name = os.path.abspath(base_name)
        if not dry_run:
            os.chdir(root_dir)

    if base_dir is None:
        base_dir = os.curdir

    kwargs = {'dry_run': dry_run, 'logger': logger}

    try:
        format_info = shutil._ARCHIVE_FORMATS[format]
    except KeyError:
        raise ValueError("unknown archive format '%s'" % format)

    func = format_info[0]
    for arg, val in format_info[1]:
        kwargs[arg] = val

    if format != 'zip':
        kwargs['owner'] = owner
        kwargs['group'] = group

    try:
        filename = func(base_name, base_dir, **kwargs)
    finally:
        if root_dir is not None:
            if logger is not None:
                logger.debug("changing back to '%s'", save_cwd)
            os.chdir(save_cwd)

    return filename

# Helpers

get_file = lambda file_name: os.path.splitext(file_name)[0]
get_ext = lambda file_name: os.path.splitext(file_name)[1]
get_fname = lambda path: os.path.split(path)[1]  # get file name from path
get_extp = lambda path: get_ext(get_fname(path))  # get ext from path
get_dir = lambda path: os.path.split(path)[0]  # get dir from path


def change_ext(file_name, new_ext):
    before_ext, ext = os.path.splitext(file_name)
    return before_ext + new_ext

# Acceptable File Ext and Copy Function


def process_moon(src, dst, *, follow_symlinks=True):
    subprocess.call([EXE_MOONC, "-o", change_ext(dst, ".lua"), src], timeout=1)

def process_aseprite(src, dst, *, follow_symlinks=True):
    dstdir, dstfname = os.path.split(dst)
    root = get_file(dstfname)
    sheet_data = dstdir + os.sep + root + ".json"
    # IPython.embed()
    dst = dstdir + os.sep + root + ".png"
    # image which filename ends with '#' is an animation atlas
    if root.endswith('#'):
        subprocess.call((EXE_ASEPRITE, '-b', src, "--sheet", dst, "--data", sheet_data,
            "--list-tags", "--format", "json-array"))
    else:
        subprocess.call((EXE_ASEPRITE, '-b', src, "--save-as", dst))

def process_tiled(src, dst, *, follow_symlinks=True):
    dstdir, dstfile = os.path.split(dst)
    root = get_file(dstfile)
    # IPython.embed()
    dst = dstdir + os.sep + root + ".lua"
    subprocess.call((EXE_TILED, "--export-map", src, dst))

EXT_SRC = {
    "":          None,  # should be directory
    ".lua":      shutil.copy2,
    ".moon":     process_moon,
    ".ase":      process_aseprite,
    ".aseprite": process_aseprite,
    ".tmx":      process_tiled,
}

# Copying/Compiling source code

# TODO add asset pipelines


def ignore_func_helper(file_name):
    return get_ext(file_name) not in EXT_SRC


def ignore_func(curdir, file_names):
    print("listing", file_names)
    names = filter(ignore_func_helper, file_names)
    return names


def copy_func(src, dst, *, follow_symlinks=True):
    print("Processing", src)
    ext = get_extp(src)
    EXT_SRC[ext](src, dst, follow_symlinks=follow_symlinks)


def build(path_out_fused=PATH_OUT, path_out_extern=PATH_OUT):
    if os.path.exists(path_out_fused):
        shutil.rmtree(path_out_fused)
    if os.path.exists(path_out_extern):
        shutil.rmtree(path_out_extern)

    copytree(PATH_DYNAMIC, path_out_fused,
             ignore=ignore_func, copy_function=copy_func)
    copytree(PATH_STATIC, path_out_fused)
    copytree(PATH_EXTERNAL, path_out_extern)

if __name__ == '__main__':
    build()
