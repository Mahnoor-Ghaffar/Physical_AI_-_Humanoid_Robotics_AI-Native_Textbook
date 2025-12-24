"""
Environment configuration management for different hardware targets
"""
import os
import platform
from typing import Dict, Any, Optional
from pathlib import Path


class EnvironmentManager:
    """
    Environment configuration management for different hardware targets
    """

    def __init__(self):
        self.system_info = self._get_system_info()
        self.hardware_target = self._detect_hardware_target()
        self.environment_config = self._get_environment_config()

    def _get_system_info(self) -> Dict[str, Any]:
        """
        Get system information for environment detection

        Returns:
            Dictionary with system information
        """
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'architecture': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'node': platform.node(),
        }

    def _detect_hardware_target(self) -> str:
        """
        Detect the hardware target based on system characteristics

        Returns:
            Detected hardware target ('desktop', 'jetson', 'orin', 'unknown')
        """
        # Check for Jetson platform
        if 'Linux' in self.system_info['platform'] and 'aarch64' in self.system_info['architecture']:
            # Check for Jetson-specific files
            jetson_files = [
                '/etc/nv_tegra_release',
                '/sys/module/tegra_fuse/parameters/tegra_chip_id'
            ]

            for jetson_file in jetson_files:
                if os.path.exists(jetson_file):
                    return 'jetson'

        # Check for specific Jetson models (like Orin)
        try:
            with open('/proc/device-tree/model', 'r', encoding='utf-8') as f:
                model = f.read().strip().lower()
                if 'orin' in model:
                    return 'orin'
                elif 'jetson' in model:
                    return 'jetson'
        except:
            pass

        # Check environment variables
        target = os.getenv('HARDWARE_TARGET', 'desktop')
        if target in ['desktop', 'jetson', 'orin']:
            return target

        # Default to desktop for other systems
        return 'desktop'

    def _get_environment_config(self) -> Dict[str, Any]:
        """
        Get environment-specific configuration

        Returns:
            Environment-specific configuration
        """
        base_config = {
            'system_info': self.system_info,
            'hardware_target': self.hardware_target,
            'cuda_available': self._check_cuda_availability(),
            'gpu_info': self._get_gpu_info(),
            'memory_info': self._get_memory_info(),
            'environment_variables': self._get_relevant_env_vars()
        }

        # Apply hardware-specific overrides
        if self.hardware_target == 'jetson':
            base_config.update({
                'max_threads': 6,  # Limited on Jetson
                'memory_limit': 0.7,  # Use 70% of available memory
                'performance_mode': 'balanced'
            })
        elif self.hardware_target == 'orin':
            base_config.update({
                'max_threads': 8,  # More cores on Orin
                'memory_limit': 0.8,  # Use 80% of available memory
                'performance_mode': 'high'
            })
        else:  # desktop
            base_config.update({
                'max_threads': os.cpu_count(),
                'memory_limit': 0.9,  # Use 90% of available memory on desktop
                'performance_mode': 'max'
            })

        return base_config

    def _check_cuda_availability(self) -> bool:
        """
        Check if CUDA is available on the system

        Returns:
            True if CUDA is available, False otherwise
        """
        try:
            import pycuda.driver as cuda
            cuda.init()
            return cuda.Device.count() > 0
        except:
            # Alternative check for CUDA availability
            cuda_visible_devices = os.getenv('CUDA_VISIBLE_DEVICES', '')
            nvidia_smi_exists = os.system('nvidia-smi > /dev/null 2>&1') == 0
            return bool(cuda_visible_devices) or nvidia_smi_exists

    def _get_gpu_info(self) -> Dict[str, Any]:
        """
        Get GPU information if available

        Returns:
            Dictionary with GPU information
        """
        gpu_info = {
            'cuda_available': self._check_cuda_availability(),
            'device_count': 0,
            'devices': []
        }

        if gpu_info['cuda_available']:
            try:
                import pycuda.driver as cuda
                cuda.init()
                gpu_info['device_count'] = cuda.Device.count()

                for i in range(gpu_info['device_count']):
                    device = cuda.Device(i)
                    gpu_info['devices'].append({
                        'id': i,
                        'name': device.name().decode('utf-8'),
                        'compute_capability': device.compute_capability(),
                        'total_memory': device.total_memory(),
                    })
            except:
                # Fallback method using nvidia-smi if pycuda is not available
                import subprocess
                try:
                    result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total', '--format=csv,noheader,nounits'],
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        gpu_info['device_count'] = len(result.stdout.strip().split('\n'))
                except:
                    pass

        return gpu_info

    def _get_memory_info(self) -> Dict[str, Any]:
        """
        Get system memory information

        Returns:
            Dictionary with memory information
        """
        try:
            import psutil
            memory = psutil.virtual_memory()
            return {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percentage': memory.percent
            }
        except ImportError:
            # Fallback without psutil
            return {
                'total': os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') if hasattr(os, 'sysconf') else 0,
                'available': 0,
                'used': 0,
                'percentage': 0
            }

    def _get_relevant_env_vars(self) -> Dict[str, str]:
        """
        Get relevant environment variables for the Isaac Robot Brain system

        Returns:
            Dictionary with relevant environment variables
        """
        relevant_vars = [
            'CUDA_VISIBLE_DEVICES',
            'ISAAC_SIM_PATH',
            'OMNIVERSE_CONFIG_PATH',
            'ROS_DOMAIN_ID',
            'PYTHONPATH',
            'LD_LIBRARY_PATH',
            'HARDWARE_TARGET',
            'ENVIRONMENT'
        ]

        env_vars = {}
        for var in relevant_vars:
            value = os.getenv(var)
            if value is not None:
                env_vars[var] = value

        return env_vars

    def get_config(self) -> Dict[str, Any]:
        """
        Get the current environment configuration

        Returns:
            Environment configuration dictionary
        """
        return self.environment_config

    def is_hardware_target(self, target: str) -> bool:
        """
        Check if the current hardware target matches the specified target

        Args:
            target: Target hardware ('desktop', 'jetson', 'orin')

        Returns:
            True if current hardware matches target, False otherwise
        """
        return self.hardware_target == target

    def get_performance_config(self) -> Dict[str, Any]:
        """
        Get performance-specific configuration based on hardware target

        Returns:
            Performance configuration
        """
        if self.hardware_target == 'jetson':
            return {
                'max_fps': 30,
                'max_resolution': [1280, 720],
                'feature_count': 1000,
                'processing_threads': 4
            }
        elif self.hardware_target == 'orin':
            return {
                'max_fps': 60,
                'max_resolution': [1920, 1080],
                'feature_count': 2000,
                'processing_threads': 6
            }
        else:  # desktop
            return {
                'max_fps': 60,
                'max_resolution': [1920, 1080],
                'feature_count': 4000,
                'processing_threads': os.cpu_count()
            }


# Global environment manager instance
environment_manager = EnvironmentManager()


def get_environment_manager() -> EnvironmentManager:
    """
    Get the global environment manager instance

    Returns:
        EnvironmentManager instance
    """
    return environment_manager