"""Generowanie wykresów świecowych z danych API Bitget."""

from pathlib import Path

import mplfinance as mpf
import pandas as pd


def render_xrp_1m_chart(df: pd.DataFrame, output_path: Path) -> None:
    """
    Renderuje wykres świecowy (candlestick) dla danych 1m z DataFrame
    i zapisuje go do pliku PNG pod podaną ścieżką.
    DataFrame musi mieć index typu datetime oraz kolumny:
    ['open', 'high', 'low', 'close', 'volume'].
    """
    if df.empty:
        raise ValueError("DataFrame z danymi jest pusty – brak danych do narysowania wykresu.")

    mpf.plot(
        df,
        type="candle",
        volume=True,
        style="charles",
        tight_layout=True,
        savefig=dict(fname=str(output_path), dpi=120),
    )
