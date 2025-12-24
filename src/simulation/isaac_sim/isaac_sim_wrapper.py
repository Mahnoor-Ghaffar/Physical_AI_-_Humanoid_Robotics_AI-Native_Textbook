"""
Isaac Sim API wrapper structure
"""
import subprocess
import os
from typing import Optional, Dict, Any, List


class IsaacSimWrapper:
    """
    Wrapper for Isaac Sim API interactions
    """

    def __init__(self, sim_path: Optional[str] = None):
        """
        Initialize the Isaac Sim wrapper

        Args:
            sim_path: Path to Isaac Sim installation (optional)
        """
        self.sim_path = sim_path or self._find_isaac_sim()
        self.is_running = False
        self.process = None

    def _find_isaac_sim(self) -> Optional[str]:
        """
        Attempt to find Isaac Sim installation

        Returns:
            Path to Isaac Sim if found, None otherwise
        """
        # Common installation paths for Isaac Sim
        common_paths = [
            "/opt/nvidia/isaac-sim",
            os.path.expanduser("~/isaac-sim"),
            os.path.expanduser("~/Documents/NVIDIA_Omniverse/Isaac-Sim"),
            "C:/Users/Public/Documents/NVIDIA Corporation/Isaac-Sim",  # Windows path
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path

        return None

    def launch_simulation(self, scene_path: Optional[str] = None, headless: bool = False) -> bool:
        """
        Launch Isaac Sim with optional scene

        Args:
            scene_path: Path to USD scene to load (optional)
            headless: Whether to run in headless mode

        Returns:
            True if simulation launched successfully, False otherwise
        """
        if not self.sim_path or not os.path.exists(self.sim_path):
            print("Error: Isaac Sim installation not found")
            return False

        try:
            # Build the command to launch Isaac Sim
            cmd = []
            if os.name == 'nt':  # Windows
                cmd = [os.path.join(self.sim_path, "isaac-sim.bat")]
            else:  # Linux/Mac
                cmd = [os.path.join(self.sim_path, "isaac-sim.sh")]

            if headless:
                cmd.extend(["--no-window", "--exec", "headless_simulation.py"])

            if scene_path:
                cmd.extend(["--scene", scene_path])

            # Launch the simulation
            self.process = subprocess.Popen(cmd)
            self.is_running = True
            print("Isaac Sim launched successfully")
            return True
        except Exception as e:
            print(f"Error launching Isaac Sim: {str(e)}")
            return False

    def stop_simulation(self):
        """
        Stop the running Isaac Sim instance
        """
        if self.process and self.is_running:
            self.process.terminate()
            self.process.wait()
            self.is_running = False
            print("Isaac Sim stopped")

    def execute_script(self, script_path: str) -> bool:
        """
        Execute a Python script within Isaac Sim

        Args:
            script_path: Path to the Python script to execute

        Returns:
            True if script executed successfully, False otherwise
        """
        if not self.sim_path or not os.path.exists(self.sim_path):
            print("Error: Isaac Sim installation not found")
            return False

        if not os.path.exists(script_path):
            print(f"Error: Script file does not exist: {script_path}")
            return False

        try:
            # Execute script within Isaac Sim context
            cmd = []
            if os.name == 'nt':  # Windows
                cmd = [os.path.join(self.sim_path, "python.bat"), script_path]
            else:  # Linux/Mac
                cmd = [os.path.join(self.sim_path, "python.sh"), script_path]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Script executed successfully: {script_path}")
                return True
            else:
                print(f"Script execution failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error executing script: {str(e)}")
            return False

    def get_simulation_status(self) -> Dict[str, Any]:
        """
        Get the current status of the simulation

        Returns:
            Dictionary with simulation status information
        """
        return {
            'is_running': self.is_running,
            'sim_path': self.sim_path,
            'process_id': self.process.pid if self.process else None
        }