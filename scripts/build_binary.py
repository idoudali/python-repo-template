"""Build a platform-tagged one-file binary with PyInstaller."""

from __future__ import annotations

from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "packaging" / "pyinstaller" / "python-repo-template.spec"
DIST = ROOT / "dist" / "binaries"


def _platform_tag() -> str:
    """Return an ``<os>-<arch>`` tag for the current machine."""
    system = platform.system().lower()
    machine = platform.machine().lower()
    if machine in {"x86_64", "amd64"}:
        arch = "x86_64"
    elif machine in {"aarch64", "arm64"}:
        arch = "arm64"
    else:
        arch = machine
    return f"{system}-{arch}"


def main() -> int:
    """Run PyInstaller and rename the binary with a platform tag."""
    DIST.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--distpath",
        str(DIST),
        "--workpath",
        str(ROOT / "build" / "pyinstaller"),
        str(SPEC),
    ]
    # cmd is a fixed argv list built above; not shell-interpolated.
    subprocess.run(cmd, check=True, cwd=ROOT)  # noqa: S603
    suffix = ".exe" if platform.system() == "Windows" else ""
    built = DIST / f"python-repo-template{suffix}"
    tagged = DIST / f"python-repo-template-{_platform_tag()}{suffix}"
    if tagged.exists():
        tagged.unlink()
    shutil.move(str(built), str(tagged))
    print(f"Built {tagged}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
