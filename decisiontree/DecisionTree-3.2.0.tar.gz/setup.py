#!/usr/bin/env python

### setup.py

#from distutils.core import setup

from setuptools import setup, find_packages
import sys, os

setup(name='DecisionTree',
      version='3.2.0',
      author='Avinash Kak',
      author_email='kak@purdue.edu',
      maintainer='Avinash Kak',
      maintainer_email='kak@purdue.edu',
      url='https://engineering.purdue.edu/kak/distDT/DecisionTree-3.2.0.html',
      download_url='https://engineering.purdue.edu/kak/distDT/DecisionTree-3.2.0.tar.gz',
      description='A Python module for decision-tree based classification of multidimensional data',
      long_description=''' 

**Version 3.2.0** adds boosting capability to the decision tree module.

**Version 3.0** adds bagging capability to the decision tree module.  If you have a large enough training dataset, you can now construct multiple decision trees and have the final classification be based on a majority vote from all the trees.  This can average out the noise in the classification process.

**Version 2.3** gives the module a new capability ---
ability to introspect about the classification decisions at
the nodes of the decision tree.

With regard to the purpose of the module, assuming you have
placed your training data in a CSV file, all you have to do
is to supply the name of the file to this module and it does
the rest for you without much effort on your part for
classifying a new data sample.  A decision tree classifier
consists of feature tests that are arranged in the form of a
tree. The feature test associated with the root node is one
that can be expected to maximally disambiguate the different
possible class labels for a new data record.  From the root
node hangs a child node for each possible outcome of the
feature test at the root. This maximal class-label
disambiguation rule is applied at the child nodes
recursively until you reach the leaf nodes.  A leaf node may
correspond either to the maximum depth desired for the
decision tree or to the case when there is nothing further
to gain by a feature test at the node.

Typical usage syntax:

::

      training_datafile = "stage3cancer.csv"
      dt = DecisionTree.DecisionTree( 
                      training_datafile = training_datafile,
                      csv_class_column_index = 2,
                      csv_columns_for_features = [3,4,5,6,7,8],
                      entropy_threshold = 0.01,
                      max_depth_desired = 8,
                      symbolic_to_numeric_cardinality_threshold = 10,
           )

        dt.get_training_data()
        dt.calculate_first_order_probabilities()
        dt.calculate_class_priors()
        dt.show_training_data()
        root_node = dt.construct_decision_tree_classifier()
        root_node.display_decision_tree("   ")

        test_sample  = ['g2 = 4.2',
                        'grade = 2.3',
                        'gleason = 4',
                        'eet = 1.7',
                        'age = 55.0',
                        'ploidy = diploid']
        classification = dt.classify(root_node, test_sample)
        print "Classification: ", classification

          ''',

      license='Python Software Foundation License',
      keywords='data classification, decision trees, information analysis',
      platforms='All platforms',
      classifiers=['Topic :: Scientific/Engineering :: Information Analysis', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3.4'],
      packages=['DecisionTree', 'DecisionTreeWithBagging', 'BoostedDecisionTree']
)
