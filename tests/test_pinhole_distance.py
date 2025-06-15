import unittest
from pinhole_distance.classes import Lens, Sensor, Package, DistortionTable

class TestPinholeDistance(unittest.TestCase):
    def test_distance_to_object(self):
        """
        Test the distance to object calculation using the pinhole camera model.
        Based on https://math.stackexchange.com/questions/3739230/calculate-the-distance-to-an-object-through-a-pinhole-camera-2-approaches
        """
        lens = Lens(focal_length_mm=15)
        sensor = Sensor(pixel_width_um=150, pixel_height_um=150, resolution=(27, 26))
        pkg = Package(lens, sensor)
        result = pkg.distance_to_object('y', actual_dimension=1.5, observed_dimension_px=10)
        self.assertAlmostEqual(result, 15.0, places=6)

    def test_object_height(self):
        """
        Test the object height calculation using the pinhole camera model.
        Based on https://math.stackexchange.com/questions/3739230/calculate-the-distance-to-an-object-through-a-pinhole-camera-2-approaches
        """
        lens = Lens(focal_length_mm=15)
        sensor = Sensor(pixel_width_um=150, pixel_height_um=150, resolution=(27, 26))
        pkg = Package(lens, sensor)
        result = pkg.object_dimension_at_distance('y', distance=15.0, observed_dimension_px=10)
        self.assertAlmostEqual(result, 1.5, places=6)

    def test_distortion_table_no_rounding(self):
        table = DistortionTable({10.0: 0.95, 20.0: 0.9}, rounding_precision=0)
        self.assertEqual(table[10.0], 0.95)
        self.assertEqual(table.get(20.0), 0.9)
        self.assertEqual(table.get(15.0, 1.0), 1.0)  # Not present, returns default

    def test_distortion_table_with_rounding(self):
        table = DistortionTable({10.15: 0.95, 20.55: 0.9}, rounding_precision=0.05)
        self.assertEqual(table[10.17], 0.95)  # 10.17 rounds to 10.15
        self.assertEqual(table.get(20.53), 0.9)  # 20.53 rounds to 20.55
        self.assertEqual(table.get(15.0, 1.0), 1.0)  # Not present, returns default

    def test_distance_to_object_with_distortion(self):
        """
        Test the distance to object calculation using the pinhole camera model.
        Based on https://math.stackexchange.com/questions/3739230/calculate-the-distance-to-an-object-through-a-pinhole-camera-2-approaches
        """
        distortion_table = DistortionTable({0: 0, 0.5: 1, 1: 2}, rounding_precision=0.5)
        lens = Lens(focal_length_mm=15, distortion_table=distortion_table)
        sensor = Sensor(pixel_width_um=150, pixel_height_um=150, resolution=(100, 100))
        pkg = Package(lens, sensor)
        # No distortion - center of the image
        result = pkg.distance_to_object('y', actual_dimension=1.5, observed_dimension_px=10, center_px=(50, 50))
        self.assertAlmostEqual(result, 15.0, places=6)

        # With distortion - 50% to the right of center
        result = pkg.distance_to_object('y', actual_dimension=1.5, observed_dimension_px=10, center_px=(50, 75))
        self.assertAlmostEqual(result, 15.0 * (1 + 1), places=6)

        # With distortion - 100% to the right of center
        result = pkg.distance_to_object('y', actual_dimension=1.5, observed_dimension_px=10, center_px=(50, 100))
        self.assertAlmostEqual(result, 15.0 * (1 + 2), places=6)

    def test_object_height_with_distortion(self):
        """
        Test the object height calculation using the pinhole camera model with a distortion table.
        """
        distortion_table = DistortionTable({0: 0, 0.5: 1, 1: 2}, rounding_precision=0.5)
        lens = Lens(focal_length_mm=15, distortion_table=distortion_table)
        sensor = Sensor(pixel_width_um=150, pixel_height_um=150, resolution=(100, 100))
        pkg = Package(lens, sensor)
        # No distortion - center of the image
        result = pkg.object_dimension_at_distance('y', distance=15.0, observed_dimension_px=10, center_px=(50, 50))
        self.assertAlmostEqual(result, 1.5, places=6)

        # With distortion - 50% to the right of center (should apply factor 1)
        # The distortion factor is applied as (1 + distortion_factor)
        # So expected = 1.5 * (1 + 1) = 3.0
        result = pkg.object_dimension_at_distance('y', distance=15.0, observed_dimension_px=10, center_px=(50, 75))
        self.assertAlmostEqual(result, 3.0, places=6)

        # With distortion - 100% to the right of center (should apply factor 2)
        result = pkg.object_dimension_at_distance('y', distance=15.0, observed_dimension_px=10, center_px=(50, 100))
        self.assertAlmostEqual(result, 4.5, places=6)
