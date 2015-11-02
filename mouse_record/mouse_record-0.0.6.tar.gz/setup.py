from __future__ import print_function

__author__ = "Bailey Hwa <hwab@janelia.hhmi.org>"
__date__ = "$July 30, 2015 20:20:18 EDT$"

from glob import glob
import os
import shutil
import sys

from setuptools import setup, find_packages

import versioneer


build_requires = []
install_requires = []
tests_require = ["nose"]
sphinx_build_pdf = False
if len(sys.argv) == 1:
    pass
elif sys.argv[1] == "build_sphinx":
    import sphinx.apidoc

    sphinx.apidoc.main([
        sphinx.apidoc.__file__,
        "-f", "-T", "-e", "-M",
        "-o", "docs",
        ".", "setup.py", "tests", "versioneer.py"
    ])

    build_prefix_arg_index = None
    for each_build_arg in ["-b", "--builder"]:
        try:
            build_arg_index = sys.argv.index(each_build_arg)
        except ValueError:
            continue

        if sys.argv[build_arg_index + 1] == "pdf":
            sphinx_build_pdf = True
            sys.argv[build_arg_index + 1] = "latex"
elif sys.argv[1] == "clean":
    saved_rst_files = ["docs/index.rst", "docs/readme.rst", "docs/todo.rst"]

    tmp_rst_files = glob("docs/*.rst")

    print("removing 'docs/*.rst'")
    for each_saved_rst_file in saved_rst_files:
        print("skipping '" + each_saved_rst_file + "'")
        tmp_rst_files.remove(each_saved_rst_file)

    for each_tmp_rst_file in tmp_rst_files:
        os.remove(each_tmp_rst_file)

    if os.path.exists("build/sphinx/doctrees"):
        print("removing 'build/sphinx/doctrees'")
        shutil.rmtree("build/sphinx/doctrees")
    else:
        print("'build/sphinx/doctrees' does not exist -- can't clean it")

    if os.path.exists(".eggs"):
        print("removing '.eggs'")
        shutil.rmtree(".eggs")
    else:
        print("'.eggs' does not exist -- can't clean it")

    if (len(sys.argv) > 2) and (sys.argv[2] in ["-a", "--all"]):
        if os.path.exists("build/sphinx"):
            print("removing 'build/sphinx'")
            shutil.rmtree("build/sphinx")
        else:
            print("'build/sphinx' does not exist -- can't clean it")
elif sys.argv[1] == "develop":
    if (len(sys.argv) > 2) and (sys.argv[2] in ["-u", "--uninstall"]):
        if os.path.exists("mouse_record.egg-info"):
            print("removing 'mouse_record.egg-info'")
            shutil.rmtree("mouse_record.egg-info")
        else:
            print("'mouse_record.egg-info' does not exist -- can't clean it")

setup(
    name="mouse_record",
    version=versioneer.get_version(),
    description="An Event Triggered Recorder",
    url="https://github.com/DudLab/mouse_record",
    license="GPLv3",
    author="Bailey Hwa",
    author_email="hwab@janelia.hhmi.org",
    scripts=glob("bin/*"),
    py_modules=["versioneer"],
    packages=find_packages(exclude=["tests*"]),
    cmdclass=versioneer.get_cmdclass(),
    install_requires=["picamera >=1.0", "RPi.GPIO >=0.5.11"],
    tests_require=["nose", "mock"],
    test_suite="nose.collector",
    zip_safe=True
)

if sphinx_build_pdf:
    make_cmd = os.environ.get("MAKE", "make")
    cwd = os.getcwd()
    os.chdir("build/sphinx/latex")
    os.execlpe(make_cmd, "all", os.environ)
    os.chdir(cwd)
