import os
import sys
from pathlib import Path
from importlib.metadata import metadata

import PyInstaller.__main__  # type: ignore
import certifi
import pykakasi
import tls_client
import yt_dlp
import ytmusicapi

from spotdl._version import __version__

LOCALES_PATH = str((Path(ytmusicapi.__file__).parent / "locales"))
PYKAKASI_PATH = str((Path(pykakasi.__file__).parent / "data"))
YTDLP_PATH = str(Path(yt_dlp.__file__).parent / "__pyinstaller")
TLS_CLIENT_DEPS_PATH = str(Path(tls_client.__file__).parent / "dependencies")
CERTIFI_PATH = str(Path(certifi.__file__).parent)

# Read modules from pyproject.toml
modules = set(
    module.split(" ")[0] for module in metadata("spotdl").get_all("Requires-Dist", [])
)

PyInstaller.__main__.run(
    [
        "spotdl/__main__.py",
        "--onefile",
        "--add-data",
        f"{LOCALES_PATH}{os.pathsep}ytmusicapi/locales",
        "--add-data",
        f"{PYKAKASI_PATH}{os.pathsep}pykakasi/data",
        "--add-binary",
        f"{TLS_CLIENT_DEPS_PATH}{os.pathsep}tls_client/dependencies",
        "--add-data",
        f"{CERTIFI_PATH}{os.pathsep}certifi",
        f"--additional-hooks-dir={YTDLP_PATH}",
        "--runtime-hook",
        "scripts/hook-runtime-certifi.py",
        "--name",
        f"spotdl-{__version__}-{sys.platform}",
        "--console",
        *(f"--collect-all={module}" for module in modules),
    ]
)
