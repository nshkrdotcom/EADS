"""Setup script for EADS package."""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="eads",
    version="0.1.0",
    author="EADS Team",
    author_email="team@eads.com",
    description="Evolutionary Algorithm-based Design System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nshkrdotcom/EADS",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black>=23.12.0",
            "flake8>=7.0.0",
            "isort>=5.13.0",
            "mypy>=1.8.0",
            "pre-commit>=3.6.0",
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "eads-nlp=nlp.nlp_service:main",
            "eads-gp=gp_engine.gp_service:main",
        ],
    },
)
