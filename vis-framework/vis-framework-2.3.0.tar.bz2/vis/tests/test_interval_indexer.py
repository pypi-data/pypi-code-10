#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           vis
# Program Description:    Helps analyze music with computers.
#
# Filename:               analyzers_tests/test_interval_indexer.py
# Purpose:                Tests for analyzers/indexers/interval.py
#
# Copyright (C) 2013, 2014 Christopher Antila
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------

# allow "no docstring" for everything
# pylint: disable=C0111
# allow "too many public methods" for TestCase
# pylint: disable=R0904


import os
import unittest
import six
import pandas
from music21 import interval, note
from vis.analyzers.indexers.interval import IntervalIndexer, HorizontalIntervalIndexer, real_indexer
from vis.tests.test_note_rest_indexer import TestNoteRestIndexer

# find the pathname of the 'vis' directory
import vis
VIS_PATH = vis.__path__[0]


def make_series(lotuples):
    """
    From a list of two-tuples, make a Series. The list should be like this:

    [(desired_index, value), (desired_index, value), (desired_index, value)]
    """
    new_index = [x[0] for x in lotuples]
    vals = [x[1] for x in lotuples]
    return pandas.Series(vals, index=new_index)

def pandas_maker(lolists):
    """
    Use make_series() to convert a list of appropriate tuples into a list of appropriate Series.

    Input: list of the input desired by make_series()

    Output: list of pandas.Series
    """
    return [make_series(x) for x in lolists]


class TestIntervalIndexerShort(unittest.TestCase):
    """
    These 'short' tests were brought over from the vis9 tests for _event_finder().
    """
    def test_int_indexer_short_1(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4')], [(0.0, 'G3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_2(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.25, 'Rest')]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4'), (0.25, 'Rest')],
                         [(0.0, 'G3'), (0.25, 'Rest')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_3(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.25, 'Rest')]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4')], [(0.0, 'G3'), (0.25, 'Rest')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_4(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.25, 'Rest')]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4'), (0.25, 'Rest')], [(0.0, 'G3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_5(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.5, interval.Interval(note.Note('A3'), note.Note('F4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4'), (0.5, 'F4')],
                         [(0.0, 'G3'), (0.5, 'A3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_6(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.5, interval.Interval(note.Note('A3'), note.Note('G4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4', 1.0)], [(0.0, 'G3'), (0.5, 'A3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_7(self):
        expected = [[(0.0, interval.Interval(note.Note('B3'), note.Note('A4')).name),
                     (0.5, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (1.0, interval.Interval(note.Note('A3'), note.Note('G4')).name),
                     (1.5, interval.Interval(note.Note('B3'), note.Note('F4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'A4'), (0.5, 'G4', 1.0), (1.5, 'F4')],
                         [(0.0, 'B3'), (0.5, 'G3'),
                          (1.0, 'A3'), (1.5, 'B3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_8(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.25, 'Rest'),
                     (0.5, interval.Interval(note.Note('A3'), note.Note('G4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4', 1.0)],
                         [(0.0, 'G3'), (0.25, 'Rest'), (0.5, 'A3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_9(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.25, 'Rest'),
                     (0.5, interval.Interval(note.Note('A3'), note.Note('G4')).name),
                     (1.0, interval.Interval(note.Note('B3'), note.Note('G4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4', 1.0), (1.0, 'G4')],
                         [(0.0, 'G3'), (0.25, 'Rest'), (0.5, 'A3'), (1.0, 'B3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_10(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.25, interval.Interval(note.Note('A3'), note.Note('G4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4', 1.0)], [(0.0, 'G3'), (0.25, 'A3', 0.75)]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_11(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.5, interval.Interval(note.Note('G3'), note.Note('G4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4', 1.0)], [(0.0, 'G3'), (0.5, 'G3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_12(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.25, 'Rest'),
                     (0.5, interval.Interval(note.Note('G3'), note.Note('G4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4', 1.0)],
                         [(0.0, 'G3'), (0.25, 'Rest'), (0.5, 'G3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_13(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.125, 'Rest'),
                     (0.25, interval.Interval(note.Note('A3'), note.Note('G4')).name),
                     (0.375, 'Rest'),
                     (0.5, interval.Interval(note.Note('G3'), note.Note('G4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4', 1.0)],
                         [(0.0, 'G3', 0.125), (0.125, 'Rest', 0.125),
                          (0.25, 'A3', 0.125), (0.375, 'Rest', 0.125), (0.5, 'G3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_14(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.0625, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.125, 'Rest'),
                     (0.1875, 'Rest'),
                     (0.25, interval.Interval(note.Note('A3'), note.Note('G4')).name),
                     (0.3125, interval.Interval(note.Note('A3'), note.Note('G4')).name),
                     (0.375, 'Rest'),
                     (0.4375, 'Rest'),
                     (0.5, interval.Interval(note.Note('G3'), note.Note('G4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4', 0.0625), (0.0625, 'G4', 0.0625),
                          (0.125, 'G4', 0.0625), (0.1875, 'G4', 0.0625),
                          (0.25, 'G4', 0.0625), (0.3125, 'G4', 0.0625),
                          (0.375, 'G4', 0.0625), (0.4375, 'G4', 0.0625),
                          (0.5, 'G4')],
                         [(0.0, 'G3', 0.125), (0.125, 'Rest', 0.125), (0.25, 'A3', 0.125),
                          (0.375, 'Rest', 0.0625), (0.4375, 'Rest', 0.0625), (0.5, 'G3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_15(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.5, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.75, 'Rest'),
                     (1.0, 'Rest'),
                     (1.5, interval.Interval(note.Note('G3'), note.Note('G4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4'), (0.5, 'G4'), (0.75, 'Rest'),
                          (1.0, 'G4'), (1.5, 'G4')],
                         [(0.0, 'G3'), (0.5, 'G3'), (0.75, 'Rest'),
                          (1.0, 'Rest'), (1.5, 'G3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_16(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.5, 'Rest'),
                     (0.75, interval.Interval(note.Note('F3'), note.Note('A4')).name),
                     (1.25, interval.Interval(note.Note('F3'), note.Note('G4')).name),
                     (1.5, interval.Interval(note.Note('E3'), note.Note('B4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4'), (0.5, 'A4', 0.75),
                          (1.25, 'G4'), (1.5, 'B4')],
                         [(0.0, 'G3'), (0.5, 'Rest'),
                          (0.75, 'F3', 0.75), (1.5, 'E3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_int_indexer_short_17(self):
        expected = [[(0.0, interval.Interval(note.Note('G3'), note.Note('G4')).name),
                     (0.5, interval.Interval(note.Note('A3'), note.Note('A4')).name),
                     (0.75, interval.Interval(note.Note('F3'), note.Note('A4')).name),
                     (1.125, 'Rest'),
                     (1.25, 'Rest'),
                     (1.375, interval.Interval(note.Note('G3'), note.Note('F4')).name),
                     (2.0, interval.Interval(note.Note('G3'), note.Note('E4')).name)]]
        expected = {'0,1': pandas_maker(expected)[0]}
        not_processed = [[(0.0, 'G4'), (0.5, 'A4', 0.75), (1.25, 'F4', 0.75),
                          (2.0, 'E4')],
                         [(0.0, 'G3'), (0.5, 'A3'), (0.75, 'F3', 0.375),
                          (1.125, 'Rest'), (1.375, 'G3', 0.625), (2.0, 'G3')]]
        test_in = pandas_maker(not_processed)
        int_indexer = IntervalIndexer(test_in,
                                      {'quality': True, 'simple or compound': 'compound', 'direction': True})
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))


class TestIntervalIndexerLong(unittest.TestCase):
    bwv77_S_B_basis = [(0.0, "P8"), (0.5, "M9"), (1.0, "m10"), (2.0, "P12"), (3.0, "M10"),
                       (4.0, "P12"), (4.5, "m13"), (5.0, "m17"), (5.5, "P12"), (6.0, "M13"),
                       (6.5, "P12"), (7.0, "P8"), (8.0, "m10"), (9.0, "m10"), (10.0, "M10"),
                       (11.0, "M10"), (12.0, "m10"), (13.0, "m10"), (14.0, "P12"), (15.0, "P8"),
                       (16.0, "P8"), (16.5, "M9"), (17.0, "m10"), (18.0, "P12"), (19.0, "M10"),
                       (20.0, "P12"), (20.5, "m13"), (21.0, "m17"), (21.5, "P12"), (22.0, "M13"),
                       (22.5, "P12"), (23.0, "P8"), (24.0, "m10"), (25.0, "m10"), (26.0, "M10"),
                       (27.0, "M10"), (28.0, "m10"), (29.0, "m10"), (30.0, "P12"), (31.0, "P8"),
                       (32.0, "P8"), (32.5, "M9"), (33.0, "m13"), (33.5, "m14"), (34.0, "m13"),
                       (34.5, "m14"), (35.0, "M10"), (36.0, "M10"), (36.5, "P11"), (37.0, "P12"),
                       (38.0, "M10"), (39.0, "P15"), (40.0, "P12"), (40.5, "P11"), (41.0, "M13"),
                       (42.0, "P12"), (43.0, "M17"), (43.5, "M16"), (44.0, "P12"), (44.5, "m13"),
                       (45.0, "P15"), (45.5, "m14"), (46.0, "P12"), (47.0, "P15"), (48.0, "P12"),
                       (49.0, "m10"), (50.0, "M13"), (50.5, "P12"), (51.0, "M10"), (52.0, "m10"),
                       (52.5, "P11"), (53.0, "m13"), (53.5, "d12"), (54.0, "m10"), (55.0, "P12"),
                       (56.0, "P8"), (56.5, "M10"), (57.0, "P12"), (57.5, "m13"), (58.0, "P15"),
                       (59.0, "M17"), (60.0, "P15"), (60.5, "m13"), (61.0, "M13"), (61.5, "m14"),
                       (62.0, "P12"), (63.0, "P8"), (64.0, "P15"), (65.0, "P12"), (65.5, "M13"),
                       (66.0, "m14"), (66.5, "P15"), (67.0, "M17"), (68.0, "P15"), (68.5, "m14"),
                       (69.0, "P12"), (69.5, "m14"), (70.0, "P12"), (71.0, "P15")]

    bwv77_S_B_small_compound_noqual = [(0.0, "8"), (0.5, "9"), (1.0, "10"), (2.0, "12"),
                                       (3.0, "10"), (4.0, "12"), (4.5, "13"), (5.0, "17"),
                                       (5.5, "12"), (6.0, "13"), (6.5, "12"), (7.0, "8")]

    bwv77_S_B_small_simple_qual = [(0.0, "P8"), (0.5, "M2"), (1.0, "m3"), (2.0, "P5"),
                                   (3.0, "M3"), (4.0, "P5"), (4.5, "m6"), (5.0, "m3"),
                                   (5.5, "P5"), (6.0, "M6"), (6.5, "P5"), (7.0, "P8")]

    bwv77_S_B_small_simple_noqual = [(0.0, "8"), (0.5, "2"), (1.0, "3"), (2.0, "5"), (3.0, "3"),
                                     (4.0, "5"), (4.5, "6"), (5.0, "3"), (5.5, "5"), (6.0, "6"),
                                     (6.5, "5"), (7.0, "8")]

    bwv77_soprano_small = [(0.0, "E4"), (0.5, "F#4"), (1.0, "G4"), (2.0, "A4"), (3.0, "B4"),
                           (4.0, "A4"), (5.0, "D5"), (6.0, "C#5"), (7.0, "B4")]

    bwv77_bass_small = [(0.0, "E3"), (1.0, "E3"), (2.0, "D3"), (3.0, "G3"), (4.0, "D3"), (4.5, "C#3"),
                        (5.0, "B2"), (5.5, "G3"), (6.0, "E3"), (6.5, "F#3"), (7.0, "B3")]

    def setUp(self):
        self.bwv77_soprano = make_series(TestNoteRestIndexer.bwv77_soprano)
        self.bwv77_bass = make_series(TestNoteRestIndexer.bwv77_bass)
        self.bwv77_s_small = make_series(self.bwv77_soprano_small)
        self.bwv77_b_small = make_series(self.bwv77_bass_small)

    def test_interval_indexer_1(self):
        # BWV7.7: full soprano and bass parts
        test_parts = [self.bwv77_soprano, self.bwv77_bass]
        expected = {'0,1': make_series(TestIntervalIndexerLong.bwv77_S_B_basis)}
        setts = {'simple or compound': 'compound', 'quality': True}
        int_indexer = IntervalIndexer(test_parts, setts)
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_interval_indexer_2(self):
        # BWV7.7: small soprano and bass parts; "simple" in settings
        test_parts = [self.bwv77_s_small, self.bwv77_b_small]
        expected = {'0,1': make_series(TestIntervalIndexerLong.bwv77_S_B_small_simple_qual)}
        setts = {'simple or compound': 'simple', 'quality': True}
        int_indexer = IntervalIndexer(test_parts, setts)
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_interval_indexer_3(self):
        # BWV7.7: small soprano and bass parts; "simple" and "quality" not in settings, and the
        # settings are in fact not specified
        test_parts = [self.bwv77_s_small, self.bwv77_b_small]
        expected = {'0,1': make_series(TestIntervalIndexerLong.bwv77_S_B_small_compound_noqual)}
        # setts = {}
        int_indexer = IntervalIndexer(test_parts)
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_interval_indexer_4(self):
        # BWV7.7: small soprano and bass parts; "simple" in settings, "quality" not
        test_parts = [self.bwv77_s_small, self.bwv77_b_small]
        expected = {'0,1': make_series(TestIntervalIndexerLong.bwv77_S_B_small_simple_noqual)}
        setts = {'simple or compound': 'simple'}
        int_indexer = IntervalIndexer(test_parts, setts)
        actual = int_indexer.run()['interval.IntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))


class TestIntervalIndexerIndexer(unittest.TestCase):
    def test_int_ind_indexer_1(self):
        # ascending simple: quality, simple
        notes = ['E4', 'C4']
        expected = 'M3'
        actual = real_indexer(notes, quality=True, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_2(self):
        # ascending simple: quality, compound
        notes = ['E4', 'C4']
        expected = 'M3'
        actual = real_indexer(notes, quality=True, simple=False, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_3(self):
        # ascending simple: noQuality, simple
        notes = ['E4', 'C4']
        expected = '3'
        actual = real_indexer(notes, quality=False, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_4(self):
        # ascending simple: noQuality, compound
        notes = ['E4', 'C4']
        expected = '3'
        actual = real_indexer(notes, quality=False, simple=False, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_5(self):
        # ascending compound: quality, simple
        notes = ['E5', 'C4']
        expected = 'M3'
        actual = real_indexer(notes, quality=True, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_6(self):
        # ascending compound: quality, compound
        notes = ['E5', 'C4']
        expected = 'M10'
        actual = real_indexer(notes, quality=True, simple=False, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_7(self):
        # ascending compound: noQuality, simple
        notes = ['E5', 'C4']
        expected = '3'
        actual = real_indexer(notes, quality=False, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_8(self):
        # ascending compound: noQuality, compound
        notes = ['E5', 'C4']
        expected = '10'
        actual = real_indexer(notes, quality=False, simple=False, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_9(self):
        # descending simple: quality, simple
        notes = ['C4', 'E4']
        expected = '-M3'
        actual = real_indexer(notes, quality=True, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_10(self):
        # descending simple: quality, compound
        notes = ['C4', 'E4']
        expected = '-M3'
        actual = real_indexer(notes, quality=True, simple=False, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_11(self):
        # descending simple: noQuality, simple
        notes = ['C4', 'E4']
        expected = '-3'
        actual = real_indexer(notes, quality=False, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_12(self):
        # descending simple: noQuality, compound
        notes = ['C4', 'E4']
        expected = '-3'
        actual = real_indexer(notes, quality=False, simple=False, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_13(self):
        # descending compound: quality, simple
        notes = ['C4', 'E5']
        expected = '-M3'
        actual = real_indexer(notes, quality=True, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_14(self):
        # descending compound: quality, compound
        notes = ['C4', 'E5']
        expected = '-M10'
        actual = real_indexer(notes, quality=True, simple=False, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_15(self):
        # descending compound: noQuality, simple
        notes = ['C4', 'E5']
        expected = '-3'
        actual = real_indexer(notes, quality=False, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_16(self):
        # descending compound: noQuality, compound
        notes = ['C4', 'E5']
        expected = '-10'
        actual = real_indexer(notes, quality=False, simple=False, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_17(self):
        # rest in upper part
        notes = ['C4', 'Rest']
        expected = 'Rest'
        actual = real_indexer(notes, quality=False, simple=False, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_18(self):
        # rest in lower part
        notes = ['Rest', 'C4']
        expected = 'Rest'
        actual = real_indexer(notes, quality=True, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_19(self):
        # triple augmented ascending
        notes = ['G###4', 'C4']
        expected = 'AAA5'
        actual = real_indexer(notes, quality=True, simple=False, direction=True)
        self.assertEqual(expected, actual)
        actual = real_indexer(notes, quality=True, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_20(self):
        # triple diminished descending
        notes = ['C###4', 'G4']
        expected = '-ddd5'
        actual = real_indexer(notes, quality=True, simple=False, direction=True)
        self.assertEqual(expected, actual)
        actual = real_indexer(notes, quality=True, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_21(self):
        # too few inputs
        notes = ['C4']
        expected = None
        actual = real_indexer(notes, quality=True, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_int_ind_indexer_22(self):
        # too many inputs
        notes = ['C4', 'D4', 'E4']
        expected = None
        actual = real_indexer(notes, quality=True, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_regression_1(self):
        "indexer_qual_simple(): P15 --> P8"
        notes = ['C6', 'C4']
        expected = 'P8'
        actual = real_indexer(notes, quality=True, simple=True, direction=True)
        self.assertEqual(expected, actual)

    def test_regression_2(self):
        "indexer_nq_simple(): 15 --> 8"
        notes = ['C6', 'C4']
        expected = '8'
        actual = real_indexer(notes, quality=False, simple=True, direction=True)
        self.assertEqual(expected, actual)


class TestHorizIntervalIndexerLong(unittest.TestCase):
    # data_interval_indexer_1.csv
    bwv77_S_B_short = pandas.read_csv(os.path.join(VIS_PATH, 'tests', 'data_interval_indexer_1.csv'),
                                      index_col=0,
                                      names=['a'],
                                      dtype={'a': str})

    # data_interval_indexer_2.csv
    bwv77_S_B_short_noqual = pandas.read_csv(os.path.join(VIS_PATH, 'tests', 'data_interval_indexer_2.csv'),
                                             index_col=0,
                                             names=['a'],
                                             dtype={'a': str})

    # data_interval_indexer_3.csv
    bwv77_S_B_basis = pandas.read_csv(os.path.join(VIS_PATH, 'tests', 'data_interval_indexer_3.csv'),
                                      index_col=0,
                                      names=['a'],
                                      dtype={'a': str})

    def setUp(self):
        self.bwv77_soprano = make_series(TestNoteRestIndexer.bwv77_soprano)
        self.bwv77_bass = make_series(TestNoteRestIndexer.bwv77_bass)

    def test_interval_indexer_1a(self):
        # BWV7.7: first 26 things in soprano part
        test_parts = [self.bwv77_soprano]
        expected = TestHorizIntervalIndexerLong.bwv77_S_B_short['a']
        setts = {'simple or compound': 'compound', 'quality': True}
        int_indexer = HorizontalIntervalIndexer(test_parts, setts)
        actual = int_indexer.run()['interval.HorizontalIntervalIndexer']['0'].iloc[:26]
        self.assertSequenceEqual(list(expected.index), list(actual.index))
        self.assertSequenceEqual(list(expected), list(actual))

    def test_interval_indexer_1b(self):
        # BWV7.7: first 26 things in soprano part (no settings specified)
        test_parts = [self.bwv77_soprano]
        expected = TestHorizIntervalIndexerLong.bwv77_S_B_short_noqual['a']
        #setts = {'simple or compound': 'compound', 'quality': True}
        int_indexer = HorizontalIntervalIndexer(test_parts)
        actual = int_indexer.run()['interval.HorizontalIntervalIndexer']['0'].iloc[:26]
        self.assertSequenceEqual(list(expected.index), list(actual.index))
        self.assertSequenceEqual(list(expected), list(actual))

    def test_interval_indexer_1c(self):
        # BWV7.7: first 26 things in soprano part (simple; quality)
        test_parts = [self.bwv77_soprano]
        expected = TestHorizIntervalIndexerLong.bwv77_S_B_short['a']
        setts = {'simple or compound': 'simple', 'quality': True}
        int_indexer = HorizontalIntervalIndexer(test_parts, setts)
        actual = int_indexer.run()['interval.HorizontalIntervalIndexer']['0'].iloc[:26]
        self.assertSequenceEqual(list(expected.index), list(actual.index))
        self.assertSequenceEqual(list(expected), list(actual))

    def test_interval_indexer_1d(self):
        # BWV7.7: first 26 things in soprano part (simple; no quality)
        test_parts = [self.bwv77_soprano]
        expected = TestHorizIntervalIndexerLong.bwv77_S_B_short_noqual['a']
        setts = {'simple or compound': 'simple', 'quality': False}
        int_indexer = HorizontalIntervalIndexer(test_parts, setts)
        actual = int_indexer.run()['interval.HorizontalIntervalIndexer']['0'].iloc[:26]
        self.assertSequenceEqual(list(expected.index), list(actual.index))
        self.assertSequenceEqual(list(expected), list(actual))

    def test_interval_indexer_2(self):
        # BWV7.7: whole soprano part
        # NB: this test is more rigourous than the others, since it actually uses the DataFrame
        test_parts = [self.bwv77_soprano]
        expected = {'0': TestHorizIntervalIndexerLong.bwv77_S_B_basis['a']}
        setts = {'simple or compound': 'compound', 'quality': True}
        int_indexer = HorizontalIntervalIndexer(test_parts, setts)
        actual = int_indexer.run()['interval.HorizontalIntervalIndexer']
        self.assertEqual(len(expected), len(actual.columns))
        for key in six.iterkeys(expected):
            self.assertTrue(key in actual)
            self.assertSequenceEqual(list(expected[key].index), list(actual[key].index))
            self.assertSequenceEqual(list(expected[key]), list(actual[key]))

    def test_interval_indexer_3(self):
        """BWV7.7: whole bass part; 'horiz_attach_later' is True"""
        test_parts = [self.bwv77_bass]
        setts = {'simple or compound': 'compound', 'quality': True, 'horiz_attach_later': True}
        expected = pandas.read_pickle(os.path.join(VIS_PATH, 'tests', 'corpus', 'data_horiz_int_ind_3.pickle'))
        actual = HorizontalIntervalIndexer(test_parts, setts).run()
        self.assertSequenceEqual(list(expected.columns), list(actual.columns))
        for col_name in expected.columns:
            self.assertEqual(list(expected[col_name].index), list(actual[col_name].index))
            self.assertEqual(list(expected[col_name].values), list(actual[col_name].values))


#-------------------------------------------------------------------------------------------------#
# Definitions                                                                                     #
#-------------------------------------------------------------------------------------------------#
INTERVAL_INDEXER_SHORT_SUITE = unittest.TestLoader().loadTestsFromTestCase(TestIntervalIndexerShort)
INTERVAL_INDEXER_LONG_SUITE = unittest.TestLoader().loadTestsFromTestCase(TestIntervalIndexerLong)
INT_IND_INDEXER_SUITE = unittest.TestLoader().loadTestsFromTestCase(TestIntervalIndexerIndexer)
HORIZ_INT_IND_LONG_SUITE = unittest.TestLoader().loadTestsFromTestCase(TestHorizIntervalIndexerLong)
