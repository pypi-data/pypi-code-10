#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
from distutils.core import setup

pypi_long_description = """

===========
qpidtoollibs
===========

qpidtoollibs provides a useful BrokerAgent object for managing a Qpid broker
using Qpid Management Framework (QMF).

This library depends on the qpid.messaging python client to send AMQP messaging
containing QMF commands to the Qpid broker.

"""

setup(name="qpid-tools",
      version="0.32",
      author="Apache Qpid",
      author_email="dev@qpid.apache.org",
      package_dir={'' : 'src/py'},
      packages=["qpidtoollibs"],
      scripts=["src/py/qpid-config",
               "src/py/qpid-ha",
               "src/py/qpid-printevents",
               "src/py/qpid-queue-stats",
               "src/py/qpid-route",
               "src/py/qpid-stat",
               "src/py/qpid-tool",
               "src/py/qmf-tool"],
      data_files=[("libexec", ["src/py/qpid-qls-analyze"]),
                  ("share/qpid-tools/python/qlslibs",
                   ["src/py/qlslibs/__init__.py",
                    "src/py/qlslibs/analyze.py",
                    "src/py/qlslibs/efp.py",
                    "src/py/qlslibs/err.py",
                    "src/py/qlslibs/jrnl.py",
                    "src/py/qlslibs/utils.py"])],
      url="http://qpid.apache.org/",
      license="Apache Software License",
      description="Diagnostic and management tools for Apache Qpid brokers.",
      long_description=pypi_long_description,
      install_requires=[
          "qpid-python >= 0.26",
      ])
