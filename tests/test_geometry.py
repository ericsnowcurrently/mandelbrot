
import unittest

from mandelbrot._geometry import Point2D


class Point2DTests(unittest.TestCase):

    def test_from_raw_supported(self):
        tests = {
                None: None,
                Point2D(): None,
                '1,1': Point2D(1, 1),
                1: Point2D(1, 0),
                # 1.0 collids with 1, so we check separately below.
                #1.0: Point2D(1.0, 0),
                1+1j: Point2D(1, 1),
                (1, 1): Point2D(1, 1),
                }
        for raw, expected in tests.items():
            with self.subTest(repr(raw)):
                p = Point2D.from_raw(raw)
                self.assertEqual(p, expected or raw)

        p = Point2D.from_raw(1.0)
        self.assertEqual(p, Point2D(1.0, 0))

    def test_from_raw_unsupported(self):
        tests = [
                '(1,1',
                object(),
                [],
                (1,),
                (1, 1, 1),
                ]
        for raw in tests:
            with self.subTest(repr(raw)):
                with self.assertRaises(ValueError):
                    Point2D.from_raw(raw)

    def test_parse_supported(self):
        tests = {
                '1, 1': Point2D(1, 1),
                '1,1': Point2D(1, 1),
                '(1, 1)': Point2D(1, 1),
                '(1,1)': Point2D(1, 1),
                '[1, 1]': Point2D(1, 1),
                '[1,1]': Point2D(1, 1),
                '1.0,1.0': Point2D(1.0, 1.0),
                '1+1i': Point2D(1, 1),
                '1+1j': Point2D(1, 1),
                '-1,-1': Point2D(-1, -1),
                }
        for raw, expected in tests.items():
            with self.subTest(repr(raw)):
                p = Point2D.parse(raw)
                self.assertEqual(p, expected)

    def test_parse_unsupported(self):
        tests = [
                # malformed pairs
                '(1,1', '1,1)',
                '[1,1', '1,1]',
                # unsupported pairs
                '1 1', '(1 1)', '[1 1]',
                '(,)', '(1,)', '(,1)',
                '(spam,spam)',
                # extra numbers
                '1,1,1',
                # not pairs
                '1',
                '1.0',
                'spam',
                # malformed complex
                '1+1jj', 'x+1j',
                # non-strings
                object(),
                None,
                True, False,
                0, 1, 1.0,
                [1, 1], (1, 1), {1: 1},
                ]
        for raw in tests:
            with self.subTest(repr(raw)):
                with self.assertRaises(ValueError):
                    Point2D.parse(raw)

    def test_parse_empty(self):
        p = Point2D.parse('')

        self.assertEqual(p, Point2D())

    def test_defaults(self):
        x, y = Point2D()

        self.assertEqual(x, 0.0)
        self.assertEqual(y, 0.0)

    def test_coerce_fields_supported(self):
        values = [
                1, 1.0,
                True,
                '1', '1.0',
                ]
        for val in values:
            with self.subTest(repr(val)):
                x, y = Point2D(val, val)

                self.assertEqual(x, 1.0)
                self.assertEqual(y, 1.0)

    def test_coerce_fields_unsupported(self):
        values = [
                '',
                1+1j, '1+1j',
                'spam',
                (), [], {},
                ]
        for val in values:
            with self.subTest(repr(val)):
                exc = ValueError if isinstance(val, str) else TypeError
                with self.assertRaises(exc):
                    Point2D(val, val)

    def test_validation(self):
        with self.assertRaises(TypeError):
            Point2D(None, 1)
        with self.assertRaises(TypeError):
            Point2D(1, None)

    def test_str(self):
        ptstr = str(Point2D(1.0, 1.0))

        self.assertEqual(ptstr, '(1.0, 1.0)')

    def test_imaginary(self):
        for a in [-1, -0.5, 0, 0.5, 1]:
            for b in [-1, -0.5, 0, 0.5, 1]:
                with self.subTest((a, b)):
                    p = Point2D(a, b)
                    c = p.imaginary

                    self.assertEqual(c, a + b * 1j)

    def test_namedtuple(self):
        p = Point2D(1.0, 1.0)
        pair = tuple(v for v in p)
        x, y = p.x, p.y
        fields = p._fields
        p0, p1 = p[0], p[1]

        self.assertEqual(pair, (1.0, 1.0))
        self.assertEqual(x, 1.0)
        self.assertEqual(y, 1.0)
        self.assertEqual(fields, ('x', 'y'))
        self.assertEqual(p0, 1.0)
        self.assertEqual(p1, 1.0)
