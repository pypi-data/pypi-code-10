#!/usr/bin/env python
# Ivana Chingovska <ivana.chingovska@idiap.ch>
# Sun Jul  8 20:35:55 CEST 2012
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
from setuptools import setup, find_packages

# Define package version
version = open("version.txt").read().rstrip()

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    name='bob.thesis.ichingo2015',
    version=version,
    description='Trustworthy biometric recognition under spoofing attacks: application to the face mode',
    url='http://pypi.python.org/pypi/bob.thesis.ichingo2015',
    license='GPLv3',
    author='Ivana Chingovska',
    author_email='ivana.chingovska@idiap.ch',
    long_description=open('README.rst').read(),
    keywords='antispoofing, face spoofing attacks, face spoofing database, bob, client-specific anti-spoofing, spoofing evaluation',

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,

    namespace_packages=[
      "bob",
      "bob.thesis",
      ],

    install_requires=[
      "setuptools",
      "bob.db.base", #1.1.0
      "bob.db.replay", # Replay-Attack database
      "antispoofing.utils",  # Utils Package
    ],

    entry_points={
      'console_scripts': [

        'replay_attack_frames.py = bob.thesis.ichingo2015.script.diverse.replay_attack_frames:main',

        'sort_cohort_models_kl.py = bob.thesis.ichingo2015.script.clientspec.sort_cohort_models_kl:main',
        'sort_cohort_models_reynolds.py = bob.thesis.ichingo2015.script.clientspec.sort_cohort_models_reynolds:main',
        'naive_likelihood_sorted_cohortmodels.py = bob.thesis.ichingo2015.script.clientspec.naive_likelihood_sorted_cohortmodels:main',
        'svmtrain.py = bob.thesis.ichingo2015.script.clientspec.svmtrain:main',
        'svmeval.py = bob.thesis.ichingo2015.script.clientspec.svmeval:main',
        'svmapprox_train.py = bob.thesis.ichingo2015.script.clientspec.svmapprox_train:main',
        'svmapprox_eval.py = bob.thesis.ichingo2015.script.clientspec.svmapprox_eval:main',
        'svm_clientspec_train.py = bob.thesis.ichingo2015.script.clientspec.svm_clientspec_train:main',
        'svmapprox_clientspec_train.py = bob.thesis.ichingo2015.script.clientspec.svmapprox_clientspec_train:main',
        'svm_clientspec_eval.py = bob.thesis.ichingo2015.script.clientspec.svm_clientspec_eval:main',
        'svm_clientspec_eval_impostors.py = bob.thesis.ichingo2015.script.clientspec.svm_clientspec_eval_impostors:main',
        'svmapprox_clientspec_eval.py = bob.thesis.ichingo2015.script.clientspec.svmapprox_clientspec_eval:main',
        'svmapprox_clientspec_eval_impostors.py = bob.thesis.ichingo2015.script.clientspec.svmapprox_clientspec_eval_impostors:main',
        'scores_box_plot.py = bob.thesis.ichingo2015.script.clientspec.scores_box_plot:main',
        'score_evaluation_crossdb.py = bob.thesis.ichingo2015.script.score_evaluation_crossdb:main',

        'and_decision_epsc.py = bob.thesis.ichingo2015.script.fusion.and_decision_epsc:main',
        'and_decision_epsc_cs.py = bob.thesis.ichingo2015.script.fusion.and_decision_epsc_cs:main',
        ],
      },

)
