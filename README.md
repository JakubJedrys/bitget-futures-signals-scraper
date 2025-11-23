# Bitget XRPUSDT Futures Canvas Screenshotter

Aplikacja do automatycznego robienia zrzutów ekranu wykresu kontraktu futures XRPUSDT z Bitget na Windows 11. Zrzuca wyłącznie element `<canvas>` z wykresem i zapisuje go w folderze `SS-XRP` na pulpicie.

## Wymagania
- Python 3.11+ (działa także w innych wersjach 3.x)
- Playwright dla Pythona

## Instalacja
1. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
2. Zainstaluj przeglądarki Playwright:
   ```bash
   python -m playwright install
   ```

## Uruchomienie
- Jeden zrzut:
  ```bash
  python main.py shot
  ```
- Pętla zrzutów co 60 sekund (10 powtórzeń):
  ```bash
  python main.py loop --interval 60 --count 10
  ```
- Tryb bez headless (widoczna przeglądarka):
  ```bash
  python main.py shot --no-headless
  ```

## Gdzie trafiają pliki
Pliki PNG są zapisywane do katalogu:
```
C:\Users\\<nazwa_użytkownika>\\Desktop\\SS-XRP\\xrp_futures_YYYY-MM-DD_HH-MM-SS.png
```
Folder jest tworzony automatycznie, jeżeli jeszcze nie istnieje.
