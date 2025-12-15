# Data Model: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

## Key Entities

### Humanoid Robot Model
**Description**: Represents the bipedal robot used in simulations and navigation tasks within NVIDIA Isaac Sim.
**Attributes**:
- `name`: String (e.g., "Unitree H1", "Generic Humanoid")
- `kinematic_properties`: Object (e.g., joint limits, degrees of freedom)
- `dynamic_properties`: Object (e.g., mass, inertia, friction coefficients)
- `sensor_configurations`: Array of Objects (e.g., camera types, IMU placements, LiDAR)
    - `type`: String (e.g., "RGB-D Camera", "IMU", "LiDAR")
    - `mount_location`: String (e.g., "head", "torso", "foot")
    - `specs`: Object (e.g., resolution, field of view, frequency)
- `visual_mesh_definitions`: Array of Strings (paths to USD assets for visual representation)
- `control_interface`: String (e.g., "ROS 2 topics", "Isaac Sim ActionGraph")
**Relationships**:
- Interacts with `Omniverse Scene`.
- Provides data to `VSLAM Pipeline`.
- Controlled by `Nav2 Stack`.

### Omniverse Scene
**Description**: A virtual 3D environment constructed within NVIDIA Isaac Sim, serving as the setting for all simulations.
**Attributes**:
- `name`: String (e.g., "Warehouse", "Office Environment")
- `usd_assets`: Array of Strings (paths to USD files for static and dynamic objects)
- `lighting_conditions`: Object (e.g., light sources, intensity, ambient light)
- `physics_properties`: Object (e.g., gravity, friction, collision layers)
- `domain_randomization_parameters`: Object (e.g., texture randomization, light randomization, object placement variability)
- `simulation_interface`: String (e.g., "Python OmniScript", "ROS 2 bridge")
**Relationships**:
- Contains `Humanoid Robot Model` and other simulation assets.
- Source for `Synthetic Dataset` generation.

### Synthetic Dataset
**Description**: High-fidelity data generated within Isaac Sim using Omniverse Replicator, specifically designed for training and validation of perception models.
**Attributes**:
- `dataset_id`: String (Unique identifier)
- `modality`: Array of Strings (e.g., "RGB images", "depth maps", "segmentation masks", "bounding boxes", "point clouds")
- `num_samples`: Integer
- `generation_parameters`: Object (parameters used in Omniverse Replicator for this dataset)
- `ground_truth_labels`: Object (e.g., bounding boxes, object poses, camera poses, segmentation masks)
- `storage_path`: String (path to where the dataset is saved)
**Relationships**:
- Generated from `Omniverse Scene`.
- Used to train perception models within `VSLAM Pipeline` (e.g., object detection).

### VSLAM Pipeline
**Description**: A software stack, primarily built using Isaac ROS components, responsible for real-time visual simultaneous localization and mapping.
**Attributes**:
- `pipeline_name`: String (e.g., "VisualSlamNode", "Nav2SLAM")
- `sensor_inputs`: Array of Objects (e.g., stereo cameras, IMUs, LiDAR)
    - `source`: String (e.g., "Isaac Sim", "Physical Robot")
    - `topic`: String (ROS 2 topic name)
- `pose_estimation_output`: Object (e.g., estimated robot pose, covariance)
    - `topic`: String (ROS 2 topic name)
- `map_output`: Object (e.g., generated occupancy grid, point cloud map)
    - `topic`: String (ROS 2 topic name)
- `components`: Array of Strings (e.g., "Feature Tracker", "Local Mapper", "Loop Closure Detector")
- `acceleration_tech`: String (e.g., "CUDA", "TensorRT", "GEMs")
**Relationships**:
- Consumes data from `Humanoid Robot Model` sensors (via `Omniverse Scene` or real hardware).
- Provides localization and mapping to `Nav2 Stack`.
- Leverages `GEMs`.

### Nav2 Stack
**Description**: The ROS 2 navigation framework specifically configured and adapted for path planning and execution for bipedal humanoid locomotion.
**Attributes**:
- `configuration_name`: String (e.g., "HumanoidNav2Profile")
- `global_planner`: String (e.g., "NavFn", "Dijkstra")
- `local_planner`: String (e.g., "DWA", "TEB", "HumanoidSpecificPlanner")
- `costmaps`: Object
    - `static_map`: String (path to static map, e.g., from VSLAM)
    - `obstacle_layer`: Object (configuration for dynamic obstacle detection)
    - `inflation_layer`: Object (configuration for inflation radius)
- `behavior_trees`: Array of Objects (XML definitions for navigation behaviors)
- `robot_footprint`: Array of Objects (coordinates defining the robot's collision boundary)
- `recovery_behaviors`: Array of Strings (e.g., "clear_costmap", "spin_robot")
- `humanoid_specific_plugins`: Array of Strings (custom plugins for gait adaptation, balance control)
**Relationships**:
- Consumes pose and map data from `VSLAM Pipeline`.
- Commands `Humanoid Robot Model` for locomotion.

### GEMs (GPU-accelerated Extensions for ROS)
**Description**: Isaac ROS specific packages providing highly optimized, hardware-accelerated components for various robotics functionalities, particularly perception and navigation.
**Attributes**:
- `gem_name`: String (e.g., "isaac_ros_image_proc", "isaac_ros_argus_camera")
- `functionality`: String (e.g., "image processing", "camera driver", "stereo matching")
- `acceleration_tech`: String (e.g., "CUDA", "TensorRT")
- `ros_interface`: Object (ROS 2 topic interfaces, services, actions)
- `compatibility`: Array of Strings (compatible Isaac ROS versions, Jetson platforms)
**Relationships**:
- Utilized by `VSLAM Pipeline` for accelerated processing.
- Potentially used by `Nav2 Stack` for accelerated sensor processing or path planning components.
