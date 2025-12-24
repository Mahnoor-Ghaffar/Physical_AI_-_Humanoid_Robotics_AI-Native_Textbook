"""
USD Scene loading framework for Isaac Sim integration
"""
import os
from typing import Optional, Dict, Any
from pxr import Usd, UsdGeom, Sdf


class USDSceneLoader:
    """
    Framework for loading and managing USD scenes in Isaac Sim
    """

    def __init__(self):
        self.stage = None
        self.scene_path = None

    def load_scene(self, scene_path: str) -> bool:
        """
        Load a USD scene from the specified path

        Args:
            scene_path: Path to the USD file

        Returns:
            True if scene loaded successfully, False otherwise
        """
        if not os.path.exists(scene_path):
            print(f"Error: Scene file does not exist: {scene_path}")
            return False

        if not scene_path.lower().endswith(('.usd', '.usda', '.usdc', '.usdz')):
            print(f"Error: Invalid USD file format: {scene_path}")
            return False

        try:
            self.stage = Usd.Stage.Open(scene_path)
            if not self.stage:
                print(f"Error: Could not open USD stage: {scene_path}")
                return False

            self.scene_path = scene_path
            print(f"Successfully loaded USD scene: {scene_path}")
            return True
        except Exception as e:
            print(f"Error loading USD scene {scene_path}: {str(e)}")
            return False

    def get_scene_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the loaded scene

        Returns:
            Dictionary with scene information or None if no scene loaded
        """
        if not self.stage:
            return None

        scene_info = {
            'scene_path': self.scene_path,
            'prim_count': len(self.stage.GetPrimAtPath('/').GetChildren()),
            'up_axis': UsdGeom.GetStageUpAxis(self.stage),
            'meters_per_unit': self.stage.GetStageMetersPerUnit(),
            'time_codes_per_second': self.stage.GetTimeCodesPerSecond()
        }

        return scene_info

    def close_scene(self):
        """
        Close the currently loaded scene
        """
        if self.stage:
            self.stage.Close()
            self.stage = None
            self.scene_path = None