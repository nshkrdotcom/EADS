from dagster import Definitions
from .assets.core_assets import core_assets
from .jobs.core_jobs import core_job

defs = Definitions(
    assets=[*core_assets],
    jobs=[core_job],
)
