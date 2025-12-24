"""
Base configuration management for Isaac Robot Brain
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path


class ConfigManager:
    """
    Base configuration management for the Isaac Robot Brain system
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager

        Args:
            config_path: Path to the main configuration file (optional)
        """
        self.config_path = config_path
        self.config = {}
        self.environment = os.getenv('ENVIRONMENT', 'development')

        # Load default configuration
        self._load_default_config()

        # Override with custom config if provided
        if config_path:
            self.load_config(config_path)

    def _load_default_config(self):
        """
        Load default configuration values
        """
        self.config = {
            'environment': self.environment,
            'simulation': {
                'default_scene_path': 'assets/scenes/default.usd',
                'render_resolution': [1920, 1080],
                'max_steps': 1000,
                'time_step': 1.0/60.0,  # 60 FPS
            },
            'vslam': {
                'camera_config': {
                    'resolution': [640, 480],
                    'fov': 90.0,  # degrees
                    'baseline': 0.2,  # meters
                },
                'cuda_enabled': True,
                'max_features': 2000,
                'min_match_distance': 20,
            },
            'navigation': {
                'max_velocity': 0.5,  # m/s
                'min_distance_to_obstacle': 0.5,  # meters
                'planning_frequency': 10.0,  # Hz
                'recovery_enabled': True,
            },
            'hardware': {
                'target_platform': 'desktop',  # desktop, jetson, orin
                'cuda_version': '12.0',
                'gpu_memory_limit': 0.8,  # 80% of available memory
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file_path': 'logs/robot_brain.log',
            }
        }

    def load_config(self, config_path: str):
        """
        Load configuration from a YAML file

        Args:
            config_path: Path to the YAML configuration file
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r') as f:
            yaml_config = yaml.safe_load(f)

        # Deep merge the loaded config with defaults
        self._deep_merge(self.config, yaml_config)

    def save_config(self, config_path: str):
        """
        Save current configuration to a YAML file

        Args:
            config_path: Path to save the configuration file
        """
        with open(config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation (e.g., 'vslam.cuda_enabled')

        Args:
            key: Configuration key in dot notation
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any):
        """
        Set a configuration value using dot notation

        Args:
            key: Configuration key in dot notation
            value: Value to set
        """
        keys = key.split('.')
        config_ref = self.config

        for k in keys[:-1]:
            if k not in config_ref:
                config_ref[k] = {}
            config_ref = config_ref[k]

        config_ref[keys[-1]] = value

    def _deep_merge(self, base_dict: Dict, update_dict: Dict):
        """
        Deep merge update_dict into base_dict

        Args:
            base_dict: Dictionary to update
            update_dict: Dictionary with values to update
        """
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._deep_merge(base_dict[key], value)
            else:
                base_dict[key] = value

    def get_platform_config(self, platform: str) -> Dict[str, Any]:
        """
        Get configuration optimized for a specific platform

        Args:
            platform: Target platform ('desktop', 'jetson', 'orin')

        Returns:
            Platform-specific configuration
        """
        platform_configs = {
            'desktop': {
                'vslam': {
                    'max_features': 4000,
                    'cuda_enabled': True,
                },
                'simulation': {
                    'render_resolution': [1920, 1080],
                    'max_steps': 10000,
                }
            },
            'jetson': {
                'vslam': {
                    'max_features': 1000,
                    'cuda_enabled': True,
                },
                'simulation': {
                    'render_resolution': [640, 480],
                    'max_steps': 1000,
                }
            },
            'orin': {
                'vslam': {
                    'max_features': 2000,
                    'cuda_enabled': True,
                },
                'simulation': {
                    'render_resolution': [1280, 720],
                    'max_steps': 5000,
                }
            }
        }

        platform_config = self.config.copy()
        if platform in platform_configs:
            self._deep_merge(platform_config, platform_configs[platform])

        return platform_config


# Global configuration instance
config_manager = ConfigManager()


def get_config() -> ConfigManager:
    """
    Get the global configuration manager instance

    Returns:
        ConfigManager instance
    """
    return config_manager