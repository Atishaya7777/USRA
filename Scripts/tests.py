import unittest
from visualize import Point, PointConfiguration


class TestPoint(unittest.TestCase):

    def test_point_initialization(self):
        point = Point(5)
        self.assertEqual(point.position, 5)

    def test_point_repr(self):
        point = Point(10)
        self.assertEqual(repr(point), "10")

    def test_point_equality(self):
        point1 = Point(5)
        point2 = Point(10)
        self.assertNotEqual(point1, point2)

    def test_point_invalid_position(self):
        with self.assertRaises(ValueError):
            Point(-5)


class TestPointConfiguration(unittest.TestCase):

    def test_basic_generation(self):
        config = PointConfiguration(5, {1, 2})
        has_config = config.generate_config()
        self.assertTrue(has_config)
        self.assertTrue(all(isinstance(p, list)
                        for p in config.configurations))
        self.assertGreater(len(config.configurations), 0)

    def test_all_distances_used(self):
        config = PointConfiguration(6, {1, 2})
        config.generate_config()
        for path in config.configurations:
            diffs = [path[i].position -
                     (path[i-1].position if i > 0 else 0) for i in range(len(path))]
            self.assertTrue({1, 2}.issubset(set(diffs)))

    def test_generate_with_large_distance(self):
        config = PointConfiguration(10, {1, 2, 4})
        has_config = config.generate_config()
        self.assertTrue(has_config)
        for path in config.configurations:
            diffs = [path[i].position -
                     (path[i-1].position if i > 0 else 0) for i in range(len(path))]
            self.assertTrue({1, 2, 4}.issubset(set(diffs)))


if __name__ == "__main__":
    unittest.main()
