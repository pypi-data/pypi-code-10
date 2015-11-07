import os
import unittest
import sys

from src import pygradle


try:
    THIS_FILE_NAME = __file__
except NameError:
    THIS_FILE_NAME = sys.argv[0]

TEST_APP_DIR = os.path.abspath(os.path.join(os.path.dirname(THIS_FILE_NAME),
                                            './testapp/'))
GRADLE_PATH = os.path.join(TEST_APP_DIR, 'gradlew')


class TestFactory(unittest.TestCase):

    def setUp(self):
        self.save_path = os.getcwd()
        os.chdir(TEST_APP_DIR)

    def tearDown(self):
        os.chdir(self.save_path)

    def test_should_gradle_clean_ends_with_success_status(self):
        gradle = pygradle.GradleFactory.create(gradle_cmd=GRADLE_PATH)
        self.assertIn('BUILD SUCCESSFUL', gradle.clean())


class TestGradle(unittest.TestCase):

    def setUp(self):
        self.save_path = os.getcwd()
        os.chdir(TEST_APP_DIR)
        self.sut = pygradle.Gradle(gradle_cmd=GRADLE_PATH)

    def tearDown(self):
        os.chdir(self.save_path)

    def test_should_contain_and_run_basic_tasks(self):
        for cmd in pygradle.gradlew._BASIC_GRADLE_TASKS:
            self.assertTrue(getattr(self.sut, cmd))
        self.assertIn('BUILD SUCCESSFUL', self.sut.clean())

    def test_should_return_correct_version(self):
        result = self.sut.versions()
        self.assertEqual('2.8', result['Gradle'])
        self.assertEqual('2.4.4', result['Groovy'])
        self.assertIsNotNone(result['Build time'])
        self.assertIsNotNone(result['Build number'])
        self.assertIsNotNone(result['Revision'])

    def test_should_execute_gradle_commands(self):
        self.sut.add_tasks('clean', 'build')
        self.assertIn('BUILD SUCCESSFUL', self.sut.execute())
