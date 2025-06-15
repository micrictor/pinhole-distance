# usb_pinhole.py - Submodule for a USB pinhole camera model off of Amazon
# https://www.amazon.com/SVPRO-Camera-Module-Illumination-Pinhole/dp/B07CF7ZTY1
# Sensor: https://skytech-tv.by/data/SONY_IMX323LQN.pdf

from pinhole_distance.classes import Lens, Sensor, Package

LENS = Lens(
    focal_length_mm=1.8, # 3.6 focal length with F-Stop of 2.0
)

SENSOR = Sensor(
    pixel_width_um=2.8,
    pixel_height_um=2.8,
    resolution=(1920, 1080)
)

PACKAGE = Package(
    lens=LENS,
    sensor=SENSOR
)