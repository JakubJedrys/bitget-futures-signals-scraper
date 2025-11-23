from datetime import datetime
from pathlib import Path
from typing import Optional

from playwright.sync_api import Playwright, TimeoutError as PlaywrightTimeoutError, sync_playwright

from . import config


class XrpFuturesCanvasScreenshotter:
    """Zrzuca canvas wykresu kontraktu XRPUSDT Futures z Bitget."""

    def __init__(self, user_agent: Optional[str] = None) -> None:
        self.user_agent = user_agent or config.AppConfig.USER_AGENT

    def _start_playwright(self) -> Playwright:
        return sync_playwright().start()

    def _stop_playwright(self, playwright_instance: Playwright) -> None:
        playwright_instance.stop()

    def generate_filename(self) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"xrp_futures_{timestamp}.png"

    def take_screenshot(self, output_path: Path, headless: bool = True) -> None:
        playwright_instance = self._start_playwright()
        browser = None
        context = None
        try:
            browser = playwright_instance.chromium.launch(headless=headless)
            context = browser.new_context(
                user_agent=self.user_agent, viewport={"width": 1600, "height": 900}
            )
            page = context.new_page()
            page.goto(
                config.AppConfig.BITGET_XRP_FUTURES_URL, wait_until="networkidle"
            )
            page.wait_for_timeout(3000)

            try:
                canvas_handle = page.wait_for_selector("canvas", timeout=15000)
            except PlaywrightTimeoutError as error:
                raise RuntimeError(
                    "Nie udało się znaleźć elementu canvas z wykresem."
                ) from error

            if canvas_handle is None:
                raise RuntimeError("Nie udało się znaleźć elementu canvas z wykresem.")

            canvas_handle.screenshot(path=str(output_path))
        except PlaywrightTimeoutError as error:
            raise RuntimeError(
                "Przekroczono czas oczekiwania na załadowanie strony lub elementu."
            ) from error
        finally:
            if context is not None:
                context.close()
            if browser is not None:
                browser.close()
            self._stop_playwright(playwright_instance)


def build_output_path(filename: str, base_dir: Optional[Path] = None) -> Path:
    target_dir = base_dir or config.AppConfig.DATA_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / filename
