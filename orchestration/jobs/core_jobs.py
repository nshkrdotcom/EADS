from dagster import job, op
from ..assets.core_assets import example_asset

@op
def example_op():
    """An example operation that returns a simple string."""
    return "Example operation"

@job
def core_job():
    """A simple job that runs both the example operation and asset."""
    example_op()
    example_asset()
