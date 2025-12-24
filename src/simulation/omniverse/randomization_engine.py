"""
Domain randomization engine for Isaac Robot Brain
"""
import random
import numpy as np
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class RandomizationConfig:
    """
    Configuration for domain randomization parameters
    """
    lighting_range: Tuple[float, float] = (0.5, 1.5)
    texture_variation: bool = True
    material_properties: Dict[str, Tuple[float, float]] = None
    camera_noise: Tuple[float, float] = (0.0, 0.1)  # mean, std
    background_variation: bool = True
    object_placement_range: Tuple[float, float] = (-2.0, 2.0)


class DomainRandomizationEngine:
    """
    Engine for applying domain randomization during synthetic data generation
    """

    def __init__(self, config: RandomizationConfig = None):
        """
        Initialize the domain randomization engine

        Args:
            config: Configuration for randomization parameters
        """
        self.config = config or RandomizationConfig()
        self.random_state = random.Random()
        self.np_random_state = np.random.RandomState()

    def apply_lighting_randomization(self, base_intensity: float = 1.0) -> float:
        """
        Apply randomization to lighting intensity

        Args:
            base_intensity: Base lighting intensity

        Returns:
            Randomized lighting intensity
        """
        min_val, max_val = self.config.lighting_range
        random_factor = self.np_random_state.uniform(min_val, max_val)
        randomized_intensity = base_intensity * random_factor

        return randomized_intensity

    def apply_texture_randomization(self) -> Dict[str, Any]:
        """
        Apply randomization to textures and materials

        Returns:
            Dictionary with randomized texture parameters
        """
        if not self.config.texture_variation:
            return {}

        # Generate random texture parameters
        texture_params = {
            'roughness': self.np_random_state.uniform(0.0, 1.0),
            'metallic': self.np_random_state.uniform(0.0, 1.0),
            'specular': self.np_random_state.uniform(0.0, 1.0),
            'normal_map_strength': self.np_random_state.uniform(0.0, 1.0),
            'displacement_scale': self.np_random_state.uniform(0.0, 0.1)
        }

        return texture_params

    def apply_material_randomization(self) -> Dict[str, Any]:
        """
        Apply randomization to material properties

        Returns:
            Dictionary with randomized material properties
        """
        if not self.config.material_properties:
            # Use default material property ranges
            material_ranges = {
                'roughness': (0.0, 1.0),
                'metallic': (0.0, 1.0),
                'specular': (0.0, 1.0)
            }
        else:
            material_ranges = self.config.material_properties

        material_params = {}
        for prop, (min_val, max_val) in material_ranges.items():
            material_params[prop] = self.np_random_state.uniform(min_val, max_val)

        return material_params

    def apply_camera_noise(self, base_image: np.ndarray) -> np.ndarray:
        """
        Apply noise to simulate real camera conditions

        Args:
            base_image: Original image array

        Returns:
            Image array with added noise
        """
        mean, std = self.config.camera_noise
        noise = self.np_random_state.normal(mean, std, base_image.shape)
        noisy_image = base_image + noise

        # Clip values to valid range [0, 255] for uint8 images
        noisy_image = np.clip(noisy_image, 0, 255)

        return noisy_image.astype(base_image.dtype)

    def apply_background_randomization(self) -> Dict[str, Any]:
        """
        Apply randomization to background elements

        Returns:
            Dictionary with randomized background parameters
        """
        if not self.config.background_variation:
            return {}

        background_params = {
            'color_shift': [
                self.np_random_state.uniform(-0.1, 0.1),
                self.np_random_state.uniform(-0.1, 0.1),
                self.np_random_state.uniform(-0.1, 0.1)
            ],
            'blur_amount': self.np_random_state.uniform(0.0, 2.0),
            'background_objects_count': self.np_random_state.randint(0, 5),
            'background_object_types': self._get_random_background_objects(
                self.np_random_state.randint(0, 3)
            )
        }

        return background_params

    def _get_random_background_objects(self, count: int) -> List[str]:
        """
        Get random background object types

        Args:
            count: Number of object types to return

        Returns:
            List of background object types
        """
        object_types = ['tree', 'building', 'fence', 'car', 'lamp_post', 'sign', 'bush']
        selected_objects = self.np_random_state.choice(
            object_types,
            size=min(count, len(object_types)),
            replace=False
        ).tolist()

        return selected_objects

    def apply_object_placement_randomization(self, object_positions: List[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
        """
        Apply randomization to object placement in the scene

        Args:
            object_positions: Original object positions

        Returns:
            Randomized object positions
        """
        min_val, max_val = self.config.object_placement_range
        randomized_positions = []

        for pos in object_positions:
            # Add random offset to each position
            offset = (
                self.np_random_state.uniform(-0.5, 0.5),
                self.np_random_state.uniform(-0.5, 0.5),
                self.np_random_state.uniform(-0.2, 0.2)  # smaller vertical offset
            )
            new_pos = (
                pos[0] + offset[0],
                pos[1] + offset[1],
                pos[2] + offset[2]
            )
            randomized_positions.append(new_pos)

        return randomized_positions

    def apply_full_randomization(self, step: int = 0) -> Dict[str, Any]:
        """
        Apply all forms of randomization and return parameters

        Args:
            step: Current step in the generation process (for consistent randomization)

        Returns:
            Dictionary with all randomization parameters
        """
        # Set random seed based on step for reproducible results
        self.np_random_state.seed(step)

        randomization_params = {
            'lighting': self.apply_lighting_randomization(),
            'textures': self.apply_texture_randomization(),
            'materials': self.apply_material_randomization(),
            'background': self.apply_background_randomization(),
            'object_placement_offset': self.np_random_state.uniform(-0.5, 0.5, size=3).tolist()
        }

        return randomization_params

    def get_effectiveness_metric(self, previous_metric: float = 0.0) -> float:
        """
        Calculate the effectiveness of domain randomization

        Args:
            previous_metric: Previous effectiveness metric (for tracking improvement)

        Returns:
            Updated effectiveness metric
        """
        # In a real implementation, this would calculate the actual improvement
        # in sim-to-real transfer based on the randomization applied
        # For now, we'll return a simulated improvement
        improvement = self.np_random_state.uniform(0.05, 0.15)  # 5-15% improvement
        new_metric = min(1.0, previous_metric + improvement)  # Cap at 100%

        return new_metric

    def reset_randomization(self):
        """
        Reset the randomization engine to initial state
        """
        self.random_state = random.Random()
        self.np_random_state = np.random.RandomState()

    def set_seed(self, seed: int):
        """
        Set the random seed for reproducible randomization

        Args:
            seed: Random seed value
        """
        self.random_state.seed(seed)
        self.np_random_state.seed(seed)

    def configure(self, new_config: RandomizationConfig):
        """
        Update the randomization configuration

        Args:
            new_config: New configuration for randomization
        """
        self.config = new_config