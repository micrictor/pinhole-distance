# rpi_cam_2.py - Submodule for the Raspberry Pi Camera 2
# https://www.sparkfun.com/raspberry-pi-camera-module-v2.html
# https://www.raspberrypi.com/documentation/accessories/camera.html#hardware-specification
# Datasheet: https://cdn.sparkfun.com/datasheets/Dev/RaspberryPi/RPiCamMod2.pdf

from pinhole_distance.classes import Lens, Sensor, Package

LENS = Lens(
    focal_length_mm=3.04,
)

SENSOR = Sensor(
    pixel_width_um=1.12,
    pixel_height_um=1.12,
    resolution=(3280, 2464)
)

PACKAGE = Package(
    lens=LENS,
    sensor=SENSOR
)