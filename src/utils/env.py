"""Environment configuration utilities.

This module handles environment variable loading with the following priority:
1. ~/.eads/config (personal overrides)
2. .env (project defaults)
3. existing environment variables
"""

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set, cast

from dotenv import load_dotenv

from .logger import setup_logger

# Set up logger
logger = setup_logger("eads.env")


@dataclass
class ConfigValidation:
    """Configuration validation results."""

    missing_required: List[str]
    invalid_format: Dict[str, str]
    warnings: List[str]

    @property
    def is_valid(self) -> bool:
        """Check if configuration is valid."""
        return not (self.missing_required or self.invalid_format)


class ConfigValidator:
    """Validates environment configuration."""

    # Required variables and their validation patterns
    REQUIRED_VARS = {
        "GOOGLE_API_KEY": r"^[A-Za-z0-9_-]+$",  # Basic API key format
        "XAI_API_KEY": r"^xai-[A-Za-z0-9]+$",  # xAI key format
    }

    # Optional variables and their validation patterns
    OPTIONAL_VARS = {
        "GEMINI_MODEL": r"^gemini-\w+$",
        "GROK_MODEL": r"^grok-[0-9]-\w+$",
    }

    @classmethod
    def validate_env(cls) -> ConfigValidation:
        """Validate environment variables.

        Returns:
            ConfigValidation: Validation results
        """
        missing = []
        invalid = {}
        warnings = []

        # Check required variables
        for var, pattern in cls.REQUIRED_VARS.items():
            value = os.getenv(var)
            if not value:
                missing.append(var)
            elif not re.match(pattern, value):
                invalid[var] = f"Does not match pattern: {pattern}"

        # Check optional variables
        for var, pattern in cls.OPTIONAL_VARS.items():
            value = os.getenv(var)
            if value and not re.match(pattern, value):
                warnings.append(f"{var}: Does not match pattern: {pattern}")

        return ConfigValidation(
            missing_required=missing, invalid_format=invalid, warnings=warnings
        )


def get_user_config_path() -> Path:
    """Get the user-specific configuration path.

    Returns:
        Path: Path to ~/.eads/config
    """
    return Path.home() / ".eads" / "config"


def get_project_env_path() -> Path:
    """Get the project's .env file path.

    Returns:
        Path: Path to project's .env file
    """
    return Path(__file__).parent.parent / ".env"


def ensure_user_config_dir() -> None:
    """Create the user configuration directory if it doesn't exist."""
    config_dir = get_user_config_path().parent
    config_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured config directory exists: {config_dir}")


def load_dotenv_safe(path: Path, override: bool = False) -> Set[str]:
    """Safely load a dotenv file with logging.

    Args:
        path: Path to .env file
        override: Whether to override existing variables

    Returns:
        Set[str]: Set of variables that were loaded
    """
    if not path.exists():
        logger.warning(f"Config file not found: {path}")
        return set()

    try:
        loaded_vars = cast(Set[str], load_dotenv(path, override=override))
        logger.info(f"Loaded {len(loaded_vars)} variables from {path}")
        return loaded_vars
    except Exception as e:
        logger.error(f"Error loading {path}: {str(e)}")
        return set()


def load_env() -> ConfigValidation:
    """Load environment variables with priority.

    1. ~/.eads/config (personal overrides)
    2. .env (project defaults)
    3. existing environment variables

    Returns:
        ConfigValidation: Validation results
    """
    logger.info("Loading environment configuration...")

    # First load project defaults
    project_env = get_project_env_path()
    project_vars = load_dotenv_safe(project_env)
    if project_vars:
        logger.info(f"Loaded project variables: {', '.join(sorted(project_vars))}")

    # Then load personal overrides
    user_config = get_user_config_path()
    user_vars = load_dotenv_safe(user_config, override=True)
    if user_vars:
        logger.info(f"Loaded user variables: {', '.join(sorted(user_vars))}")

    # Validate configuration
    validation = ConfigValidator.validate_env()

    # Log validation results
    if validation.missing_required:
        logger.error(
            f"Missing required variables: {', '.join(validation.missing_required)}"
        )
    if validation.invalid_format:
        logger.error("Invalid variable formats:")
        for var, error in validation.invalid_format.items():
            logger.error(f"  {var}: {error}")
    if validation.warnings:
        logger.warning("Configuration warnings:")
        for warning in validation.warnings:
            logger.warning(f"  {warning}")

    return validation


def get_required_env(key: str) -> str:
    """Get a required environment variable.

    Args:
        key: Environment variable key

    Returns:
        str: Environment variable value

    Raises:
        ValueError: If environment variable is not set or invalid
    """
    value = os.getenv(key)
    if value is None:
        raise ValueError(
            f"Required environment variable {key} is not set. "
            f"Set it in .env or ~/.eads/config"
        )

    # Validate if there's a pattern
    if key in ConfigValidator.REQUIRED_VARS:
        pattern = ConfigValidator.REQUIRED_VARS[key]
        if not re.match(pattern, value):
            raise ValueError(
                f"Environment variable {key} has invalid format. "
                f"Should match pattern: {pattern}"
            )

    return value
