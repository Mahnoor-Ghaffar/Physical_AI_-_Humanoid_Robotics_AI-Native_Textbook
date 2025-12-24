"""
DomainRandomizationParams model for Isaac Robot Brain
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class DomainRandomizationParams:
    """
    Configuration for domain randomization during synthetic data generation
    """

    def __init__(self,
                 lighting_variation: Optional[Dict[str, float]] = None,
                 texture_randomization: bool = True,
                 environment_objects: Optional[Dict[str, Any]] = None,
                 sensor_noise: Optional[Dict[str, float]] = None,
                 effectiveness_metric: float = 0.0):
        """
        Initialize DomainRandomizationParams instance

        Args:
            lighting_variation: Range of lighting conditions (min/max values)
            texture_randomization: Whether to randomize textures and materials
            environment_objects: Random object placement configuration
            sensor_noise: Simulated sensor noise parameters (mean, std)
            effectiveness_metric: Sim-to-real transfer improvement metric
        """
        # Validate lighting variation parameters
        if lighting_variation:
            if not all(k in ['min', 'max'] for k in lighting_variation.keys()):
                raise ValueError("Lighting variation must have 'min' and 'max' keys")
            if lighting_variation.get('min', 0) < 0 or lighting_variation.get('max', 1) < 0:
                raise ValueError("Lighting variation values must be non-negative")
            if lighting_variation.get('min', 0) > lighting_variation.get('max', 1):
                raise ValueError("Lighting min value cannot be greater than max value")

        # Validate sensor noise parameters
        if sensor_noise:
            if sensor_noise.get('mean', 0) < 0:
                raise ValueError("Sensor noise mean must be non-negative")
            if sensor_noise.get('std', 0) < 0:
                raise ValueError("Sensor noise std must be non-negative")

        if effectiveness_metric < 0:
            raise ValueError("Effectiveness metric must be non-negative")

        self.lighting_variation = lighting_variation or {'min': 0.5, 'max': 1.5}
        self.texture_randomization = texture_randomization
        self.environment_objects = environment_objects or {}
        self.sensor_noise = sensor_noise or {'mean': 0.0, 'std': 0.1}
        self.effectiveness_metric = effectiveness_metric

    def validate(self) -> bool:
        """
        Validate the domain randomization parameters

        Returns:
            True if valid, False otherwise
        """
        # Check lighting variation
        if self.lighting_variation:
            if not all(k in ['min', 'max'] for k in self.lighting_variation.keys()):
                return False
            if self.lighting_variation.get('min', 0) < 0 or self.lighting_variation.get('max', 1) < 0:
                return False
            if self.lighting_variation.get('min', 0) > self.lighting_variation.get('max', 1):
                return False

        # Check sensor noise
        if self.sensor_noise:
            if self.sensor_noise.get('mean', 0) < 0 or self.sensor_noise.get('std', 0) < 0:
                return False

        # Check effectiveness metric
        if self.effectiveness_metric < 0:
            return False

        return True

    def get_params_dict(self) -> Dict[str, Any]:
        """
        Get the parameters as a dictionary

        Returns:
            Dictionary with all parameters
        """
        return {
            'lighting_variation': self.lighting_variation,
            'texture_randomization': self.texture_randomization,
            'environment_objects': self.environment_objects,
            'sensor_noise': self.sensor_noise,
            'effectiveness_metric': self.effectiveness_metric
        }

    def update_params(self, **kwargs):
        """
        Update parameters with new values

        Args:
            **kwargs: Parameters to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                if key == 'lighting_variation' and value:
                    if not all(k in ['min', 'max'] for k in value.keys()):
                        raise ValueError("Lighting variation must have 'min' and 'max' keys")
                    if value.get('min', 0) < 0 or value.get('max', 1) < 0:
                        raise ValueError("Lighting variation values must be non-negative")
                    if value.get('min', 0) > value.get('max', 1):
                        raise ValueError("Lighting min value cannot be greater than max value")
                elif key == 'sensor_noise' and value:
                    if value.get('mean', 0) < 0 or value.get('std', 0) < 0:
                        raise ValueError("Sensor noise values must be non-negative")
                elif key == 'effectiveness_metric' and value < 0:
                    raise ValueError("Effectiveness metric must be non-negative")

                setattr(self, key, value)

    def __str__(self) -> str:
        """
        String representation of the domain randomization parameters

        Returns:
            String representation
        """
        return f"DomainRandomizationParams(lighting={self.lighting_variation}, textures={self.texture_randomization}, effectiveness={self.effectiveness_metric})"

    def __repr__(self) -> str:
        """
        Detailed string representation of the domain randomization parameters

        Returns:
            Detailed string representation
        """
        return self.__str__()