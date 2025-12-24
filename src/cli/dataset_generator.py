"""
CLI tool for dataset generation in Isaac Robot Brain
"""
import argparse
import os
import sys
from typing import Dict, Any
import yaml

from src.simulation.synthetic_data.generator import SyntheticDatasetGenerator
from src.simulation.isaac_sim.usd_scene import USDScene
from src.simulation.omniverse.domain_randomization_params import DomainRandomizationParams
from src.utils.logging import get_logger


def create_dataset(args: argparse.Namespace):
    """
    Create a synthetic dataset based on command line arguments

    Args:
        args: Parsed command line arguments
    """
    logger = get_logger("dataset_generator")

    logger.info("Starting dataset generation",
                scene_path=args.scene_path,
                output_dir=args.output_dir,
                num_samples=args.num_samples)

    # Validate input paths
    if not os.path.exists(args.scene_path):
        logger.error("Scene file does not exist", scene_path=args.scene_path)
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load domain randomization parameters from file if provided
    domain_randomization_params = DomainRandomizationParams()
    if args.config:
        if not os.path.exists(args.config):
            logger.error("Config file does not exist", config_path=args.config)
            sys.exit(1)

        try:
            with open(args.config, 'r') as f:
                config_data = yaml.safe_load(f)

            # Extract domain randomization parameters
            dr_config = config_data.get('domain_randomization', {})

            lighting_variation = dr_config.get('lighting_variation')
            texture_randomization = dr_config.get('texture_randomization', True)
            environment_objects = dr_config.get('environment_objects', {})
            sensor_noise = dr_config.get('sensor_noise', {'mean': 0.0, 'std': 0.1})
            effectiveness_metric = dr_config.get('effectiveness_metric', 0.0)

            domain_randomization_params = DomainRandomizationParams(
                lighting_variation=lighting_variation,
                texture_randomization=texture_randomization,
                environment_objects=environment_objects,
                sensor_noise=sensor_noise,
                effectiveness_metric=effectiveness_metric
            )
        except Exception as e:
            logger.error("Error loading config file", error=str(e))
            sys.exit(1)

    # Create USDScene object
    try:
        scene_id = f"scene_{hash(args.scene_path) % 1000000}"
        scene_name = os.path.splitext(os.path.basename(args.scene_path))[0]

        scene = USDScene(
            scene_id=scene_id,
            name=scene_name,
            path=args.scene_path,
            description=f"Scene for dataset generation: {args.dataset_name or 'unnamed'}"
        )
    except ValueError as e:
        logger.error("Error creating USD scene", error=str(e))
        sys.exit(1)

    # Create dataset generator
    generator = SyntheticDatasetGenerator()

    # Generate the dataset
    dataset = generator.generate_dataset(
        scene=scene,
        output_dir=args.output_dir,
        num_samples=args.num_samples,
        domain_randomization_params=domain_randomization_params,
        dataset_name=args.dataset_name
    )

    if dataset:
        logger.info("Dataset generation completed successfully",
                    dataset_id=dataset.id,
                    dataset_name=dataset.name,
                    samples_generated=dataset.size)

        # Print summary
        print(f"\nDataset Generation Summary:")
        print(f"  Dataset ID: {dataset.id}")
        print(f"  Dataset Name: {dataset.name}")
        print(f"  Samples Generated: {dataset.size}")
        print(f"  Format: {dataset.format}")
        print(f"  Output Directory: {args.output_dir}")

        if dataset.domain_randomization:
            print(f"  Domain Randomization Applied: Yes")
        else:
            print(f"  Domain Randomization Applied: No")
    else:
        logger.error("Dataset generation failed")
        sys.exit(1)


def main():
    """
    Main function for the dataset generator CLI
    """
    parser = argparse.ArgumentParser(
        description="Generate synthetic datasets for Isaac Robot Brain using Isaac Sim"
    )

    parser.add_argument(
        "--scene-path",
        type=str,
        required=True,
        help="Path to the USD scene file"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Directory to save the generated dataset"
    )

    parser.add_argument(
        "--num-samples",
        type=int,
        default=100,
        help="Number of samples to generate (default: 100)"
    )

    parser.add_argument(
        "--dataset-name",
        type=str,
        help="Name for the generated dataset (auto-generated if not provided)"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to YAML config file with domain randomization parameters"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Set logging level based on verbose flag
    import structlog
    if args.verbose:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.stdlib.filter_by_level,
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.stdlib.BoundLogger,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # Use default logging setup
        pass

    create_dataset(args)


if __name__ == "__main__":
    main()