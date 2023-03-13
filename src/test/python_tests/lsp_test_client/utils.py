# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""
Utility functions for use with tests.
"""
import contextlib
import json
import os
import pathlib
import platform
import random

from .constants import PROJECT_ROOT


def normalizecase(path: str) -> str:
    """Fixes 'file' uri or path case for easier testing in windows."""
    return path.lower() if platform.system() == "Windows" else path


def as_uri(path: str) -> str:
    """Return 'file' uri as string."""
    return normalizecase(pathlib.Path(path).as_uri())


@contextlib.contextmanager
def python_file(contents: str, root: pathlib.Path, ext: str = ".py"):
    """Creates a temporary python file."""
    basename = (
        "".join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(9)) + ext
    )
    fullpath = root / basename
    try:
        fullpath.write_text(contents)
        yield fullpath
    finally:
        os.unlink(str(fullpath))


def get_server_info_defaults():
    """Returns server info from package.json"""
    package_json_path = PROJECT_ROOT / "package.json"
    package_json = json.loads(package_json_path.read_text())
    return package_json["serverInfo"]


def get_initialization_options():
    """Returns initialization options from package.json"""
    package_json_path = PROJECT_ROOT / "package.json"
    package_json = json.loads(package_json_path.read_text())

    server_info = package_json["serverInfo"]
    server_id = server_info["module"]

    properties = package_json["contributes"]["configuration"]["properties"]
    setting = {
        prop[len(server_id) + 1 :]: properties[prop]["default"]
        for prop in properties
    }
    setting["workspace"] = as_uri(str(PROJECT_ROOT))
    setting["interpreter"] = []
    setting["cwd"] = str(PROJECT_ROOT)
    setting["extraPaths"] = []

    return {"settings": [setting], "globalSettings": setting}
