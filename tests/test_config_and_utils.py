from pathlib import Path
from datetime import datetime

import pytest

from src import config

pytest.importorskip("playwright", reason="Playwright nie jest zainstalowany.")

from src.screenshotter import XrpFuturesCanvasScreenshotter, build_output_path


def test_generate_filename_format():
    screenshotter = XrpFuturesCanvasScreenshotter()
    filename = screenshotter.generate_filename()
    assert filename.startswith("xrp_futures_")
    assert filename.endswith(".png")
    datetime.strptime(filename.removeprefix("xrp_futures_").removesuffix(".png"), "%Y-%m-%d_%H-%M-%S")


def test_build_output_path_creates_directory(tmp_path: Path):
    target_dir = tmp_path / "nested" / "SS-XRP"
    output = build_output_path("example.png", base_dir=target_dir)
    assert output == target_dir / "example.png"
    assert output.parent.exists()


def test_ensure_data_dir_custom_path(tmp_path: Path):
    custom_dir = tmp_path / "custom" / "SS-XRP"
    created = config.ensure_data_dir(custom_dir)
    assert created == custom_dir
    assert custom_dir.exists()
