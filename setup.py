from distutils.core import setup
from pathlib import Path

script_path = Path(__file__).parent


def read_requirements_file() -> list:
    with open(Path(script_path, "requirements.txt"), "r") as f:
        return f.read()


requirements = read_requirements_file()

setup(
    name="ashp-shortage-ndc-web-scraper",
    version="0.1.0",
    author="stepheku",
    license="LICENSE.txt",
    long_description=open("README.md").read(),
    install_requires=requirements,
)
