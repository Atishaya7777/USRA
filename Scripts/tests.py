import unittest
from visualize import Point, PointConfiguration


class TestPoint(unittest.TestCase):

    def test_point_initialization(self):
        point = Point(5)
        self.assertEqual(point.position, 5)

    def test_point_repr(self):
        point = Point(10)
        self.assertEqual(repr(point), "Point is at 10")

    def test_point_equality(self):
        point1 = Point(5)
        point2 = Point(10)
        self.assertNotEqual(point1, point2)

    def test_point_invalid_position(self):
        with self.assertRaises(ValueError):
            Point(-5)


class TestPointConfiguration(unittest.TestCase):

    def test_configuration_initialization(self):
        config = PointConfiguration(10, {1, 2, 3})
        self.assertEqual(config.n, 10)
        self.assertEqual(config.distances, {1, 2, 3})
        self.assertEqual(config.configurations, [])

    def test_generate_config_valid_case(self):
        config = PointConfiguration(10, {1, 2})
        success = config.generate_config()
        self.assertTrue(success)
        self.assertGreater(len(config.configurations), 0)

    def test_generate_config_invalid_case(self):
        config = PointConfiguration(10, {5, 6})
        success = config.generate_config()
        self.assertFalse(success)

    def test_is_valid_with_valid_configuration(self):
        config = PointConfiguration(10, {1, 2})
        config.configurations = [
            [Point(1), Point(3), Point(6), Point(9)]]
        self.assertTrue(config.is_valid())

    def test_is_valid_with_invalid_configuration(self):
        config = PointConfiguration(10, {1, 3})
        config.configurations = [[Point(1), Point(4), Point(7)]]
        self.assertFalse(config.is_valid())

    def test_generate_config_edge_case(self):
        config = PointConfiguration(1, {1})
        success = config.generate_config()
        self.assertFalse(success)

    def test_generate_config_with_large_input(self):
        config = PointConfiguration(100, {1, 2, 3, 4})
        success = config.generate_config()
        self.assertTrue(success)
        self.assertGreater(len(config.configurations), 0)

    def test_generate_config_empty_distances(self):
        config = PointConfiguration(10, set())
        success = config.generate_config()
        self.assertFalse(success)

    def test_repr(self):
        config = PointConfiguration(10, {1, 2, 3})
        self.assertEqual(repr(config), "PointConfiguration([])")

    def test_is_valid_when_no_configurations(self):
        config = PointConfiguration(10, {1, 2, 3})
        config.generate_config()
        self.assertFalse(config.is_valid())


if __name__ == "__main__":
    unittest.main()
