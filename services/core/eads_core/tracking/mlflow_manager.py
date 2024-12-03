"""MLflow experiment tracking and model registry manager."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, cast

import mlflow
from mlflow.entities import Run
from mlflow.tracking import MlflowClient


@dataclass
class MLflowConfig:
    """Configuration for MLflow."""

    tracking_uri: str
    experiment_name: str
    registry_uri: Optional[str] = None
    artifacts_uri: Optional[str] = None


class MLflowManager:
    """Manager for MLflow experiment tracking and model registry."""

    def __init__(self, config: MLflowConfig) -> None:
        """Initialize MLflow manager.

        Args:
            config: MLflow configuration
        """
        self.config = config
        mlflow.set_tracking_uri(config.tracking_uri)
        if config.registry_uri:
            mlflow.set_registry_uri(config.registry_uri)

        # Set up experiment
        self.experiment = mlflow.get_experiment_by_name(config.experiment_name)
        if not self.experiment:
            mlflow.create_experiment(
                config.experiment_name, artifact_location=config.artifacts_uri
            )
        mlflow.set_experiment(config.experiment_name)

        self.client = MlflowClient()

    def start_run(
        self, run_name: Optional[str] = None, tags: Optional[Dict[str, str]] = None
    ) -> Run:
        """Start a new MLflow run.

        Args:
            run_name: Optional name for the run
            tags: Optional tags for the run

        Returns:
            Run: MLflow Run object
        """
        run = mlflow.start_run(run_name=run_name, tags=tags)
        return cast(Run, run)

    def log_params(self, params: Dict[str, Any]) -> None:
        """Log parameters for the current run.

        Args:
            params: Parameters to log
        """
        mlflow.log_params(params)

    def log_metrics(
        self, metrics: Dict[str, float], step: Optional[int] = None
    ) -> None:
        """Log metrics for the current run.

        Args:
            metrics: Metrics to log
            step: Optional step number
        """
        mlflow.log_metrics(metrics, step=step)

    def log_artifact(self, local_path: Union[str, Path]) -> None:
        """Log an artifact for the current run.

        Args:
            local_path: Path to the artifact
        """
        mlflow.log_artifact(str(local_path))

    def log_model(
        self,
        model: Any,
        artifact_path: str,
        registered_model_name: Optional[str] = None,
    ) -> None:
        """Log a model for the current run.

        Args:
            model: Model to log
            artifact_path: Path in the artifact store
            registered_model_name: Optional name for model registration
        """
        mlflow.pyfunc.log_model(
            artifact_path,
            python_model=model,
            registered_model_name=registered_model_name,
        )

    def get_run(self, run_id: str) -> Run:
        """Get a run by ID.

        Args:
            run_id: Run ID

        Returns:
            Run: MLflow Run object
        """
        run = self.client.get_run(run_id)
        return cast(Run, run)

    def list_experiments(self) -> List[mlflow.entities.Experiment]:
        """List all experiments.

        Returns:
            List[mlflow.entities.Experiment]: List of experiments
        """
        experiments = self.client.search_experiments()
        return cast(List[mlflow.entities.Experiment], experiments)

    def get_model_version(
        self, name: str, version: str
    ) -> mlflow.entities.model_registry.ModelVersion:
        """Get a specific model version.

        Args:
            name: Model name
            version: Version number

        Returns:
            mlflow.entities.model_registry.ModelVersion: Model version
        """
        return self.client.get_model_version(name, version)

    def list_model_versions(
        self, name: str
    ) -> List[mlflow.entities.model_registry.ModelVersion]:
        """List all versions of a model.

        Args:
            name: Model name

        Returns:
            List[mlflow.entities.model_registry.ModelVersion]: List of model versions
        """
        versions = self.client.search_model_versions(f"name='{name}'")
        return cast(List[mlflow.entities.model_registry.ModelVersion], versions)

    def set_model_version_tag(
        self, name: str, version: str, key: str, value: str
    ) -> None:
        """Set a tag on a model version.

        Args:
            name: Model name
            version: Version number
            key: Tag key
            value: Tag value
        """
        self.client.set_model_version_tag(name, version, key, value)
