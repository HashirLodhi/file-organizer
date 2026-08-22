from setuptools import setup, find_packages

setup(
    name="file-organizer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "file-organize=file_organizer.cli:main",
        ],
    },
    author="Your Name",
    description="A CLI tool to organize files by type or date",
    python_requires=">=3.7",
)
