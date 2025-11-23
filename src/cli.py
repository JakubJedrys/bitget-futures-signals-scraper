import argparse
import sys
import time

from .config import AppConfig, ensure_data_dir
from .screenshotter import XrpFuturesCanvasScreenshotter


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automatyczne zrzuty ekranu wykresu XRPUSDT Futures z Bitget."
    )

    parser.add_argument(
        "command",
        choices=["shot", "loop"],
        help="shot wykonuje pojedynczy zrzut, loop uruchamia pętlę zrzutów.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Interwał (w sekundach) pomiędzy zrzutami w trybie loop.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=0,
        help="Liczba zrzutów w pętli loop (0 = nieskończona pętla).",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Uruchamia przeglądarkę w trybie widocznym.",
    )

    return parser.parse_args()


def _do_shot(screenshotter: XrpFuturesCanvasScreenshotter, headless: bool) -> Path:
    ensure_data_dir()
    filename = screenshotter.generate_filename()
    output_path = AppConfig.DATA_DIR / filename
    screenshotter.take_screenshot(output_path=output_path, headless=headless)
    return output_path


def _loop_shots(screenshotter: XrpFuturesCanvasScreenshotter, interval: int, count: int, headless: bool) -> None:
    iteration = 0
    try:
        while True:
            if count and iteration >= count:
                break

            output_path = _do_shot(screenshotter, headless)
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] Zapisano zrzut do: {output_path}")
            iteration += 1
            if count and iteration >= count:
                break
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Przerwano pętlę przez użytkownika.")


def main() -> None:
    args = _parse_args()
    headless = not args.no_headless
    screenshotter = XrpFuturesCanvasScreenshotter()

    try:
        if args.command == "shot":
            output_path = _do_shot(screenshotter, headless)
            print(f"Zapisano zrzut do: {output_path}")
        elif args.command == "loop":
            _loop_shots(screenshotter, args.interval, args.count, headless)
    except RuntimeError as error:
        print(f"Błąd: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
