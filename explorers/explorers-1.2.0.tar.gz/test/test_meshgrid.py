from __future__ import absolute_import, division, print_function
import unittest
import random

import dotdot
from explorers import MeshGrid


random.seed(0)


class TestMeshGrid(unittest.TestCase):

    def test_meshgrid1D(self):
        cfg = None
        mesh = MeshGrid({'res': 10}, ((0, 1),))
        for _ in range(10000):
            mesh.add((random.random(),))

        self.assertEqual(len(mesh._nonempty_bins), 10)

        mesh2 = MeshGrid({'res': 10}, ((0, 1),))
        for _ in range(1000):
            mesh2.add(mesh.draw(replace=True))

        for b in mesh2._nonempty_bins:
            self.assertTrue(80 <= len(b) <= 120)

        mesh3 = MeshGrid({'res': 10}, ((0, 1),))
        for _ in range(1000):
            mesh3.add(mesh.draw(replace=False))

        for b in mesh3._nonempty_bins:
            self.assertTrue(80 <= len(b) <= 120)

        self.assertEqual(len(mesh._nonempty_bins), 10)

    def test_meshgrid2D(self):
        cfg = None
        bounds = ((-30, -20), (4, 5))
        res = 15

        mesh = MeshGrid({'res': res}, bounds)
        for _ in range(10000):
            mesh.add((random.uniform(*bounds[0]),
                      random.uniform(*bounds[1])))

        self.assertEqual(len(mesh._nonempty_bins), res**2)

        res2 = 10
        mesh2 = MeshGrid({'res': res2}, bounds)
        for _ in range(1000):
            mesh2.add(mesh.draw(replace=True))

        self.assertEqual(len(mesh2._nonempty_bins), res2**2)

    def test_meshgrid_outliers(self):
        cfg = None
        bounds = ((0, 1),)
        res = 15

        mesh = MeshGrid({'res': res}, bounds)
        for _ in range(1000):
            mesh.add(( random.uniform(*bounds[0]),))
        for _ in range(1000):
            mesh.add((-random.uniform(*bounds[0]),))

        self.assertEqual(len(mesh._nonempty_bins), res+1)

        res2 = 10
        mesh2 = MeshGrid({'res': res2}, bounds)
        for _ in range(100):
            mesh2.add(mesh.draw(replace=True))

        for b in mesh2._nonempty_bins:
            self.assertTrue(3 < len(b) < 20)
        self.assertEqual(len(mesh2._nonempty_bins), res2+1)

    def test_resize(self):
        cfg = None
        bounds = ((0, 1),)
        res = 15

        mesh = MeshGrid({'res': res}, bounds)
        for _ in range(1000):
            mesh.add(( random.uniform(*bounds[0]),))

        self.assertEqual(len(mesh._nonempty_bins), res)

        res = 10
        mesh.resize(((0, 1),), res=res)
        self.assertEqual(len(mesh._nonempty_bins), res)

        mesh.resize(((0, 2),), res=res)
        self.assertEqual(len(mesh._nonempty_bins), res/2)


if __name__ == '__main__':
    unittest.main()
