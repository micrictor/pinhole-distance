# fake_flat.py - Submodule for a fake flat camera model
# This defines a simple camera package with no lens and a flat 100x100 pixel sensor,
# where each pixel is 1m x 1m in size for testing purposes.

from pinhole_distance.classes import Lens, Sensor, Package

LENS = Lens(
    focal_length_mm=1e3,  # Focal length of 1000 mm (1 meter)
)

SENSOR = Sensor(
    pixel_width_um=1e6,  # 1 meter per pixel
    pixel_height_um=1e6,  # 1 meter per pixel
    resolution=(100, 100)
)

PACKAGE = Package(
    lens=LENS,
    sensor=SENSOR
)