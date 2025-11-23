from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    BITGET_XRP_FUTURES_URL: str = "https://www.bitget.com/pl/futures/usdt/XRPUSDT"

    DESKTOP_DIR: Path = Path.home() / "Desktop"
    DATA_DIR: Path = DESKTOP_DIR / "SS-XRP"

    # Zachowujemy user-agent na potrzeby trybu Playwright.
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )


def ensure_data_dir() -> Path:
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    return config.DATA_DIR


def build_output_path(filename: str, base_dir: Path | None = None) -> Path:
    target_dir = base_dir or config.DATA_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / filename


config = AppConfig()
