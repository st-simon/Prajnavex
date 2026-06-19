"""Install or inspect Prajnavex PDF dependencies in the project-local .deps."""

import argparse
import importlib.metadata
import importlib.util
import subprocess
import sys
from importlib.machinery import PathFinder
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEPS = ROOT / ".deps"
REQUIREMENTS = ROOT / "requirements.txt"


def project_pypdf_spec():
    if not DEPS.is_dir():
        return None
    return PathFinder.find_spec("pypdf", [str(DEPS)])


def project_pypdf_version():
    if not project_pypdf_spec():
        return None
    distributions = importlib.metadata.distributions(path=[str(DEPS)])
    for distribution in distributions:
        if distribution.metadata["Name"].lower() == "pypdf":
            return distribution.version
    return "unknown"


def environment_pypdf_version():
    if not importlib.util.find_spec("pypdf"):
        return None
    try:
        return importlib.metadata.version("pypdf")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def install():
    DEPS.mkdir(exist_ok=True)
    command = [
        sys.executable,
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--target",
        str(DEPS),
        "--requirement",
        str(REQUIREMENTS),
        "--upgrade",
    ]
    return subprocess.run(command, cwd=ROOT).returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Report readiness without installing."
    )
    args = parser.parse_args()
    project_version = project_pypdf_version()
    environment_version = environment_pypdf_version()
    if args.check:
        if project_version:
            print(f"ready: pypdf {project_version} (project .deps)")
            return 0
        if environment_version:
            print(f"ready: pypdf {environment_version} (environment)")
            return 0
        print("not ready: run this script without --check")
        return 1
    result = install()
    if result:
        return result
    print(f"installed: pypdf {project_pypdf_version()} (project .deps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
