"""DVC data and model versioning manager."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, cast

import dvc.api
from dvc.repo import Repo


@dataclass
class DVCConfig:
    """Configuration for DVC."""

    repo_path: str
    remote_name: str
    remote_url: str


class DVCManager:
    """Manager for DVC data and model versioning."""

    def __init__(self, config: DVCConfig) -> None:
        """Initialize DVC manager.

        Args:
            config: DVC configuration
        """
        self.config = config
        self.repo = Repo(config.repo_path)

        # Configure remote storage
        if config.remote_name not in self.repo.config["remote"]:
            self.repo.config["remote"][config.remote_name] = {"url": config.remote_url}
        self.repo.config["core"]["remote"] = config.remote_name

    def add_data(self, path: Union[str, Path]) -> None:
        """Add data to DVC tracking.

        Args:
            path: Path to data file or directory
        """
        self.repo.add(str(path))

    def remove_data(self, path: Union[str, Path]) -> None:
        """Remove data from DVC tracking.

        Args:
            path: Path to data file or directory
        """
        self.repo.remove(str(path))

    def push_data(self, path: Optional[Union[str, Path]] = None) -> None:
        """Push tracked data to remote storage.

        Args:
            path: Optional specific path to push
        """
        self.repo.push(targets=[str(path)] if path else None)

    def pull_data(self, path: Optional[Union[str, Path]] = None) -> None:
        """Pull tracked data from remote storage.

        Args:
            path: Optional specific path to pull
        """
        self.repo.pull(targets=[str(path)] if path else None)

    def get_url(self, path: Union[str, Path]) -> str:
        """Get the DVC URL for a tracked file.

        Args:
            path: Path to tracked file

        Returns:
            str: DVC URL
        """
        url = dvc.api.get_url(str(path), repo=self.config.repo_path)
        return cast(str, url)

    def get_hash(self, path: Union[str, Path]) -> str:
        """Get the hash of a tracked file.

        Args:
            path: Path to tracked file

        Returns:
            str: File hash
        """
        hash_value = self.repo.hash_fs.get_hash(str(path))
        return cast(str, hash_value)

    def checkout(self, revision: str) -> None:
        """Checkout a specific DVC revision.

        Args:
            revision: Revision to checkout (commit hash, tag, or branch)
        """
        self.repo.checkout(revision=revision)

    def get_metrics(self) -> Dict[str, Any]:
        """Get tracked metrics.

        Returns:
            Dict[str, Any]: Metrics data
        """
        metrics = self.repo.metrics.show()
        return cast(Dict[str, Any], metrics)

    def add_metric(self, path: Union[str, Path]) -> None:
        """Add a file as a metric.

        Args:
            path: Path to metric file
        """
        self.repo.metrics.add(str(path))

    def get_deps(self, path: Union[str, Path]) -> List[str]:
        """Get dependencies of a tracked file.

        Args:
            path: Path to tracked file

        Returns:
            List[str]: List of dependencies
        """
        deps = self.repo.status([str(path)])["deps"]
        return cast(List[str], deps)

    def get_outs(self, path: Union[str, Path]) -> List[str]:
        """Get outputs of a tracked file.

        Args:
            path: Path to tracked file

        Returns:
            List[str]: List of outputs
        """
        outs = self.repo.status([str(path)])["outs"]
        return cast(List[str], outs)
