"""
Logging infrastructure for simulation and navigation
"""
import logging
import structlog
from typing import Dict, Any
from pathlib import Path
import os
from .config import get_config


def setup_logging():
    """
    Setup structured logging for the Isaac Robot Brain system
    """
    # Configure structlog
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

    # Get config
    config = get_config()

    # Setup basic logging configuration
    log_level = getattr(logging, config.get('logging.level', 'INFO'))
    log_file = config.get('logging.file_path', 'logs/robot_brain.log')

    # Create log directory if it doesn't exist
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Configure root logger
    logging.basicConfig(
        level=log_level,
        format=config.get('logging.format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a configured logger instance

    Args:
        name: Name of the logger

    Returns:
        Configured logger instance
    """
    return structlog.get_logger(name)


def log_simulation_event(
    event_type: str,
    robot_id: str,
    simulation_step: int,
    additional_data: Dict[str, Any] = None
) -> None:
    """
    Log a simulation-specific event

    Args:
        event_type: Type of simulation event
        robot_id: ID of the robot involved
        simulation_step: Current simulation step
        additional_data: Additional event-specific data
    """
    logger = get_logger("simulation")

    log_data = {
        'event_type': event_type,
        'robot_id': robot_id,
        'simulation_step': simulation_step,
        'additional_data': additional_data or {}
    }

    logger.info("simulation_event", **log_data)


def log_navigation_event(
    event_type: str,
    robot_id: str,
    position: Dict[str, float],
    additional_data: Dict[str, Any] = None
) -> None:
    """
    Log a navigation-specific event

    Args:
        event_type: Type of navigation event
        robot_id: ID of the robot involved
        position: Current position of the robot (x, y, theta)
        additional_data: Additional event-specific data
    """
    logger = get_logger("navigation")

    log_data = {
        'event_type': event_type,
        'robot_id': robot_id,
        'position': position,
        'additional_data': additional_data or {}
    }

    logger.info("navigation_event", **log_data)


def log_vslam_event(
    event_type: str,
    pipeline_id: str,
    performance_metrics: Dict[str, float],
    additional_data: Dict[str, Any] = None
) -> None:
    """
    Log a VSLAM-specific event

    Args:
        event_type: Type of VSLAM event
        pipeline_id: ID of the VSLAM pipeline
        performance_metrics: Performance metrics (FPS, accuracy, etc.)
        additional_data: Additional event-specific data
    """
    logger = get_logger("vslam")

    log_data = {
        'event_type': event_type,
        'pipeline_id': pipeline_id,
        'performance_metrics': performance_metrics,
        'additional_data': additional_data or {}
    }

    logger.info("vslam_event", **log_data)


# Initialize logging when module is imported
setup_logging()