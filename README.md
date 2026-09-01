# Generator linków pornograficznych

Prosty program z GUI (Tkinter) generujący linki wyszukiwania na popularnych stronach pornograficznych na podstawie słów kluczowych.

## Wymagania

- Python 3.8+ (zalecany 3.10+)
- Tylko standardowa biblioteka Pythona (Tkinter jest wbudowany)

## Jak otworzyć w IntelliJ IDEA / PyCharm

1. Otwórz **IntelliJ IDEA** (z pluginem Python) lub **PyCharm**.
2. Wybierz **File → Open...**
3. Wskaż folder `PornLinkGenerator` (ten, który zawiera `src/` i ten README).
4. IntelliJ/PyCharm automatycznie wykryje projekt Python.
5. Ustaw interpreter Pythona (File → Project Structure → Project → SDK lub w ustawieniach).
6. Otwórz plik `src/main.py`.
7. Kliknij prawym przyciskiem → **Run 'main'** lub użyj zielonej strzałki.

Alternatywnie możesz uruchomić z terminala:

```bash
cd PornLinkGenerator
python src/main.py
```

## Funkcje

- Wpisujesz słowa kluczowe (np. `blonde anal`, `milf japanese`)
- Podajesz liczbę linków (1–50)
- Program generuje linki do wyszukiwarek: Pornhub, Xvideos, XNXX, SpankBang, Eporner, XHamster, RedTube, YouPorn, Tube8 + Google dork
- Możesz otworzyć wszystkie linki w przeglądarce lub skopiować je do schowka

## Uwagi

- Program generuje **linki do stron wyników wyszukiwania**, nie bezpośrednie linki do konkretnych filmów.
- Nie wymaga żadnych zewnętrznych bibliotek.
- Działa na Windows, macOS i Linux.
