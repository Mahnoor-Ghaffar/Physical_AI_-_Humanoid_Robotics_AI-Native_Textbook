"""
SyntheticDataset model for Isaac Robot Brain
"""
from datetime import datetime
from typing import Dict, Any, Optional
import os


class SyntheticDataset:
    """
    Collection of photorealistic images with ground truth annotations for training perception models
    """

    def __init__(self,
                 dataset_id: str,
                 name: str,
                 size: int,
                 format: str = "PNG",
                 annotations: Optional[Dict[str, Any]] = None,
                 domain_randomization: Optional[Dict[str, Any]] = None):
        """
        Initialize a SyntheticDataset instance

        Args:
            dataset_id: Unique identifier for the dataset
            name: Name of the dataset
            size: Number of images in the dataset
            format: Image format (default: PNG)
            annotations: Ground truth annotations (pose, depth, semantics)
            domain_randomization: Parameters used for randomization
        """
        if size <= 0:
            raise ValueError("Size must be greater than 0")

        if format not in ["PNG", "JPEG", "TIFF", "EXR"]:
            raise ValueError(f"Invalid image format: {format}")

        self.id = dataset_id
        self.name = name
        self.size = size
        self.format = format
        self.annotations = annotations or {}
        self.domain_randomization = domain_randomization or {}
        self.created_at = datetime.now()
        self.path = None

    def validate(self) -> bool:
        """
        Validate the synthetic dataset

        Returns:
            True if valid, False otherwise
        """
        if self.size <= 0:
            return False

        if self.format not in ["PNG", "JPEG", "TIFF", "EXR"]:
            return False

        return True

    def set_path(self, path: str):
        """
        Set the path for the dataset

        Args:
            path: Path to the dataset directory
        """
        if not os.path.exists(path):
            raise ValueError(f"Dataset path does not exist: {path}")

        self.path = path

    def get_annotation_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the annotations in the dataset

        Returns:
            Dictionary with annotation statistics
        """
        stats = {
            'total_annotations': len(self.annotations),
            'pose_annotations': 0,
            'depth_annotations': 0,
            'semantic_annotations': 0,
        }

        for key, value in self.annotations.items():
            if 'pose' in key.lower():
                stats['pose_annotations'] += 1
            elif 'depth' in key.lower():
                stats['depth_annotations'] += 1
            elif 'semantic' in key.lower() or 'seg' in key.lower():
                stats['semantic_annotations'] += 1

        return stats

    def get_dataset_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about the dataset

        Returns:
            Dictionary with dataset information
        """
        return {
            'id': self.id,
            'name': self.name,
            'size': self.size,
            'format': self.format,
            'created_at': self.created_at.isoformat(),
            'annotation_stats': self.get_annotation_stats(),
            'domain_randomization_params': self.domain_randomization,
            'path': self.path
        }

    def __str__(self) -> str:
        """
        String representation of the dataset

        Returns:
            String representation
        """
        return f"SyntheticDataset(id={self.id}, name={self.name}, size={self.size}, format={self.format})"

    def __repr__(self) -> str:
        """
        Detailed string representation of the dataset

        Returns:
            Detailed string representation
        """
        return self.__str__()