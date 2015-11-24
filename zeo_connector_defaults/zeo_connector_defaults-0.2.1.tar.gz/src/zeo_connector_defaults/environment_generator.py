#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import shutil
import random
import os.path
import tempfile
import threading
import subprocess
from string import Template


# Variables ===================================================================
SERV = None  #: Here is stored the running process.
TMP_PATH = None  #: Here will be stored the path to the temporary directory.
ZEO_SERVER = "localhost"  #: Hostname for the ZEO server
ZEO_PORT = random.randint(20000, 65000)  #: Port for the ZEO server


# Functions & classes =========================================================
def data_context_name(fn):
    """
    Return the `fn` in absolute path in `template_data` directory.
    """
    return os.path.join(os.path.dirname(__file__), "template_data", fn)


def data_context(fn, mode="r"):
    """
    Return content fo the `fn` from the `template_data` directory.
    """
    with open(data_context_name(fn), mode) as f:
        return f.read()


def tmp_context_name(fn=None):
    """
    Return the `fn` in absolute path in temporary directory.
    """
    if not fn:
        return TMP_PATH

    return os.path.join(TMP_PATH, fn)


def tmp_context(fn, mode="r"):
    """
    Return content fo the `fn` from the temporary directory.
    """
    with open(tmp_context_name(fn), mode) as f:
        return f.read()


# Environment generators ======================================================
def generate_environment():
    """
    Generate the environment in ``/tmp`` and run the ZEO server process in
    another thread.
    """
    global TMP_PATH
    TMP_PATH = tempfile.mkdtemp()

    # write ZEO server config to  temp directory
    zeo_conf_path = os.path.join(TMP_PATH, "zeo.conf")
    with open(zeo_conf_path, "w") as f:
        f.write(
            Template(data_context("zeo.conf")).substitute(
                path=TMP_PATH,
                server=ZEO_SERVER,
            )
        )

    # write client config to temp directory
    client_config_path = os.path.join(TMP_PATH, "zeo_client.conf")
    with open(client_config_path, "w") as f:
        f.write(
            Template(data_context("zeo_client.conf")).substitute(
                path=TMP_PATH,
                server=ZEO_SERVER,
                port=ZEO_PORT,
            )
        )

    # run the ZEO server
    def run_zeo():
        global SERV
        SERV = subprocess.Popen(["runzeo", "-C", zeo_conf_path])

    serv = threading.Thread(target=run_zeo)
    serv.setDaemon(True)
    serv.start()


def cleanup_environment():
    """
    Shutdown the ZEO server process running in another thread and cleanup the
    temporary directory.
    """
    SERV.terminate()
    shutil.rmtree(TMP_PATH)
    if os.path.exists(TMP_PATH):
        os.rmdir(TMP_PATH)

    global TMP_PATH
    TMP_PATH = None
