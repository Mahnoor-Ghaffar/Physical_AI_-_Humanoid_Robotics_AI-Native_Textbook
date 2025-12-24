# Quickstart Guide: Vision-Language-Action (VLA) Module

## Prerequisites

### System Requirements
- Ubuntu 22.04 LTS
- ROS 2 Jazzy installed
- Python 3.10 or higher
- At least 16GB RAM (32GB recommended for optimal performance)
- NVIDIA GPU with CUDA support (RTX 3080 or equivalent for local inference)

### Software Dependencies
```bash
# Install ROS 2 Jazzy
sudo apt update
sudo apt install ros-jazzy-desktop ros-jazzy-ros-base

# Install Python dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install openai whisper-openai transformers langchain
pip install ros2-interfaces rclpy std-msgs
```

### API Keys and Access
- OpenAI API key for Whisper and GPT services
- Hugging Face token for VLA model access (if using private models)
- ROS 2 workspace setup with necessary packages

## Environment Setup

### 1. Create ROS 2 Workspace
```bash
mkdir -p ~/vla_ws/src
cd ~/vla_ws
colcon build
source install/setup.bash
```

### 2. Install VLA Module Dependencies
```bash
cd ~/vla_ws/src
git clone https://github.com/your-repo/vla-module.git
cd ~/vla_ws
pip install -r src/vla-module/requirements.txt
colcon build
source install/setup.bash
```

### 3. Configure API Keys
Create a `.env` file in your workspace:
```
OPENAI_API_KEY=your_openai_api_key_here
HUGGING_FACE_TOKEN=your_huggingface_token_here
ROS_DOMAIN_ID=42
```

## Basic Voice-to-Action Example

### 1. Start the Voice Recognition Node
```bash
source ~/vla_ws/install/setup.bash
ros2 run vla_module voice_recognition_node
```

### 2. Test Voice Command Processing
```bash
# In another terminal
ros2 topic echo /transcription
```

### 3. Speak a Command
Say "Move forward" to test the basic voice-to-action pipeline.

## Cognitive Planning Example

### 1. Start the Planning Node
```bash
source ~/vla_ws/install/setup.bash
ros2 run vla_module planning_node
```

### 2. Send a Complex Task
```bash
ros2 topic pub /task_request std_msgs/String "data: 'Clean the room'"
```

### 3. Observe Action Sequence Generation
The system will decompose "Clean the room" into subtasks and generate an executable action sequence.

## Full VLA Integration Example

### 1. Start All VLA Components
```bash
source ~/vla_ws/install/setup.bash
# Start all nodes in separate terminals or use launch file
ros2 launch vla_module vla_system.launch.py
```

### 2. Execute End-to-End Task
```bash
# Send a complex command combining vision, language, and action
ros2 topic pub /voice_command std_msgs/String "data: 'Find the red ball and place it in the box'"
```

### 3. Monitor System Response
Watch the system process the command through:
- Voice transcription
- Language understanding
- Vision processing
- Action planning
- Robot execution

## Hardware Track Configuration

### RTX Local Inference Track
```bash
# Set environment for local GPU processing
export VLA_HARDWARE_TRACK=rtx
export CUDA_VISIBLE_DEVICES=0
ros2 run vla_module vla_node --hardware-track rtx
```

### Jetson Edge Deployment Track
```bash
# Set environment for Jetson optimization
export VLA_HARDWARE_TRACK=jetson
export VLA_MODEL_SIZE=small  # Use smaller models for edge
ros2 run vla_module vla_node --hardware-track jetson
```

### Cloud API Track
```bash
# Use cloud-based processing
export VLA_HARDWARE_TRACK=cloud
export OPENAI_API_KEY=your_cloud_api_key
ros2 run vla_module vla_node --hardware-track cloud
```

## Troubleshooting

### Common Issues

1. **CUDA/GPU Issues**:
   - Ensure NVIDIA drivers are properly installed
   - Verify CUDA version compatibility (11.8 recommended)
   - Check GPU memory availability

2. **ROS 2 Communication Issues**:
   - Verify ROS_DOMAIN_ID is consistent across nodes
   - Check network configuration for multi-machine setups
   - Ensure all nodes are on the same ROS domain

3. **API Access Issues**:
   - Verify API keys are properly set in environment
   - Check internet connectivity for cloud services
   - Confirm rate limits are not exceeded

### Performance Optimization
- Use appropriate model sizes for your hardware
- Adjust processing frequency based on real-time requirements
- Monitor system resources and adjust accordingly

## Next Steps

1. Complete the three chapters in sequence:
   - Chapter 1: Voice-to-Action with OpenAI Whisper
   - Chapter 2: Cognitive Planning Using LLMs
   - Chapter 3: Integrating VLA for Autonomous Humanoids

2. Implement the capstone project combining all VLA capabilities

3. Test with different hardware configurations to understand trade-offs

4. Explore advanced features like multi-modal perception and complex task planning