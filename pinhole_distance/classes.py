from typing import Optional, Dict, Tuple

class DistortionTable(dict):
    def __init__(self, *args, rounding_precision: float = 0, **kwargs):
        """
        A dictionary that maps field  to distortion correction factor, with optional rounding of keys.

        Args:
            rounding_precision (float): The precision to which keys should be rounded. Default is 0 (no rounding). For example, a value of 0.01 will round keys to the nearest 0.01.
            *args: Positional arguments for the base dict.
            **kwargs: Keyword arguments for the base dict.
        """
        super().__init__(*args, **kwargs)
        self._rounding_precision = rounding_precision

    def __getitem__(self, key: float) -> float:
        if not self._rounding_precision or self._rounding_precision == 0:
            return super().__getitem__(key)
        rounding_factor = int(1 / self._rounding_precision)
        rounded_key = round(key * rounding_factor) / rounding_factor
        return super().__getitem__(rounded_key)

    def get(self, key: float, default=None) -> float:
        if not self._rounding_precision or self._rounding_precision == 0:
            return super().get(key, default)
        rounding_factor = int(1 / self._rounding_precision)
        rounded_key = round(key * rounding_factor) / rounding_factor
        return super().get(rounded_key, default)

class Lens:
    def __init__(self, focal_length_mm: float, distortion_table: Optional[DistortionTable] = None):
        """
        Args:
            focal_length_mm (float): Focal length of the lens in millimeters.
            distortion_table (Optional[DistortionTable]): Optional mapping of observed radius to distortion correction factor.
        """
        self.focal_length = focal_length_mm
        self.distortion_table = distortion_table

class Sensor:
    def __init__(self, pixel_width_um: float, pixel_height_um: float, resolution: Tuple[int, int]):
        """
        Args:
            pixel_width_um (float): Width of a single pixel in micrometers (μm). In most cases, this is the same for both dimensions.
            pixel_height_um (float): Height of a single pixel in micrometers (μm). In most cases, this is the same for both dimensions.
            resolution (tuple): (width_px, height_px)
        """
        self.pixel_width_um = pixel_width_um
        self.pixel_height_um = pixel_height_um
        self.resolution = resolution

class Package:
    def __init__(self, lens: Lens, sensor: Sensor):
        self.lens = lens
        self.sensor = sensor

    def calculate_percent_distortion(self, dimension: str, center_px: Tuple[int, int]) -> float:
        """
        Calculate the percent distortion for a given dimension and center pixel.
        Args:
            dimension (str): 'x', 'w', 'y', or 'h'.
            center_px (tuple): (x, y) pixel coordinates of the object's center.
        Returns:
            float: Percent distortion (0.0 to 1.0)
        """
        res_x, res_y = self.sensor.resolution
        image_center_x = res_x / 2
        image_center_y = res_y / 2
        center_x, center_y = center_px
        delta_x = abs(center_x - image_center_x)
        delta_y = abs(center_y - image_center_y)
        max_delta = image_center_x if dimension in ['x', 'w'] else image_center_y
        if max_delta == 0:
            raise ValueError("Invalid sensor resolution, cannot calculate distortion.")
        if dimension in ['x', 'w']:
            return delta_x / max_delta if delta_x != 0 else 0.0
        else:
            return delta_y / max_delta if delta_y != 0 else 0.0

    def distance_to_object(self, dimension: str, actual_dimension: float, observed_dimension_px: float, center_px: Optional[Tuple[int, int]] = None) -> float:
        """
        Calculate the distance to an object using the pinhole camera model.
        Args:
            dimension (str): The dimension to use for the calculation. Must be one of 'x', 'y', 'h', or 'w':
                - 'x' or 'w': Use the horizontal (width) dimension.
                - 'y' or 'h': Use the vertical (height) dimension.
            actual_dimension (float): The real-world size of the object along the specified dimension (in meters).
            observed_dimension_px (float): The size of the object as observed in the image (in pixels) along the specified dimension.
            center_px (tuple): The pixel coordinates of the center of the object in the image, required for use of a distortion table. Default is None.
        Returns:
            float: The estimated distance to the object (in meters).
        """
        pixel_dim_m = self.sensor.pixel_width_um * 1e-6 if dimension in ['x', 'w'] else self.sensor.pixel_height_um * 1e-6
        focal_length_m = self.lens.focal_length * 1e-3
        distance = (actual_dimension * focal_length_m) / (observed_dimension_px * pixel_dim_m)
        if self.lens.distortion_table and center_px:
            percent_distortion = self.calculate_percent_distortion(dimension, center_px)
            if percent_distortion == 0:
                return distance
            distortion_factor = self.lens.distortion_table.get(percent_distortion, 1.0)
            return distance * (1 + distortion_factor)
        return distance

    def object_dimension_at_distance(self, dimension: str, distance: float, observed_dimension_px: float, center_px: Optional[Tuple[int, int]] = None) -> float:
        """
        Calculate the actual dimension of an object at a given distance (in meters), given its observed dimension (in pixels).
        Args:
            dimension (str): The dimension to use for the calculation. Must be one of 'x', 'y', 'h', or 'w'.
            distance (float): The distance to the object (in meters).
            observed_dimension_px (float): The size of the object as observed in the image (in pixels) along the specified dimension.
        Returns:
            float: The estimated actual dimension (in meters).
        """
        pixel_dim_m = self.lens.pixel_width_um * 1e-6 if dimension in ['x', 'w'] else self.sensor.pixel_height_um * 1e-6
        focal_length_m = self.lens.focal_length * 1e-3
        actual_dimension = (distance * observed_dimension_px * pixel_dim_m) / focal_length_m
        if self.lens.distortion_table and center_px:
            percent_distortion = self.calculate_percent_distortion(dimension, center_px)
            if percent_distortion == 0:
                return actual_dimension
            distortion_factor = self.lens.distortion_table.get(percent_distortion, 1.0)
            return actual_dimension * (1 + distortion_factor)
        return actual_dimension
