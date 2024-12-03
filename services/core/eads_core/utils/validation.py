"""Validation utilities for the core service."""
from typing import Any, Dict, Optional, Tuple

from pydantic import BaseModel, ValidationError


def validate_input(
    data: Dict[str, Any], model: BaseModel, partial: bool = False
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """Validate input data against a Pydantic model.

    Args:
        data: Input data to validate
        model: Pydantic model class
        partial: Allow partial data validation

    Returns:
        Tuple of (is_valid, error_message, validated_data)
    """
    try:
        if partial:
            validated = model.model_validate(data, partial=True)
        else:
            validated = model.model_validate(data)
        return True, None, validated.model_dump()
    except ValidationError as e:
        errors = []
        for error in e.errors():
            loc = " -> ".join(str(x) for x in error["loc"])
            msg = error["msg"]
            errors.append(f"{loc}: {msg}")
        return False, "; ".join(errors), None
