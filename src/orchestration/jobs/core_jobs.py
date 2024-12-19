"""Core jobs module containing basic Dagster job definitions."""

from dagster import job, op

from ..assets.core_assets import example_asset


@op
def example_op() -> str:
    """An example operation that returns a simple string.

    Returns:
        str: A simple message
    """
    return "Example operation"


@job
def core_job() -> None:
    """A simple job that runs both the example operation and asset."""
    example_op()
    example_asset()
