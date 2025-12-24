# Data Model: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

## Entity: SyntheticDataset
**Description**: Collection of photorealistic images with ground truth annotations for training perception models
- **Fields**:
  - id: string (unique identifier)
  - name: string (dataset name)
  - size: integer (number of images)
  - format: string (image format, e.g., PNG, JPEG)
  - annotations: object (ground truth pose, depth, semantics)
  - domain_randomization: object (parameters used for randomization)
  - created_at: datetime (timestamp of generation)
- **Validation**: Size must be > 0, format must be valid image format
- **Relationships**: Generated from USDScene

## Entity: USDScene
**Description**: Universal Scene Description file representing 3D environments for Isaac Sim
- **Fields**:
  - id: string (unique identifier)
  - name: string (scene name)
  - path: string (file path to USD file)
  - description: string (scene description)
  - humanoid_robot: object (robot model configuration)
  - environment: object (scene objects and lighting)
  - created_at: datetime (timestamp of creation)
- **Validation**: Path must exist and be valid USD file
- **Relationships**: Used to generate SyntheticDataset

## Entity: VSLAMPipeline
**Description**: Visual SLAM system configuration and state
- **Fields**:
  - id: string (unique identifier)
  - name: string (pipeline name)
  - stereo_camera_config: object (camera parameters)
  - feature_detector: string (detector algorithm)
  - pose_estimator: string (estimation algorithm)
  - map_builder: object (mapping configuration)
  - performance_metrics: object (FPS, accuracy measurements)
  - cuda_enabled: boolean (whether CUDA acceleration is used)
- **Validation**: Camera config must be valid, CUDA must be available if enabled
- **Relationships**: Processes images from SyntheticDataset or real sensors

## Entity: BipedalNavigationPlan
**Description**: Navigation plan specifically configured for legged locomotion
- **Fields**:
  - id: string (unique identifier)
  - robot_config: object (bipedal kinematic constraints)
  - costmap_config: object (navigation costmap parameters)
  - behavior_tree: object (recovery behaviors)
  - path_planner: string (path planning algorithm)
  - success_rate: float (navigation success rate)
  - terrain_types: array (supported terrain types)
- **Validation**: Robot config must match humanoid kinematics
- **Relationships**: Uses VSLAMPipeline for localization

## Entity: HardwareDeployment
**Description**: Configuration for deploying on specific hardware platforms
- **Fields**:
  - id: string (unique identifier)
  - platform: string (e.g., "jetson-orin", "rtx-workstation", "cloud")
  - cuda_version: string (CUDA version)
  - isaac_ros_packages: array (installed packages)
  - performance_profile: object (resource usage characteristics)
  - power_consumption: float (watts)
- **Validation**: Platform must be supported, CUDA version must be compatible
- **Relationships**: Deploys VSLAMPipeline and BipedalNavigationPlan

## Entity: DomainRandomizationParams
**Description**: Configuration for domain randomization during synthetic data generation
- **Fields**:
  - id: string (unique identifier)
  - lighting_variation: object (range of lighting conditions)
  - texture_randomization: object (texture and material variations)
  - environment_objects: object (random object placement)
  - sensor_noise: object (simulated sensor noise parameters)
  - effectiveness_metric: float (sim-to-real transfer improvement)
- **Validation**: All ranges must be valid and non-negative
- **Relationships**: Applied to USDScene to generate SyntheticDataset