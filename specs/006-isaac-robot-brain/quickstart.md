# Quickstart Guide: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

This quickstart guide provides instructions for setting up the development environment and running the code examples presented in Module 3 of the Physical AI & Humanoid Robotics Textbook. It covers the necessary software installations, configuration steps, and basic commands to get started with NVIDIA Isaac Sim, Isaac ROS, ROS 2 Kilted Kaiju, and Nav2.

## 1. System Requirements

Ensure your system meets the following minimum requirements:

- **Operating System**: Ubuntu 24.04 LTS (recommended)
- **GPU**: NVIDIA RTX 30 Series or 40 Series GPU (or equivalent NVIDIA professional GPU) with the latest NVIDIA drivers installed.
- **Processor**: Intel Core i7 (10th Gen or newer) or AMD Ryzen 7 (3000 Series or newer)
- **RAM**: 32 GB or more
- **Storage**: 500 GB SSD or more free space

## 2. Setting Up the Development Environment (Docker-based)

To ensure a consistent and reproducible environment, all examples are designed to run within Docker containers.

### 2.1. Install Docker and NVIDIA Container Toolkit

Follow the official Docker and NVIDIA Container Toolkit installation guides for Ubuntu 24.04:

- [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- [Install NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

Verify your installation:
```bash
sudo docker run --rm --gpus all ubuntu nvidia-smi
```
You should see your GPU information.

### 2.2. Clone the Repository

Clone the textbook repository, which contains all code examples and configuration files:
```bash
git clone https://github.com/[YOUR_ORG]/ai-native-book.git
cd ai-native-book
```

### 2.3. Build the Docker Image for Module 3

Navigate to the Module 3 specific Dockerfile and build the image:
```bash
cd docker/module3-isaac-env
sudo docker build -t module3-isaac-env:latest .
```
This process might take a while as it downloads and installs NVIDIA Isaac Sim 5.1, Isaac ROS 3.2, ROS 2 Kilted Kaiju, and Nav2 1.4.x.

## 3. Launching the Development Container

Once the Docker image is built, you can launch a development container:
```bash
sudo docker run --gpus all --rm -it \
    --network host \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /path/to/ai-native-book:/workspace/ai-native-book \
    --name module3-dev \
    module3-isaac-env:latest /bin/bash
```
**Note**: Replace `/path/to/ai-native-book` with the absolute path to your cloned repository on your host machine.

Inside the container, you will be in the `/workspace/ai-native-book` directory.

## 4. Running Chapter Examples

### 4.1. Chapter 1: Photorealistic Simulation with NVIDIA Isaac Sim

Navigate to the Chapter 1 examples directory:
```bash
cd /workspace/ai-native-book/src/code-examples/module3/ch1_isaac_sim
```
To launch an Isaac Sim example (e.g., scene building with OmniGraph):
```bash
./run_scene_builder.sh
# Or, to run a Python OmniScript
python3 omnigraph_example.py
```
**Expected Outcome**: Isaac Sim GUI should launch, displaying the simulated environment or executing the specified script.

### 4.2. Chapter 2: Isaac ROS for Hardware-Accelerated Perception

Navigate to the Chapter 2 examples directory:
```bash
cd /workspace/ai-native-book/src/code-examples/module3/ch2_isaac_ros
```
To launch a VSLAM pipeline example:
```bash
ros2 launch isaac_ros_vslam vslam_example.launch.py
```
**Expected Outcome**: ROS 2 nodes for VSLAM should start, processing simulated sensor data, and potentially displaying a map or pose estimation in RViz if configured.

### 4.3. Chapter 3: Nav2 Path Planning for Bipedal Humanoids

Navigate to the Chapter 3 examples directory:
```bash
cd /workspace/ai-native-book/src/code-examples/module3/ch3_nav2_humanoid
```
To launch a Nav2 example for humanoid navigation:
```bash
ros2 launch humanoid_nav2_bringup nav2_humanoid_example.launch.py
```
**Expected Outcome**: A simulated humanoid robot in Isaac Sim should be controllable via Nav2, able to plan and execute paths while avoiding obstacles. RViz might display planned paths and costmaps.

## 5. Running the Capstone Project

The capstone project integrates concepts from all three chapters.

Navigate to the capstone project directory:
```bash
cd /workspace/ai-native-book/src/code-examples/module3/capstone_humanoid_navigator
```
Follow the `README.md` in this directory for specific instructions on how to:
1.  Generate synthetic data for VSLAM training.
2.  Train a simple perception model (if applicable).
3.  Deploy the VSLAM-trained humanoid navigator in Isaac Sim.

## 6. Accessing the Docusaurus Textbook

The textbook content itself is accessible via a web browser. On your host machine, once the Docusaurus site is built and served (instructions not part of this quickstart but covered in the main project documentation):
1.  Open your web browser.
2.  Navigate to `http://localhost:3000/` (or the port where Docusaurus is served).
3.  Browse to Module 3: The AI-Robot Brain (NVIDIA Isaac™).

## Hardware Tracks Specifics

- **Track A (RTX Workstation + Isaac Sim)**: The Docker setup primarily caters to this. Ensure direct GPU access.
- **Track B (Jetson/Unitree + Isaac ROS)**: While primary development is in Docker, Isaac ROS examples are designed to be deployable on Jetson. Specific deployment instructions for Jetson will be provided within Chapter 2.
- **Track C (Cloud/AWS Omniverse)**: For cloud-based development, refer to NVIDIA's official documentation for setting up Isaac Sim on AWS Omniverse. The core code examples remain the same.

**Important**: Always refer to the `README.md` files within individual example directories for the most up-to-date and specific instructions.
