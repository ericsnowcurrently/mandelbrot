
import unittest

from mandelbrot._mandelbrot import iter_mandelbrot


class IterMandelbrotTests(unittest.TestCase):

    def test_basic(self):
        candidates = [0.1j * i for i in range(10)]
        candidates.extend([c + 1 for c in candidates])
        mandelbrot = [(c.real + int(c.imag * 10) / 10 * 1j, i)
                      for c, i in iter_mandelbrot(candidates)]

        self.assertEqual(mandelbrot, [
            (0j, None),
            (0.1j, None),
            (0.2j, None),
            (0.3j, None),
            (0.4j, None),
            (0.5j, None),
            (0.6j, None),
            (0.7j, 12),
            (0.8j, 17),
            (0.9j, 7),
            (1+0j, 2),
            (1+0.1j, 1),
            (1+0.2j, 1),
            (1+0.3j, 1),
            (1+0.4j, 1),
            (1+0.5j, 1),
            (1+0.6j, 1),
            (1+0.7j, 1),
            (1+0.8j, 1),
            (1+0.9j, 1),
            ])

    def test_full(self):
        candidates = [0.1j * i for i in range(10)]
        candidates.extend([c + 1 for c in candidates])
        maxiter = 2
        mandelbrot = [(c.real + int(c.imag * 10) / 10 * 1j, i)
                      for c, i in iter_mandelbrot(candidates, maxiter)]

        self.assertEqual(mandelbrot, [
            (0j, None),
            (0.1j, None),
            (0.2j, None),
            (0.3j, None),
            (0.4j, None),
            (0.5j, None),
            (0.6j, None),
            (0.7j, None),
            (0.8j, None),
            (0.9j, None),
            (1+0j, None),
            (1+0.1j, 1),
            (1+0.2j, 1),
            (1+0.3j, 1),
            (1+0.4j, 1),
            (1+0.5j, 1),
            (1+0.6j, 1),
            (1+0.7j, 1),
            (1+0.8j, 1),
            (1+0.9j, 1),
            ])

    def test_no_candidates(self):
        mandelbrot = list(iter_mandelbrot([]))

        self.assertEqual(mandelbrot, [])

    def test_noniterable_candidates(self):
        with self.assertRaises(TypeError):
            list(iter_mandelbrot(0j))

    def test_invalid_candidate(self):
        with self.assertRaises(TypeError):
            list(iter_mandelbrot(['0j']))

    def test_invalid_maxiter(self):
        maxiter = object()
        with self.assertRaises(TypeError):
            list(iter_mandelbrot([0j], maxiter))
