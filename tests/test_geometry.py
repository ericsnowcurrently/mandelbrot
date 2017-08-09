
import unittest

from mandelbrot._geometry import Grid, Point2D, Area
from mandelbrot._util import Steps


class GridTests(unittest.TestCase):

    def test_fields(self):
        width = Steps(200)
        height = Steps(300)
        grid = Grid(width, height)
        values = grid.width, grid.height

        self.assertEqual(values, (width, height))

    def test_defaults(self):
        width = Steps(200)
        grid = Grid(width)
        height = grid.height

        self.assertEqual(height, width)

    def test_coercion(self):
        tests = {
                2: Steps(2),
                3.1: Steps(3),
                '4': Steps(4),
                }
        for wval, wexpected in tests.items():
            for hval, hexpected in tests.items():
                with self.subTest((wval, hval)):
                    grid = Grid(wval, hval)
                    width, height = grid.width, grid.height

                    self.assertEqual(width, wexpected)
                    self.assertEqual(height, hexpected)

    def test_validation(self):
        with self.assertRaises(TypeError):
            Grid(-1, 3)
        with self.assertRaises(TypeError):
            Grid(3, -1)

    def test_len(self):
        grid = Grid(200, 300)
        size = len(grid)

        self.assertEqual(size, 60501)

    def test_iter(self):
        grid = Grid(4, 5)
        pairs = list(grid)

        self.assertEqual(pairs, [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0),
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
            (0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
            (0, 4), (1, 4), (2, 4), (3, 4), (4, 4),
            (0, 5), (1, 5), (2, 5), (3, 5), (4, 5),
            ])

    def test_reversed(self):
        grid = Grid(4, 5)
        pairs = list(reversed(grid))

        self.assertEqual(pairs, [
            (4, 5), (3, 5), (2, 5), (1, 5), (0, 5),
            (4, 4), (3, 4), (2, 4), (1, 4), (0, 4),
            (4, 3), (3, 3), (2, 3), (1, 3), (0, 3),
            (4, 2), (3, 2), (2, 2), (1, 2), (0, 2),
            (4, 1), (3, 1), (2, 1), (1, 1), (0, 1),
            (4, 0), (3, 0), (2, 0), (1, 0), (0, 0),
            ])

    def test_contains_values(self):
        return
        grid = Grid(640, 480)
        for x in range(-100, 1000):
            for y in range(-50, 500):
                with self.subTest((x, y)):
                    found = (x, y) in grid

                    if x < 0 or y < 0:
                        self.assertFalse(found)
                    elif x > 640 or y > 480:
                        self.assertFalse(found)
                    else:
                        self.assertTrue(found)

    def test_contains_supported(self):
        grid = Grid(10, 10)
        values = [
                (1, 1),
                [1, 1],
                ]
        for value in values:
            with self.subTest(repr(value)):
                found = value in grid

                self.assertTrue(found)

    def test_contains_unsupported(self):
        grid = Grid(10, 10)
        values = [
                object(),
                None,
                1,
                1.0,
                'spam',
                (), [], {},
                (1,),
                ('1', '1'),
                '11',
                ]
        for value in values:
            with self.subTest(repr(value)):
                found = value in grid

                self.assertFalse(found)

    def test_getitem_values(self):
        grid = Grid(5, 10)
        expected = grid.width
        for y in range(-5, 15):
            with self.subTest(y):
                if 0 <= y <= 10:
                    width = grid[y]
                    self.assertEqual(width, expected)
                else:
                    with self.assertRaises(IndexError):
                        grid[y]

    def test_getitem_unsupported(self):
        grid = Grid(10, 10)
        values = [
                (1, 1),
                object(),
                None,
                'spam',
                ]
        for value in values:
            with self.subTest(repr(value)):
                with self.assertRaises(IndexError):
                    grid[value]

    def test_iter_floats(self):
        grid = Grid(4, 7)
        floats = list(grid.iter_floats(-0.1, 0.9, 2.5, -1.0))

        self.assertEqual(floats, [
            (-0.1, 2.5), (0.15, 2.5), (0.40, 2.5), (0.65, 2.5), (0.9, 2.5),
            (-0.1, 2.0), (0.15, 2.0), (0.40, 2.0), (0.65, 2.0), (0.9, 2.0),
            (-0.1, 1.5), (0.15, 1.5), (0.40, 1.5), (0.65, 1.5), (0.9, 1.5),
            (-0.1, 1.0), (0.15, 1.0), (0.40, 1.0), (0.65, 1.0), (0.9, 1.0),
            (-0.1, 0.5), (0.15, 0.5), (0.40, 0.5), (0.65, 0.5), (0.9, 0.5),
            (-0.1, 0.0), (0.15, 0.0), (0.40, 0.0), (0.65, 0.0), (0.9, 0.0),
            (-.1, -0.5), (.15, -0.5), (.40, -0.5), (.65, -0.5), (.9, -0.5),
            (-.1, -1.0), (.15, -1.0), (.40, -1.0), (.65, -1.0), (.9, -1.0),
            ])

    def test_iter_points(self):
        start = Point2D(1, 2)
        end = Point2D(3, -2)
        grid = Grid(4, 4)
        points = list(grid.iter_points(start, end))

        P = Point2D
        self.assertEqual(points, [
            P(1, 2), P(1.5, 2), P(2, 2), P(2.5, 2), P(3, 2),
            P(1, 1), P(1.5, 1), P(2, 1), P(2.5, 1), P(3, 1),
            P(1, 0), P(1.5, 0), P(2, 0), P(2.5, 0), P(3, 0),
            P(1, -1), P(1.5, -1), P(2, -1), P(2.5, -1), P(3, -1),
            P(1, -2), P(1.5, -2), P(2, -2), P(2.5, -2), P(3, -2),
            ])


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


class AreaTests(unittest.TestCase):

    MIN = Point2D(-1, -1)
    MAX = Point2D(1, 1)

    def test_from_radius(self):
        Area.from_radius()

    def test_from_sides(self):
        # Note that MAX.x was passed as x1.
        area = Area.from_sides(self.MAX.x, self.MIN.x, self.MIN.y, self.MAX.y)
        pmin, pmax = area.min, area.max

        self.assertEqual(pmin, self.MIN)
        self.assertEqual(pmax, self.MAX)

    def test_reorder(self):
        area1 = Area(self.MIN, self.MAX)
        area2 = Area(self.MAX, self.MIN)

        self.assertEqual(area1, area2)

    def test_coerce_tuples(self):
        area = Area(tuple(self.MIN), tuple(self.MAX))
        pmin, pmax = area

        self.assertEqual(pmin, self.MIN)
        self.assertEqual(pmax, self.MAX)

    def test_coerce_strings(self):
        area = Area(str(self.MIN), str(self.MAX))
        pmin, pmax = area

        self.assertEqual(pmin, self.MIN)
        self.assertEqual(pmax, self.MAX)

    def test_namedtuple(self):
        area = Area(self.MIN, self.MAX)
        triple = tuple(v for v in area)
        pmin, pmax = area.min, area.max
        fields = area._fields
        a0, a1 = area[0], area[1]

        self.assertEqual(triple, (self.MIN, self.MAX))
        self.assertEqual(pmin, self.MIN)
        self.assertEqual(pmax, self.MAX)
        self.assertEqual(fields, ('min', 'max'))
        self.assertEqual(a0, self.MIN)
        self.assertEqual(a1, self.MAX)
