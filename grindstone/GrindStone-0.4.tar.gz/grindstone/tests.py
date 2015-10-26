#!/usr/bin/env python
"""
File: test.py
Package: grindstone
Author: Elijah Caine
Description:
    Test GrindStone lib functionality
"""
from lib import GrindStone
import unittest
import shutil
import os

class TestGrindStoneLibrary(unittest.TestCase):

    def setUp(self):
        # We're testing everything in a /tmp/* directory to avoid overwriting
        # an existing .grindstone file
        self.testing_path = '/tmp/grindstone_testing/'

        try:
            # Make directory for testing stuffs
            os.mkdir(self.testing_path)
        # If that directory exists
        except FileExistsError:
            # Blow everything away
            shutil.rmtree(self.testing_path)
            os.mkdir(self.testing_path)
        # Move to the testing directory
        os.chdir(self.testing_path)

        self.cwd = os.getcwd()


    def tearDown(self):
        try:
            # Remove the grindstone_path
            os.remove(self.gs.grindstone_path)
        except FileNotFoundError:
            # It's okay, this is probably supposed to happen
            pass
        except AttributeError:
            # self.gs is not found
            pass
        finally:
            # Burn the testing files. Burn them with fire.
            shutil.rmtree(self.testing_path)


    def test_cwd_path(self):
        os.mkdir('./t/')
        os.chdir('./t/')
        self.cwd = os.getcwd()
        open('.grindstone', 'w').close()
        self.gs = GrindStone(self.cwd)
        self.assertEqual(self.gs.grindstone_path,\
                         os.path.realpath(self.gs.grindstone_filename))


    def test_no_path_given(self):
        with self.assertRaises(ValueError) as err:
            self.gs = GrindStone()
        self.assertEqual(str(err.exception), 'Path must not be None')


    def test_add_one_complete_task(self):
        self.gs = GrindStone(self.cwd)
        self.gs.add_task('book1', 'read the book')
        self.assertEqual(self.gs.get_tasks(), [{'book1': 'read the book'}])

        self.gs.write_grindstone()
        with open(self.gs.grindstone_path, 'r') as f:
            file_contents = f.read()
        self.assertTrue('"tasks": [{"book1": "read the book"}]'\
                         in file_contents)


    def test_add_one_shallow_task(self):
        self.gs = GrindStone(self.cwd)
        self.gs.add_task('bookA')
        self.assertEqual(self.gs.get_tasks(), [{'bookA': None}])

        self.gs.write_grindstone()
        with open(self.gs.grindstone_path, 'r') as f:
            file_contents = f.read()
        self.assertTrue('"tasks": [{"bookA": null}]' in file_contents)


    def test_add_complete_tasks(self):
        self.gs = GrindStone(self.cwd)
        self.gs.add_task('book1', 'read the book')
        self.gs.add_task('book2', 'read the other book')
        self.assertEqual(self.gs.get_tasks(),\
                         [{'book1': 'read the book'},\
                          {'book2': 'read the other book'}])


        self.gs.write_grindstone()
        with open(self.gs.grindstone_path, 'r') as f:
            file_contents = f.read()
        self.assertTrue('"tasks": [{"book1": "read the book"}, '+
                                  '{"book2": "read the other book"}]'\
                          in file_contents)


    def test_open_grindstone(self):
        self.gs = GrindStone(self.cwd)
        self.gs.add_task('bookAlpha', 'read the book')
        self.gs.write_grindstone()

        self.gs2 = GrindStone(self.cwd)
        self.assertEqual(self.gs2.get_tasks(),\
                         [{'bookAlpha': 'read the book'}])


    def test_open_modify_grindstone(self):
        self.gs = GrindStone(self.cwd)
        self.gs.add_task('bookAlpha', 'read the book')
        self.gs.write_grindstone()

        self.gs2 = GrindStone(self.cwd)
        self.gs2.add_task('bookBeta', 'This one matters less')
        self.assertEqual(self.gs2.get_tasks(),\
                         [{'bookAlpha': 'read the book'},
                          {'bookBeta': 'This one matters less'}])

        self.gs2.write_grindstone()
        with open(self.gs2.grindstone_path, 'r') as f:
            file_contents2 = f.read()
            self.assertTrue('"tasks": [{"bookAlpha": "read the book"}, '+
                                      '{"bookBeta": "This one matters less"}]'\
                            in file_contents2)


    def test_add_empty_task(self):
        self.gs = GrindStone(self.cwd)
        with self.assertRaises(ValueError) as err:
            self.gs.add_task()

        self.assertEqual(str(err.exception),\
                         'Tasks `name` cannot be None')
        self.assertEqual(self.gs.get_tasks(), [])


    def test_add_task_with_no_name(self):
        self.gs = GrindStone(self.cwd)
        with self.assertRaises(ValueError) as err:
            self.gs.add_task(desc='foo')

        self.assertEqual(str(err.exception),\
                         'Tasks `name` cannot be None')
        self.assertEqual(self.gs.get_tasks(), [])


    def test_fetch_empty_task(self):
        self.gs = GrindStone(self.cwd)
        self.gs.add_task('bookAlpha', None)
        self.gs.write_grindstone()

        self.gs2 = GrindStone(self.cwd)
        self.assertEqual(self.gs2.get_task('bookAlpha'),
                         {'bookAlpha': None})


    def test_fetch_task(self):
        self.gs = GrindStone(self.cwd)
        self.gs.add_task('bookAlpha', 'The Most Awesome Book')
        self.gs.write_grindstone()

        self.gs2 = GrindStone(self.cwd)
        self.assertEqual(self.gs2.get_task('bookAlpha'),
                         {'bookAlpha': 'The Most Awesome Book'})


    def test_non_existent_get_task(self):
        self.gs = GrindStone(self.cwd)
        self.gs.add_task('bookAlpha', 'The Most Awesome Book')
        self.gs.write_grindstone()

        self.gs2 = GrindStone(self.cwd)
        self.assertEqual(self.gs2.get_task('bookOmega'), None)


    def test_delete_task(self):
        self.gs = GrindStone(self.cwd)
        self.gs.add_task('bookAlpha', 'The Most Awesome Book')
        self.gs.delete_task('bookAlpha')
        self.assertEqual(self.gs.get_task('bookAlpha'), None)
        self.assertEqual(self.gs.get_tasks(), [])


    def test_delete_non_existent_task(self):
        self.gs = GrindStone(self.cwd)
        self.assertFalse(self.gs.delete_task('bookAlpha'))
        self.assertEqual(self.gs.get_tasks(), [])


    def test_fail_to_add_double_task(self):
        self.gs = GrindStone(self.cwd)
        self.gs.add_task('bookA')
        self.assertEqual(self.gs.get_tasks(), [{'bookA': None}])
        
        with self.assertRaises(ValueError) as err:
            self.gs.add_task('bookA')

        self.assertEqual(str(err.exception), 'Task already exists')
        self.assertEqual(self.gs.get_tasks(), [{'bookA': None}])


if __name__ == '__main__':
    unittest.main()
