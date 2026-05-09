from __future__ import annotations

import importlib
import os
import runpy
import site
import sys
from pathlib import Path


ROUND3_LIMITS = {
    "HYDROGEL_PACK": 200,
    "VELVETFRUIT_EXTRACT": 200,
    "VEV_4000": 300,
    "VEV_4500": 300,
    "VEV_5000": 300,
    "VEV_5100": 300,
    "VEV_5200": 300,
    "VEV_5300": 300,
    "VEV_5400": 300,
    "VEV_5500": 300,
    "VEV_6000": 300,
    "VEV_6500": 300,
}


def _candidate_site_packages() -> list[Path]:
    candidates: list[Path] = []

    def add(path_like: str | Path | None) -> None:
        if not path_like:
            return
        path = Path(path_like)
        if path.exists() and path not in candidates:
            candidates.append(path)

    for entry in sys.path:
        add(entry)

    try:
        add(site.getusersitepackages())
    except Exception:
        pass

    try:
        for path in site.getsitepackages():
            add(path)
    except Exception:
        pass

    local_app_data = Path(os.environ.get("LOCALAPPDATA", ""))
    if local_app_data.exists():
        windows_store_root = local_app_data / "Packages"
        for package_root in windows_store_root.glob("PythonSoftwareFoundation.Python.*"):
            local_cache = package_root / "LocalCache" / "local-packages"
            if not local_cache.exists():
                continue
            for python_root in local_cache.glob("Python*"):
                add(python_root / "site-packages")

    roaming_app_data = Path(os.environ.get("APPDATA", ""))
    if roaming_app_data.exists():
        python_root = roaming_app_data / "Python"
        for version_root in python_root.glob("Python*"):
            add(version_root / "site-packages")

    return candidates


def ensure_package_importable(package_name: str) -> None:
    try:
        importlib.import_module(package_name)
        return
    except ModuleNotFoundError:
        pass

    for candidate in _candidate_site_packages():
        candidate_str = str(candidate)
        if candidate_str not in sys.path:
            sys.path.insert(0, candidate_str)
        try:
            importlib.import_module(package_name)
            return
        except ModuleNotFoundError:
            continue

    raise ModuleNotFoundError(
        f"Could not import '{package_name}'. Checked interpreter paths plus common user site-packages locations."
    )


def patch_prosperity_limits(extra_limits: dict[str, int]) -> None:
    ensure_package_importable("prosperity3bt")

    data_module = importlib.import_module("prosperity3bt.data")
    runner_module = importlib.import_module("prosperity3bt.runner")

    data_module.LIMITS.update(extra_limits)
    runner_module.LIMITS.update(extra_limits)


def run_prosperity3bt_cli(cli_args: list[str], extra_limits: dict[str, int] | None = None) -> int:
    ensure_package_importable("prosperity3bt")
    if extra_limits:
        patch_prosperity_limits(extra_limits)

    previous_argv = sys.argv[:]
    sys.argv = ["prosperity3bt", *cli_args]
    try:
        runpy.run_module("prosperity3bt", run_name="__main__")
        return 0
    except SystemExit as exc:
        code = exc.code
        if isinstance(code, int):
            return code
        return 1 if code else 0
    finally:
        sys.argv = previous_argv
