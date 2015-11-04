import unittest
from pyppo import pipeline
from unittest.mock import Mock


class SplitPipelineTestCase(unittest.TestCase):

    def test_fork_pipeline(self):
        entry = {'i': 1}

        initial_step = Mock()
        initial_step.return_value = entry

        def initial_left(entry):
            entry['x'] = 1
            return entry

        def initial_right(entry):
            entry['y'] = 2
            return entry

        left = Mock()
        left.return_value = entry

        right = Mock()
        right.return_value = entry

        left_branch = [initial_left, left]
        right_branch = [initial_right, right]

        forked_pipeline = pipeline.pipeline([entry],
                                        initial_step,
                                        pipeline.fork(left_branch, right_branch))

        pipeline.consume(forked_pipeline)

        self.assertTrue(left.called)
        self.assertEqual(left.call_args[0][0], {'x': 1, 'i': 1})
        self.assertTrue(right.called)
        self.assertEqual(right.call_args[0][0], {'y': 2, 'i': 1})


class PipilineGenerationTestCase(unittest.TestCase):

    def test_functions_are_called(self):
        initial_arg = {}

        def generator():
            yield initial_arg

        first_function = Mock()
        first_function.return_value = initial_arg
        second_function = Mock()
        second_function.return_value = initial_arg
        pipeline.consume(pipeline.pipeline(generator(), first_function, second_function))
        self.assertTrue(first_function.called)
        self.assertEqual(first_function.call_args[0][0], initial_arg)
        self.assertTrue(second_function.called)
        self.assertEqual(second_function.call_args[0][0], initial_arg)

    def test_functions_in_pipeline_change_data(self):
        entry = {}

        def add_x(entry):
            entry['x'] = 1
            return entry

        def add_y(entry):
            entry['y'] = 2
            return entry

        pipeline.consume(pipeline.pipeline([entry], add_x, add_y))
        self.assertTrue('x' in entry)
        self.assertTrue('y' in entry)

    def test_steps_can_be_validated(self):
        entry = {}
        add_y = Mock()
        add_y.return_value = entry

        @pipeline.validate_with(lambda entry: 'y' in entry)
        def not_running_step(entry):
            return entry

        test_pipeline = pipeline.pipeline([entry], add_y, not_running_step)
        self.assertRaises(pipeline.StepValidationError, pipeline.consume, test_pipeline)


unittest.main()
