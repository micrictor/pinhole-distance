# pinhole-distance

A Python library for calculating the distance to an observed object in an
image, given that you know, for either height (y) or width (x):

*   The actual measurement of the object, in meters.
*   The observed measurement of the object, in pixels.
    *   Most readily determined using an object recognition model like YOLO
        and using the measurements of the bounding box.

This module has pre-defined classes for doing these calculations for:

*   `ov5647` - [Arducam 5MP 120 degree camera](https://www.arducam.com/b006604-arducam-for-raspberry-pi-zero-camera-module-wide-angle-120-1-4-inch-5mp-ov5647-spy-camera-with-flex-cable-for-pi-zero-and-pi-compute-module.html)
    *   Module compensates for the "fish-eye" effect, where images closer to the edge of the FOV will have the observed dimension distorted
*   `rpi_cam_2` - [Raspberry Pi Camera Module 2](https://www.sparkfun.com/raspberry-pi-camera-module-v2.html)
*   `usb_pinhole` - [SVPRO 3.7mm Pinhole Lens USB Camera](https://www.amazon.com/SVPRO-Camera-Module-Illumination-Pinhole/dp/B07CF7ZTY1)

Users can also define their own camera packages using the `Sensor`, `Lens`, and `Package` classes.

## Installation

```bash
pip install pinhole-distance
```

## Usage

```python
# Calculate the distance to an object known to be 21" wide that is 70px wide in the image
# Assumes you're using the USB pinhole camera defined in usb_pinhole.py
from pinhole_distance import usb_pinhole

distance = usb_pinhole.distance_to_object(
    dimension='x',
    actual_dimension=0.5334,
    observed_dimension_px=70
)
print(f"Distance to object: {distance:.4f} meters")
```

## API Reference

### class Lens
Represents a camera lens.

**Attributes:**
- `focal_length` (float): Focal length of the lens in millimeters.
- `pixel_width_um` (float): Width of a single pixel in micrometers (μm).
- `distortion_table` (Optional[dict[float, float]]): Optional mapping of observed radius (pixels or mm) to distortion correction factor (for fisheye lenses).

**Example:**
```python
lens = Lens(focal_length=4.0, pixel_width_um=1.4, distortion_table={0.0: 1.0, 100.0: 0.98})
```

---

### class Sensor
Represents a camera sensor.

**Attributes:**
- `pixel_height_um` (float): Height of a single pixel in micrometers (μm).
- `resolution` (tuple[int, int]): Sensor resolution as (width_px, height_px).

**Example:**
```python
sensor = Sensor(pixel_height_um=1.4, resolution=(1920, 1080))
```

---

### class Package
Combines a `Lens` and a `Sensor` for distance and dimension calculations.

**Attributes:**
- `lens` (Lens): The lens used.
- `sensor` (Sensor): The sensor used.

**Methods:**
- `distance_to_object(actual_dimension: float, observed_dimension_px: float) -> float`  
  Returns the distance (in meters) to an object given its actual dimension (height or width, in meters) and observed dimension in the image.
- `object_dimension_at_distance(distance: float, observed_dimension_px: float) -> float`  
  Returns the actual dimension (in meters) of an object at a given distance (in meters), given its observed dimension in the image.


The output is a distance of 4.8986 meters, or roughly a 2% error.

## License

MIT
