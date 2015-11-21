import unittest
from tempfile import NamedTemporaryFile
from .runners import NodeRunner, BabelRunner


class TestNodeRunner(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestNodeRunner, self).__init__(*args, **kwargs)
        self.runner = NodeRunner()

    def get_script_without_args(self):
        return 'console.log(\'test\')'

    def get_script_with_args(self, index):
        return '(function () {console.log(process.argv[' + str(index) + '])})()'

    def create_script(self, use_args=False):
        file = NamedTemporaryFile(delete=True)
        if use_args:
            file.write(bytes(self.get_script_with_args(2), 'utf-8'))
        else:
            file.write(bytes(self.get_script_without_args(), 'utf-8'))
        file.flush()
        return file

    def test_execute_without_args(self):
        result = self.runner.execute(self.get_script_without_args())
        self.assertEqual(result, 'test')

    def test_execute_with_args(self):
        result = self.runner.execute(self.get_script_with_args(1), 'test')
        self.assertEqual(result, 'test')

    def test_execute_silent_without_args(self):
        result = self.runner.execute_silent(self.get_script_without_args())
        self.assertTrue(result)

    def test_execute_silent_with_args(self):
        result = self.runner.execute_silent(self.get_script_with_args(1), 'test')
        self.assertTrue(result)

    def test_execute_script_without_args(self):
        temp_file = self.create_script()
        result = self.runner.execute_script(temp_file.name)
        self.assertEqual(result, 'test')
        temp_file.close()

    def test_execute_script_with_args(self):
        temp_file = self.create_script(True)
        result = self.runner.execute_script(temp_file.name, 'test')
        self.assertEqual(result, 'test')
        temp_file.close()

    def test_execute_script_silent_without_args(self):
        temp_file = self.create_script()
        result = self.runner.execute_script_silent(temp_file.name)
        self.assertTrue(result)
        temp_file.close()

    def test_execute_script_silent_with_args(self):
        temp_file = self.create_script(True)
        result = self.runner.execute_script_silent(temp_file.name, 'test')
        self.assertTrue(result)
        temp_file.close()


class TestBabelRunner(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBabelRunner, self).__init__(*args, **kwargs)
        # TODO: Test babel settings
        self.runner = BabelRunner()

    def get_script_without_args(self):
        return 'console.log(\'test\')'

    def get_script_with_args(self, index):
        return '(() => {console.log(process.argv[' + str(index) + '])})()'

    def create_script(self, use_args=False):
        file = NamedTemporaryFile(delete=True)
        if use_args:
            file.write(bytes(self.get_script_with_args(2), 'utf-8'))
        else:
            file.write(bytes(self.get_script_without_args(), 'utf-8'))
        file.flush()
        return file

    def test_execute_without_args(self):
        result = self.runner.execute(self.get_script_without_args())
        self.assertEqual(result, 'test')

    def test_execute_with_args(self):
        result = self.runner.execute(self.get_script_with_args(4), 'test')
        self.assertEqual(result, 'test')

    def test_execute_silent_without_args(self):
        result = self.runner.execute_silent(self.get_script_without_args())
        self.assertTrue(result)

    def test_execute_silent_with_args(self):
        result = self.runner.execute_silent(self.get_script_with_args(2), 'test')
        self.assertTrue(result)

    def test_execute_script_without_args(self):
        temp_file = self.create_script()
        result = self.runner.execute_script(temp_file.name)
        self.assertEqual(result, 'test')
        temp_file.close()

    def test_execute_script_with_args(self):
        temp_file = self.create_script(True)
        result = self.runner.execute_script(temp_file.name, 'test')
        self.assertEqual(result, 'test')
        temp_file.close()

    def test_execute_script_silent_without_args(self):
        temp_file = self.create_script()
        result = self.runner.execute_script_silent(temp_file.name)
        self.assertTrue(result)
        temp_file.close()

    def test_execute_script_silent_with_args(self):
        temp_file = self.create_script(True)
        result = self.runner.execute_script_silent(temp_file.name, 'test')
        self.assertTrue(result)
        temp_file.close()

if __name__ == '__main__':
    unittest.main()
