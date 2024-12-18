from dagster import asset

@asset
def example_asset():
    """An example asset that returns a simple greeting."""
    return "Hello from EADS Dagster!"

core_assets = [example_asset]
