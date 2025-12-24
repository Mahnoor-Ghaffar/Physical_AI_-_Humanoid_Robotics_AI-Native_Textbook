"""
USDScene model for Isaac Robot Brain
"""
from datetime import datetime
from typing import Dict, Any, Optional
import os


class USDScene:
    """
    Universal Scene Description file representing 3D environments for Isaac Sim
    """

    def __init__(self,
                 scene_id: str,
                 name: str,
                 path: str,
                 description: str = "",
                 humanoid_robot: Optional[Dict[str, Any]] = None,
                 environment: Optional[Dict[str, Any]] = None):
        """
        Initialize a USDScene instance

        Args:
            scene_id: Unique identifier for the scene
            name: Name of the scene
            path: File path to the USD file
            description: Description of the scene
            humanoid_robot: Robot model configuration
            environment: Scene objects and lighting configuration
        """
        if not os.path.exists(path):
            raise ValueError(f"USD file does not exist: {path}")

        if not path.lower().endswith(('.usd', '.usda', '.usdc', '.usdz')):
            raise ValueError(f"Invalid USD file format: {path}")

        self.id = scene_id
        self.name = name
        self.path = path
        self.description = description
        self.humanoid_robot = humanoid_robot or {}
        self.environment = environment or {}
        self.created_at = datetime.now()

    def validate(self) -> bool:
        """
        Validate the USD scene

        Returns:
            True if valid, False otherwise
        """
        if not os.path.exists(self.path):
            return False

        if not self.path.lower().endswith(('.usd', '.usda', '.usdc', '.usdz')):
            return False

        return True

    def get_scene_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about the scene

        Returns:
            Dictionary with scene information
        """
        return {
            'id': self.id,
            'name': self.name,
            'path': self.path,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'has_humanoid_robot': bool(self.humanoid_robot),
            'environment_objects_count': len(self.environment.get('objects', [])) if isinstance(self.environment.get('objects'), list) else 0,
            'lighting_config': self.environment.get('lighting', {}),
            'robot_config': self.humanoid_robot
        }

    def load_scene(self):
        """
        Load the USD scene using the USDSceneLoader
        """
        from .scene_loader import USDSceneLoader
        loader = USDSceneLoader()
        return loader.load_scene(self.path)

    def get_scene_size(self) -> Optional[int]:
        """
        Get the size of the USD file

        Returns:
            Size in bytes or None if file doesn't exist
        """
        if os.path.exists(self.path):
            return os.path.getsize(self.path)
        return None

    def __str__(self) -> str:
        """
        String representation of the scene

        Returns:
            String representation
        """
        return f"USDScene(id={self.id}, name={self.name}, path={self.path})"

    def __repr__(self) -> str:
        """
        Detailed string representation of the scene

        Returns:
            Detailed string representation
        """
        return self.__str__()