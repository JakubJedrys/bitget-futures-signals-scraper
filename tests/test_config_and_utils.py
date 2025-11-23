from datetime import datetime
from pathlib import Path

import pytest

pytest.importorskip("playwright", reason="Playwright nie jest zainstalowany.")
pytest.importorskip("pandas", reason="pandas nie jest zainstalowany.")

import src.config as config_module
from src.bitget_api import get_xrp_futures_1m_df
from src.chart import render_xrp_1m_chart
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


def test_ensure_data_dir_respects_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(config_module.config, "DATA_DIR", tmp_path / "custom" / "SS-XRP")
    created = config_module.ensure_data_dir()
    assert created == config_module.config.DATA_DIR
    assert created.exists()


def test_get_xrp_futures_1m_df_parses_sample(monkeypatch: pytest.MonkeyPatch):
    class DummyResponse:
        def __init__(self, payload):
            self._payload = payload

        def raise_for_status(self):
            return None

        def json(self):
            return self._payload

    sample_data = {
        "data": [
            ["1710000000000", "0.50", "0.55", "0.45", "0.52", "123"],
            ["1710000060000", "0.52", "0.56", "0.50", "0.54", "150"],
        ]
    }

    def fake_get(url, params=None, timeout=10):
        assert "XRPUSDT" in params["symbol"]
        return DummyResponse(sample_data)

    monkeypatch.setattr("requests.get", fake_get)

    df = get_xrp_futures_1m_df(limit=2)
    assert not df.empty
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert len(df) == 2


def test_render_xrp_1m_chart_creates_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    pytest.importorskip("mplfinance", reason="mplfinance nie jest zainstalowane.")
    import pandas as pd

    index = pd.to_datetime(["2024-01-01 00:00", "2024-01-01 00:01"], utc=True)
    df = pd.DataFrame(
        {
            "open": [0.5, 0.52],
            "high": [0.55, 0.56],
            "low": [0.45, 0.50],
            "close": [0.52, 0.54],
            "volume": [123, 150],
        },
        index=index,
    )

    output_path = tmp_path / "chart.png"
    render_xrp_1m_chart(df, output_path)
    assert output_path.exists()
