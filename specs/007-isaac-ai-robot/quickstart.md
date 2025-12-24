# Quickstart Guide: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

## Prerequisites

### Hardware Requirements
- **Development**: RTX-enabled workstation (RTX 3080 or better recommended)
- **Deployment**: NVIDIA Jetson Orin (AGX Orin or Orin NX)
- **Alternative**: Cloud GPU instance with CUDA support

### Software Requirements
- Ubuntu 22.04 LTS
- ROS 2 Jazzy
- NVIDIA Isaac Sim 2024.2+
- Isaac ROS 3.x
- CUDA 12.x
- NVIDIA GPU drivers (535+)

## Installation

### 1. Install ROS 2 Jazzy
```bash
# Setup locale
sudo locale-gen en_US.UTF-8
export LANG=en_US.UTF-8

# Setup sources
sudo apt update && sudo apt install curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/rosEntries.list | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update

# Install ROS 2 packages
sudo apt install ros-jazzy-desktop ros-jazzy-cv-bridge ros-jazzy-tf2-tools python3-colcon-common-extensions
```

### 2. Install NVIDIA Isaac Sim
```bash
# Download Isaac Sim 2024.2+ from NVIDIA Developer website
# Follow NVIDIA's installation guide for your platform
# Ensure to install with Omniverse support
```

### 3. Install Isaac ROS
```bash
# Add Isaac ROS repository
sudo apt update && sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update

# Install Isaac ROS packages
sudo apt install ros-jazzy-isaac-ros-visual-slam ros-jazzy-isaac-ros-stereo-image-rectification
```

### 4. Setup Project Workspace
```bash
# Create workspace
mkdir -p ~/isaac_robot_ws/src
cd ~/isaac_robot_ws

# Build workspace
colcon build --symlink-install
source install/setup.bash
```

## Basic Usage

### 1. Launch Isaac Sim
```bash
# Source ROS environment
source ~/isaac_robot_ws/install/setup.bash

# Launch Isaac Sim with a basic humanoid scene
ros2 launch isaac_sim launch_isaac_sim.launch.py scene:=humanoid_lab
```

### 2. Generate Synthetic Dataset
```bash
# Run domain randomization to generate training data
ros2 run synthetic_data_generator generate_dataset \
  --scene_path /path/to/usd/scene.usd \
  --output_dir /path/to/dataset \
  --num_samples 1000 \
  --domain_randomization_params config/domain_randomization.yaml
```

### 3. Deploy VSLAM Pipeline
```bash
# Launch CUDA-accelerated VSLAM
ros2 launch vslam_pipeline stereo_vslam.launch.py \
  --stereo_camera_config config/stereo_camera.yaml \
  --cuda_enabled true
```

### 4. Configure Bipedal Navigation
```bash
# Launch Nav2 with bipedal-specific parameters
ros2 launch nav2_bipedal bringup_launch.py \
  --params_file config/bipedal_nav2_params.yaml \
  --map_file maps/indoor_lab.yaml
```

## Example Workflows

### Workflow 1: Synthetic Dataset Generation
1. Create USD scene in Isaac Sim
2. Configure domain randomization parameters
3. Run synthetic data generator
4. Validate dataset quality and annotations

### Workflow 2: VSLAM Pipeline Deployment
1. Calibrate stereo camera
2. Configure VSLAM parameters
3. Launch pipeline on Jetson hardware
4. Monitor performance metrics

### Workflow 3: Navigation in Simulation
1. Load environment map
2. Configure bipedal navigation parameters
3. Set navigation goal
4. Monitor path execution and recovery behaviors

## Troubleshooting

### Common Issues
- **CUDA not found**: Ensure NVIDIA drivers and CUDA are properly installed
- **Isaac Sim crashes**: Check GPU memory and driver compatibility
- **VSLAM performance**: Verify CUDA acceleration is enabled and working
- **Navigation failures**: Check costmap configuration for bipedal constraints

### Performance Tips
- Use CUDA 12.x for best Isaac ROS performance
- Ensure sufficient GPU memory for Isaac Sim scenes
- Optimize stereo camera resolution for target frame rate
- Profile navigation parameters for specific terrain types