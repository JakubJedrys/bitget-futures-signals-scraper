# Bitget XRPUSDT Futures Canvas Screenshotter

Aplikacja w Pythonie do automatycznego robienia zrzutów ekranu wykresu kontraktu futures XRPUSDT na giełdzie Bitget (tylko element `<canvas>` z wykresem). Pliki PNG lądują w folderze `SS-XRP` na pulpicie Windows 11.

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
3. (Opcjonalnie) uruchom szybki test konfiguracji:
   ```bash
   python -m pytest
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
C:\Users\<nazwa_użytkownika>\Desktop\SS-XRP\xrp_futures_YYYY-MM-DD_HH-MM-SS.png
```
Folder jest tworzony automatycznie, jeżeli jeszcze nie istnieje.

## Typowe problemy
- Jeśli Playwright nie widzi elementu canvas, upewnij się, że przeglądarki zostały zainstalowane poleceniem `python -m playwright install`.
- Przy pierwszym uruchomieniu na słabszych łączach możesz zwiększyć czas ładowania strony, uruchamiając komendę z przełącznikiem `--no-headless` i sprawdzając, czy wykres jest widoczny.
