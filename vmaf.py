from rich.console import Console
from pathlib import Path
from shutil import which
import subprocess
import re

console = Console()


def get_ffmpeg() -> str:
    path = which("ffmpeg")
    if path is None:
        console.print("[bold red]ffmpeg not found in PATH[/bold red]")
        raise SystemExit(1)
    return path


def build_vmaf(distorted: Path, reference: Path) -> list:
    cmd = [
        get_ffmpeg(),
        "-i",
        distorted,
        "-i",
        reference,
        "-lavfi",
        "libvmaf=n_threads=0",
        "-f",
        "null",
        "-",
    ]

    return cmd


def run_vmaf(command: list) -> float | None:
    output = subprocess.run(command, capture_output=True, text=True)

    if output is None:
        return 0.0

    for line in output.stderr.splitlines():
        match = re.search(r"VMAF score: (\d+\.\d+)", line)

        if match:
            return round(float(match.group(1)), 2)


def vmaf(distorted, reference):
    cmd = build_vmaf(distorted, reference)
    score = run_vmaf(cmd)
    return score
