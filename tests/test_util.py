
import unittest

from mandelbrot._util import Steps


class StepsTests(unittest.TestCase):

    def test_int(self):
        steps = Steps(3)

        isinstance(steps, int)

    def test_new_noop(self):
        orig = Steps(3)
        steps = Steps(orig)

        self.assertIs(steps, orig)

    def test_new_coercion(self):
        values = [3, 3.1, '3']
        for value in values:
            with self.subTest(repr(value)):
                steps = Steps(value)

                self.assertEqual(steps, 3)

    def test_new_unsupported_num(self):
        values = [1+1j]
        for value in values:
            with self.subTest(repr(value)):
                with self.assertRaises(TypeError):
                    Steps(value)

    def test_new_bad_num(self):
        with self.assertRaises(TypeError):
            Steps(object())
        with self.assertRaises(ValueError):
            Steps('')

    def test_validation(self):
        with self.assertRaises(TypeError):
            Steps(-1)

    def test_len(self):
        steps0 = Steps(0)
        size0 = len(steps0)
        steps3 = Steps(3)
        size3 = len(steps3)

        self.assertEqual(size0, 1)
        self.assertEqual(size3, 4)

    def test_iter(self):
        steps = Steps(3)
        values = list(steps)

        self.assertEqual(values, [0, 1, 2, 3])

    def test_reversed(self):
        steps = Steps(3)
        values = list(reversed(steps))

        self.assertEqual(values, [3, 2, 1, 0])

    def test_contains_values(self):
        steps = Steps(3)
        for i in range(4):
            with self.subTest(i):
                contained = (i in steps)
                self.assertTrue(contained)
        contained = (-1 in steps)
        self.assertFalse(contained)
        contained = (4 in steps)
        self.assertFalse(contained)

    def test_contains_unsupported(self):
        steps = Steps(3)
        values = [
                None,
                object(),
                'spam',
                '1',
                ]
        for value in values:
            with self.subTest(repr(value)):
                found = value in steps

                self.assertFalse(found)

    def test_range_no_start_no_stop_no_step(self):
        steps = Steps(3)
        r = steps.range()

        self.assertEqual(r, range(4))
        self.assertEqual(len(r), len(steps))

    def test_range_no_start_no_stop_step(self):
        steps = Steps(3)
        r_inc = steps.range(step=2)
        r_dec = steps.range(step=-2)

        self.assertEqual(r_inc, range(0, 8, 2))
        self.assertEqual(len(r_inc), len(steps))
        self.assertEqual(r_dec, range(0, -8, -2))
        self.assertEqual(len(r_dec), len(steps))

    def test_range_no_start_stop_no_step(self):
        steps = Steps(3)
        r1 = steps.range(stop=3)
        r2 = steps.range(stop=-3)

        self.assertEqual(r1, range(-1, 3, 1))
        self.assertEqual(len(r1), len(steps))
        self.assertEqual(r2, range(-7, -3, 1))
        self.assertEqual(len(r2), len(steps))

    def test_range_no_start_stop_step(self):
        steps = Steps(3)
        r_inc = steps.range(stop=3, step=2)
        r_dec = steps.range(stop=3, step=-2)

        self.assertEqual(r_inc, range(-5, 3, 2))
        self.assertEqual(len(r_inc), len(steps))
        self.assertEqual(r_dec, range(11, 3, -2))
        self.assertEqual(len(r_dec), len(steps))

    def test_range_start_no_stop_no_step(self):
        steps = Steps(3)
        r = steps.range(start=4)

        self.assertEqual(r, range(4, 8, 1))
        self.assertEqual(len(r), len(steps))

    def test_range_start_no_stop_step(self):
        steps = Steps(3)
        r = steps.range(start=4, step=2)

        self.assertEqual(r, range(4, 12, 2))
        self.assertEqual(len(r), len(steps))

    def test_range_start_stop_no_step_valid(self):
        steps = Steps(3)
        start = 2

        tests = {
                -5: [-18, -17, -16],
                -4: [-15, -14, -13],
                -3: [-12, -11, -10],
                -2: [-8, -7],
                -1: [-4],
                1: [4],
                2: [7, 8],
                3: [10, 11, 12],
                4: [13, 14, 15],
                5: [16, 17, 18],
                }
        for step in sorted(tests):
            for stop in tests[step]:
                stop += start
                with self.subTest((start, stop, step)):
                    r = steps.range(start=start, stop=stop)
                    self.assertEqual(r, range(start, stop, step))
                    self.assertEqual(len(r), len(steps))

    def test_range_start_stop_no_step_invalid(self):
        steps = Steps(3)
        start = 2

        invalid = [
                -9,
                -6, -5,
                -3, -2, -1,
                0,
                1, 2, 3,
                5, 6,
                9,
                ]
        for stop in invalid:
            stop += start
            with self.subTest((start, stop)):
                with self.assertRaises(ValueError):
                    steps.range(start=start, stop=stop)

    def test_range_start_stop_step(self):
        steps = Steps(3)
        start = 2
        tests = {
                -4: {-16, -15, -14, -13},
                -3: {-12, -11, -10},
                -2: {-8, -7},
                -1: {-4},
                0: {},
                1: {4},
                2: {7, 8},
                3: {10, 11, 12},
                4: {13, 14, 15, 16},
                }
        for step in sorted(tests):
            validstops = tests[step]
            for base in range(-20, 21):
                stop = base + start
                with self.subTest((start, stop, step)):
                    if base in validstops:
                        r = steps.range(start=start, stop=stop, step=step)
                        self.assertEqual(r, range(start, stop, step))
                        self.assertEqual(len(r), len(steps))
                    else:
                        with self.assertRaises(ValueError):
                            steps.range(start=start, stop=stop, step=step)

    def test_iter_floats_increasing(self):
        steps = Steps(3)
        values = list(steps.iter_floats(0.0, 1.0))

        self.assertEqual(values, [0.0, 1/3, 2/3, 1.0])

    def test_iter_floats_decreasing(self):
        steps = Steps(7)
        values = list(steps.iter_floats(2.5, -1.0))

        self.assertEqual(values, [2.5, 2.0, 1.5, 1.0, 0.5, 0.0, -0.5, -1.0])
