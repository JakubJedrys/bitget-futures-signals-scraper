"""Pobieranie danych 1m XRPUSDT Futures z API Bitget."""

import requests
import pandas as pd


API_URL = "https://api.bitget.com/api/v2/mix/market/candles"


def get_xrp_futures_1m_df(limit: int = 200) -> pd.DataFrame:
    """
    Pobiera świece 1m XRPUSDT USDT-FUTURES z API Bitget i zwraca je
    jako DataFrame z kolumnami: ['open', 'high', 'low', 'close', 'volume']
    oraz indeksem typu datetime (UTC).
    """
    params = {
        "symbol": "XRPUSDT",
        "productType": "USDT-FUTURES",
        "granularity": "1m",
        "limit": limit,
    }

    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
        raw = resp.json().get("data", [])
    except Exception as e:  # pragma: no cover - defensywne logowanie
        print(f"Błąd podczas pobierania danych z API Bitget: {e}")
        return pd.DataFrame()

    if not raw:
        return pd.DataFrame()

    rows = []
    for item in raw:
        ts = int(item[0])
        o = float(item[1])
        h = float(item[2])
        l = float(item[3])
        c = float(item[4])
        v = float(item[5]) if len(item) > 5 else 0.0
        rows.append((ts, o, h, l, c, v))

    df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "volume"])
    df["datetime"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    df = df.set_index("datetime").sort_index()
    return df[["open", "high", "low", "close", "volume"]]
