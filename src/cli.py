import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

from .bitget_api import get_xrp_futures_1m_df
from .chart import render_xrp_1m_chart
from .config import config, ensure_data_dir
from .screenshotter import XrpFuturesCanvasScreenshotter


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automatyczne zrzuty ekranu lub wykresy XRPUSDT Futures z Bitget.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    shot_parser = subparsers.add_parser(
        "shot", help="Wykonuje pojedynczy zrzut ekranu canvas z użyciem Playwright."
    )
    shot_parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Uruchamia przeglądarkę w trybie widocznym.",
    )

    loop_parser = subparsers.add_parser(
        "loop", help="Uruchamia pętlę zrzutów ekranu w zadanym interwale."
    )
    loop_parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Interwał (w sekundach) pomiędzy zrzutami w trybie loop.",
    )
    loop_parser.add_argument(
        "--count",
        type=int,
        default=0,
        help="Liczba zrzutów w pętli loop (0 = nieskończona pętla).",
    )
    loop_parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Uruchamia przeglądarkę w trybie widocznym.",
    )

    shot_1m_parser = subparsers.add_parser(
        "shot-1m",
        help="Pobiera świece 1m z API Bitget i zapisuje wykres do pliku PNG.",
    )
    shot_1m_parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="Liczba świeczek 1m do pobrania (domyślnie 200).",
    )

    return parser.parse_args()


def _do_shot(screenshotter: XrpFuturesCanvasScreenshotter, headless: bool) -> Path:
    ensure_data_dir()
    filename = screenshotter.generate_filename()
    output_path = config.DATA_DIR / filename
    screenshotter.take_screenshot(output_path=output_path, headless=headless)
    return output_path


def _loop_shots(
    screenshotter: XrpFuturesCanvasScreenshotter, interval: int, count: int, headless: bool
) -> None:
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


def _cmd_shot_1m(limit: int) -> None:
    data_dir = ensure_data_dir()
    df = get_xrp_futures_1m_df(limit=limit)

    if df.empty:
        print("Błąd: Nie udało się pobrać danych 1m z API Bitget (pusty DataFrame).")
        return

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = data_dir / f"xrp_1m_{now}.png"

    try:
        render_xrp_1m_chart(df, output_path)
        print(f"Wygenerowano wykres 1m i zapisano do pliku: {output_path}")
    except Exception as e:  # pragma: no cover - komunikat użytkownika
        print(f"Błąd podczas generowania wykresu 1m: {e}")


def main() -> None:
    args = _parse_args()
    headless = not getattr(args, "no_headless", False)
    screenshotter = XrpFuturesCanvasScreenshotter()

    try:
        if args.command == "shot":
            output_path = _do_shot(screenshotter, headless)
            print(f"Zapisano zrzut do: {output_path}")
        elif args.command == "loop":
            _loop_shots(screenshotter, args.interval, args.count, headless)
        elif args.command == "shot-1m":
            _cmd_shot_1m(limit=args.limit)
    except RuntimeError as error:
        print(f"Błąd: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
