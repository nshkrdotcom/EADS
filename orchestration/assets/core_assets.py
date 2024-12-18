"""Core assets module containing basic Dagster asset definitions."""

from dagster import asset


@asset
def example_asset() -> str:
    """An example asset that returns a simple greeting.

    Returns:
        str: A greeting message
    """
    return "Hello from EADS Dagster!"


core_assets = [example_asset]
