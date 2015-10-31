
import json
import unittest

import m26


class RunWalkCalculatorTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def log_result(self, result_dict):
        print(json.dumps(result_dict, sort_keys=True, indent=2))

    def test_calculate_all_walking(self):
        run_hhmmss = '00:00'
        run_ppm = '9:00'
        walk_hhmmss = '10:00'
        walk_ppm = '18:00'
        miles = '3.333'

        result = m26.RunWalkCalculator.calculate(run_hhmmss, run_ppm, walk_hhmmss, walk_ppm, miles)
        self.log_result(result)

        self.assertAlmostEqual(result['avg_mph'], 3.33333333)
        self.assertAlmostEqual(result['miles'], 3.333)
        self.assertAlmostEqual(result['proj_miles'], 3.333)

        self.assertTrue(result['avg_ppm'] == '18:00.0', "avg_ppm is incorrect")
        self.assertTrue(result['proj_time'] == '00:59:59', "proj_time is incorrect")
        self.assertTrue(result['run_hhmmss'] == '00:00', "run_hhmmss is incorrect")
        self.assertTrue(result['run_ppm'] == '9:00', "run_ppm is incorrect")
        self.assertTrue(result['walk_hhmmss'] == '10:00', "walk_hhmmss is incorrect")
        self.assertTrue(result['walk_ppm'] == '18:00', "walk_ppm is incorrect")

    def test_calculate_all_running(self):
        run_hhmmss = '10:00'
        run_ppm = '9:00'
        walk_hhmmss = '00:00'
        walk_ppm = '18:00'
        miles = '3.333'

        result = m26.RunWalkCalculator.calculate(run_hhmmss, run_ppm, walk_hhmmss, walk_ppm, miles)
        self.log_result(result)

        self.assertAlmostEqual(result['avg_mph'], 6.66666666)
        self.assertAlmostEqual(result['miles'], 3.333)
        self.assertAlmostEqual(result['proj_miles'], 3.333)

        self.assertTrue(result['avg_ppm'] == '9:00.0', "avg_ppm is incorrect")
        self.assertTrue(result['proj_time'] == '00:29:59', "proj_time is incorrect")
        self.assertTrue(result['run_hhmmss'] == '10:00', "run_hhmmss is incorrect")
        self.assertTrue(result['run_ppm'] == '9:00', "run_ppm is incorrect")
        self.assertTrue(result['walk_hhmmss'] == '00:00', "walk_hhmmss is incorrect")
        self.assertTrue(result['walk_ppm'] == '18:00', "walk_ppm is incorrect")

    def test_calculate_1_to_1_run_walk(self):
        run_hhmmss = '10:00'
        run_ppm = '8:00'
        walk_hhmmss = '10:00'
        walk_ppm = '16:00'
        miles = '4.0'

        result = m26.RunWalkCalculator.calculate(run_hhmmss, run_ppm, walk_hhmmss, walk_ppm, miles)
        self.log_result(result)

        self.assertAlmostEqual(result['avg_mph'], 5.0000000)
        self.assertAlmostEqual(result['miles'], 4.000)
        self.assertAlmostEqual(result['proj_miles'], 4.000)

        self.assertTrue(result['avg_ppm'] == '12:00.0', "avg_ppm is incorrect")
        self.assertTrue(result['proj_time'] == '00:48:00', "proj_time is incorrect")
        self.assertTrue(result['run_hhmmss'] == '10:00', "run_hhmmss is incorrect")
        self.assertTrue(result['run_ppm'] == '8:00', "run_ppm is incorrect")
        self.assertTrue(result['walk_hhmmss'] == '10:00', "walk_hhmmss is incorrect")
        self.assertTrue(result['walk_ppm'] == '16:00', "walk_ppm is incorrect")

    def test_calculate_9_to_1_marathon(self):
        run_hhmmss = '9:00'
        run_ppm = '9:00'
        walk_hhmmss = '1:00'
        walk_ppm = '18:00'
        miles = '26.2'

        result = m26.RunWalkCalculator.calculate(run_hhmmss, run_ppm, walk_hhmmss, walk_ppm, miles)
        self.log_result(result)

        self.assertAlmostEqual(result['avg_mph'], 6.0606060606060606)
        self.assertAlmostEqual(result['miles'], 26.200)
        self.assertAlmostEqual(result['proj_miles'], 26.200)

        self.assertTrue(result['avg_ppm'] == '9:54.0', "avg_ppm is incorrect")
        self.assertTrue(result['proj_time'] == '04:19:22', "proj_time is incorrect")
        self.assertTrue(result['run_hhmmss'] == '9:00', "run_hhmmss is incorrect")
        self.assertTrue(result['run_ppm'] == '9:00', "run_ppm is incorrect")
        self.assertTrue(result['walk_hhmmss'] == '1:00', "walk_hhmmss is incorrect")
        self.assertTrue(result['walk_ppm'] == '18:00', "walk_ppm is incorrect")
