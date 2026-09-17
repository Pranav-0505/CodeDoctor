from setuptools import setup, find_packages

setup(
    name="codedoctor-cli",
    version="1.0.0",
    description="Code Doctor CLI — Universal Intelligent Code Diagnosis & Repair Platform",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "codedoctor=codedoctor.main:main",
        ],
    },
    install_requires=[
        "rich>=12.0.0"
    ]
)
