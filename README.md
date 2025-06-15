# pinhole-distance

A Python library for pinhole distance calculations.

## Installation

```bash
pip install pinhole-distance
```

## Usage

```python
from pinhole_distance import hello
print(hello())
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

**Example:**
```python
pkg = Package(lens, sensor)
dist = pkg.distance_to_object(actual_dimension=0.2, observed_dimension_px=150)
dimension = pkg.object_dimension_at_distance(distance=1.0, observed_dimension_px=150)
```

## Publishing

- Build: `python -m build`
- Publish: `twine upload dist/*`

## License

MIT
