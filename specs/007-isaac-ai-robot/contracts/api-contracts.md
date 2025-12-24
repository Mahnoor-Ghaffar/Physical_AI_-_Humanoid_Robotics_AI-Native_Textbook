# API Contracts: Module 3: The AI-Robot Brain (NVIDIA Isaac™)

## Dataset Generation Service

### POST /datasets/generate
**Description**: Generate synthetic dataset using Isaac Sim and domain randomization

**Request**:
```json
{
  "scene_path": "/path/to/usd/scene.usd",
  "output_dir": "/path/to/output/dataset",
  "num_samples": 1000,
  "domain_randomization_params": {
    "lighting_variation": {"min": 0.5, "max": 1.5},
    "texture_randomization": true,
    "sensor_noise": {"mean": 0.0, "std": 0.1}
  }
}
```

**Response** (200 OK):
```json
{
  "dataset_id": "ds_12345",
  "status": "generating",
  "estimated_completion": "2025-01-23T15:30:00Z",
  "output_path": "/path/to/output/dataset"
}
```

**Response** (400 Bad Request):
```json
{
  "error": "Invalid scene path or parameters",
  "details": "Scene file does not exist"
}
```

## VSLAM Pipeline Service

### POST /vslam/start
**Description**: Start CUDA-accelerated VSLAM pipeline

**Request**:
```json
{
  "camera_config": {
    "left_camera_topic": "/camera/left/image_raw",
    "right_camera_topic": "/camera/right/image_raw",
    "calibration_file": "/path/to/stereo_calib.yaml"
  },
  "cuda_enabled": true,
  "map_init_method": "monocular"
}
```

**Response** (200 OK):
```json
{
  "pipeline_id": "vslam_67890",
  "status": "running",
  "pose_topic": "/vslam/pose",
  "map_topic": "/vslam/map"
}
```

**Response** (500 Internal Server Error):
```json
{
  "error": "CUDA initialization failed",
  "details": "Insufficient GPU memory"
}
```

### GET /vslam/{pipeline_id}/status
**Description**: Get current status and performance metrics of VSLAM pipeline

**Response** (200 OK):
```json
{
  "pipeline_id": "vslam_67890",
  "status": "running",
  "fps": 32.5,
  "pose_accuracy": {
    "position_error": 0.03,  // meters
    "orientation_error": 0.8 // degrees
  },
  "gpu_usage": 78.2,
  "tracking_status": "good"
}
```

## Navigation Service

### POST /navigation/plan
**Description**: Plan path for bipedal humanoid robot

**Request**:
```json
{
  "start_pose": {
    "x": 0.0,
    "y": 0.0,
    "theta": 0.0
  },
  "goal_pose": {
    "x": 5.0,
    "y": 3.0,
    "theta": 1.57
  },
  "robot_config": {
    "foot_separation": 0.3,
    "step_height": 0.15,
    "max_step_length": 0.4
  }
}
```

**Response** (200 OK):
```json
{
  "plan_id": "plan_abc123",
  "status": "success",
  "waypoints": [
    {"x": 0.5, "y": 0.2, "theta": 0.1},
    {"x": 1.0, "y": 0.8, "theta": 0.2},
    // ... more waypoints
  ],
  "estimated_time": 45.2  // seconds
}
```

**Response** (404 Not Found):
```json
{
  "error": "No valid path found",
  "details": "Goal is unreachable with current robot configuration"
}
```

### POST /navigation/execute
**Description**: Execute navigation plan for bipedal robot

**Request**:
```json
{
  "plan_id": "plan_abc123",
  "execution_params": {
    "max_velocity": 0.5,
    "safety_margin": 0.3,
    "recovery_enabled": true
  }
}
```

**Response** (200 OK):
```json
{
  "execution_id": "exec_def456",
  "status": "executing",
  "current_waypoint": 0,
  "progress": 0.0
}
```

## Hardware Deployment Service

### POST /deployment/configure
**Description**: Configure hardware deployment profile

**Request**:
```json
{
  "platform": "jetson-orin",
  "components": ["vslam", "navigation"],
  "performance_profile": "realtime",
  "resource_limits": {
    "cpu_percent": 80,
    "gpu_percent": 85,
    "memory_mb": 4096
  }
}
```

**Response** (200 OK):
```json
{
  "deployment_id": "deploy_789xyz",
  "status": "configured",
  "estimated_performance": {
    "vslam_fps": 30,
    "navigation_update_rate": 10
  }
}
```