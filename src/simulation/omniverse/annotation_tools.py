"""
Ground truth annotation tools for Isaac Robot Brain
"""
import json
import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from PIL import Image


class AnnotationTools:
    """
    Tools for generating and managing ground truth annotations
    """

    @staticmethod
    def generate_pose_annotation(camera_pose: Dict[str, float],
                                object_poses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate pose annotations for the current scene state

        Args:
            camera_pose: Dictionary with camera position and orientation
            object_poses: List of object pose dictionaries

        Returns:
            Dictionary with pose annotations
        """
        pose_annotation = {
            'camera_pose': camera_pose,
            'object_poses': object_poses,
            'timestamp': datetime.now().isoformat(),
            'coordinate_system': 'world_frame'
        }

        return pose_annotation

    @staticmethod
    def generate_depth_annotation(depth_map: np.ndarray,
                                 min_depth: float = 0.1,
                                 max_depth: float = 10.0) -> Dict[str, Any]:
        """
        Generate depth annotations from a depth map

        Args:
            depth_map: 2D numpy array representing depth values
            min_depth: Minimum depth value in meters
            max_depth: Maximum depth value in meters

        Returns:
            Dictionary with depth annotations
        """
        depth_annotation = {
            'depth_map': depth_map.tolist(),  # Convert to list for JSON serialization
            'min_depth': min_depth,
            'max_depth': max_depth,
            'unit': 'meters',
            'shape': depth_map.shape,
            'dtype': str(depth_map.dtype)
        }

        return depth_annotation

    @staticmethod
    def generate_semantic_annotation(segmentation_map: np.ndarray,
                                   class_mapping: Optional[Dict[int, str]] = None) -> Dict[str, Any]:
        """
        Generate semantic segmentation annotations

        Args:
            segmentation_map: 2D numpy array with class IDs
            class_mapping: Optional mapping from class IDs to class names

        Returns:
            Dictionary with semantic segmentation annotations
        """
        if class_mapping is None:
            # Default class mapping
            class_mapping = {
                0: 'background',
                1: 'robot',
                2: 'obstacle',
                3: 'furniture',
                4: 'decoration'
            }

        semantic_annotation = {
            'segmentation_map': segmentation_map.tolist(),
            'class_mapping': class_mapping,
            'num_classes': len(class_mapping),
            'shape': segmentation_map.shape,
            'dtype': str(segmentation_map.dtype)
        }

        return semantic_annotation

    @staticmethod
    def generate_instance_annotation(instance_map: np.ndarray,
                                   instance_info: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate instance segmentation annotations

        Args:
            instance_map: 2D numpy array with instance IDs
            instance_info: List of dictionaries with information about each instance

        Returns:
            Dictionary with instance segmentation annotations
        """
        instance_annotation = {
            'instance_map': instance_map.tolist(),
            'instance_info': instance_info,
            'shape': instance_map.shape,
            'dtype': str(instance_map.dtype)
        }

        return instance_annotation

    @staticmethod
    def generate_2d_bounding_boxes(segmentation_map: np.ndarray) -> List[Dict[str, Any]]:
        """
        Generate 2D bounding box annotations from segmentation map

        Args:
            segmentation_map: 2D numpy array with class IDs

        Returns:
            List of bounding box annotations
        """
        bounding_boxes = []

        # Find unique class IDs (excluding background)
        unique_classes = np.unique(segmentation_map)
        unique_classes = unique_classes[unique_classes != 0]  # Exclude background

        for class_id in unique_classes:
            # Find all pixels belonging to this class
            y_coords, x_coords = np.where(segmentation_map == class_id)

            if len(x_coords) > 0 and len(y_coords) > 0:
                # Calculate bounding box
                x_min, x_max = int(np.min(x_coords)), int(np.max(x_coords))
                y_min, y_max = int(np.min(y_coords)), int(np.max(y_coords))

                bbox = {
                    'class_id': int(class_id),
                    'x_min': x_min,
                    'y_min': y_min,
                    'x_max': x_max,
                    'y_max': y_max,
                    'width': x_max - x_min,
                    'height': y_max - y_min,
                    'area': (x_max - x_min) * (y_max - y_min)
                }

                bounding_boxes.append(bbox)

        return bounding_boxes

    @staticmethod
    def generate_optical_flow_annotation(prev_frame: np.ndarray,
                                       curr_frame: np.ndarray) -> Dict[str, Any]:
        """
        Generate optical flow annotations (simplified)

        Args:
            prev_frame: Previous frame image
            curr_frame: Current frame image

        Returns:
            Dictionary with optical flow annotations
        """
        # In a real implementation, this would compute actual optical flow
        # For now, we'll return a simplified version
        height, width = prev_frame.shape[:2]

        # Create dummy flow field
        flow_field = np.zeros((height, width, 2), dtype=np.float32)
        flow_field[:, :, 0] = np.random.uniform(-1.0, 1.0, (height, width))  # x flow
        flow_field[:, :, 1] = np.random.uniform(-1.0, 1.0, (height, width))  # y flow

        optical_flow_annotation = {
            'flow_field': flow_field.tolist(),
            'shape': flow_field.shape,
            'dtype': str(flow_field.dtype),
            'unit': 'pixels'
        }

        return optical_flow_annotation

    @staticmethod
    def save_annotations(annotations: Dict[str, Any],
                        output_path: str,
                        image_filename: Optional[str] = None) -> bool:
        """
        Save annotations to a JSON file

        Args:
            annotations: Dictionary containing all annotations
            output_path: Path to save the annotations
            image_filename: Optional filename of the corresponding image

        Returns:
            True if successful, False otherwise
        """
        try:
            # Add image reference if provided
            if image_filename:
                annotations['image_filename'] = image_filename

            # Add creation timestamp
            annotations['created_at'] = datetime.now().isoformat()

            # Write annotations to file
            with open(output_path, 'w') as f:
                json.dump(annotations, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving annotations: {e}")
            return False

    @staticmethod
    def load_annotations(input_path: str) -> Optional[Dict[str, Any]]:
        """
        Load annotations from a JSON file

        Args:
            input_path: Path to the annotations file

        Returns:
            Dictionary with annotations or None if failed
        """
        try:
            with open(input_path, 'r') as f:
                annotations = json.load(f)
            return annotations
        except Exception as e:
            print(f"Error loading annotations: {e}")
            return None

    @staticmethod
    def validate_annotations(annotations: Dict[str, Any]) -> bool:
        """
        Validate annotation format and content

        Args:
            annotations: Annotations dictionary to validate

        Returns:
            True if valid, False otherwise
        """
        required_keys = ['timestamp', 'camera_pose']
        for key in required_keys:
            if key not in annotations:
                print(f"Missing required key in annotations: {key}")
                return False

        # Validate camera pose structure
        camera_pose = annotations.get('camera_pose', {})
        required_pose_keys = ['x', 'y', 'z', 'roll', 'pitch', 'yaw']
        for key in required_pose_keys:
            if key not in camera_pose:
                print(f"Missing required key in camera pose: {key}")
                return False

        return True

    @staticmethod
    def merge_annotations(annotation_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Merge multiple annotation dictionaries into one

        Args:
            annotation_list: List of annotation dictionaries

        Returns:
            Merged annotation dictionary
        """
        if not annotation_list:
            return {}

        merged = annotation_list[0].copy()

        for annotation in annotation_list[1:]:
            # Merge dictionaries, preferring values from later annotations
            for key, value in annotation.items():
                if key not in merged:
                    merged[key] = value
                elif isinstance(value, dict) and isinstance(merged[key], dict):
                    # Recursively merge nested dictionaries
                    merged[key] = {**merged[key], **value}
                else:
                    # For non-dict values, use the value from the later annotation
                    merged[key] = value

        return merged

    @staticmethod
    def calculate_annotation_statistics(annotations: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate statistics for the annotations

        Args:
            annotations: Annotations dictionary

        Returns:
            Dictionary with annotation statistics
        """
        stats = {
            'total_annotations': len(annotations),
            'has_pose': 'camera_pose' in annotations,
            'has_depth': 'depth_map' in annotations,
            'has_semantic': 'segmentation_map' in annotations,
            'has_objects': 'object_poses' in annotations and len(annotations.get('object_poses', [])) > 0,
            'object_count': len(annotations.get('object_poses', [])),
            'timestamp': annotations.get('timestamp', 'N/A')
        }

        # Calculate depth statistics if available
        if 'depth_map' in annotations:
            depth_map = np.array(annotations['depth_map'])
            stats['depth_stats'] = {
                'min': float(np.min(depth_map)),
                'max': float(np.max(depth_map)),
                'mean': float(np.mean(depth_map)),
                'std': float(np.std(depth_map))
            }

        # Calculate object statistics if available
        if 'object_poses' in annotations:
            object_classes = [obj.get('class', 'unknown') for obj in annotations['object_poses']]
            unique_classes, counts = np.unique(object_classes, return_counts=True)
            stats['object_classes'] = dict(zip(unique_classes, counts.tolist()))

        return stats