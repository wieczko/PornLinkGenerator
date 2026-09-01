import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import urllib.parse
import webbrowser


class PornLinkGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Generator linków pornograficznych")
        self.root.geometry("780x620")
        self.root.minsize(600, 500)

        # Style
        style = ttk.Style()
        style.theme_use("clam")

        main_frame = ttk.Frame(root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Wejście ---
        input_frame = ttk.LabelFrame(main_frame, text="Parametry", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text="Słowa kluczowe / kategoria:").grid(row=0, column=0, sticky="w", pady=3)
        self.keywords_entry = ttk.Entry(input_frame, width=50)
        self.keywords_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=3)
        self.keywords_entry.insert(0, "blonde anal")

        ttk.Label(input_frame, text="Liczba linków:").grid(row=1, column=0, sticky="w", pady=3)
        self.num_entry = ttk.Spinbox(input_frame, from_=1, to=50, width=10)
        self.num_entry.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=3)
        self.num_entry.set(10)

        input_frame.columnconfigure(1, weight=1)

        # Przyciski
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text="Generuj linki", command=self.generate).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Otwórz wszystkie", command=self.open_all).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Kopiuj wszystko", command=self.copy_all).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Wyczyść", command=self.clear).pack(side=tk.LEFT)

        # Wyniki
        result_frame = ttk.LabelFrame(main_frame, text="Wygenerowane linki", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20, font=("Consolas", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.links = []

        # Info
        info = ttk.Label(main_frame, text="Program generuje linki do stron wyszukiwania (nie bezpośrednie filmy). Działa stabilnie.", foreground="gray")
        info.pack(pady=(8, 0))

    def get_site_templates(self, encoded):
        """Szablony URL-i wyszukiwania na różnych stronach"""
        return [
            ("Pornhub", f"https://www.pornhub.com/video/search?search={encoded}"),
            ("Xvideos", f"https://www.xvideos.com/?k={encoded}"),
            ("XNXX", f"https://www.xnxx.com/search/{encoded}"),
            ("SpankBang", f"https://spankbang.com/s/{encoded}/"),
            ("Eporner", f"https://www.eporner.com/search/{encoded}/"),
            ("XHamster", f"https://xhamster.com/search/{encoded}"),
            ("RedTube", f"https://www.redtube.com/?search={encoded}"),
            ("YouPorn", f"https://www.youporn.com/search/?query={encoded}"),
            ("Tube8", f"https://www.tube8.com/search.html?q={encoded}"),
            ("Google (site:pornhub)", f"https://www.google.com/search?q={encoded}+site:pornhub.com"),
        ]

    def generate(self):
        keywords = self.keywords_entry.get().strip()
        if not keywords:
            messagebox.showwarning("Brak danych", "Wpisz słowa kluczowe!")
            return

        try:
            num = int(self.num_entry.get())
            if num < 1 or num > 50:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Błąd", "Liczba linków musi być liczbą od 1 do 50.")
            return

        encoded = urllib.parse.quote_plus(keywords)
        templates = self.get_site_templates(encoded)

        self.links = []
        self.result_text.delete(1.0, tk.END)

        # Generujemy linki: najpierw podstawowe, potem z numerami stron / losowymi wariantami
        for i in range(num):
            site_name, base_url = templates[i % len(templates)]

            # Dodajemy warianty stron (page) żeby były bardziej zróżnicowane
            page = (i // len(templates)) + 1
            if "pornhub.com" in base_url:
                url = f"{base_url}&page={page}"
            elif "xvideos.com" in base_url:
                url = f"{base_url}&p={page}" if page > 1 else base_url
            elif "xnxx.com" in base_url:
                url = f"{base_url}/{page}" if page > 1 else base_url
            elif "spankbang.com" in base_url:
                url = f"{base_url}?page={page}" if page > 1 else base_url
            elif "eporner.com" in base_url:
                url = f"{base_url}{page}/" if page > 1 else base_url
            else:
                url = base_url

            self.links.append(url)
            self.result_text.insert(tk.END, f"{i+1}. [{site_name}] {url}\n\n")

        self.result_text.see(1.0)
        messagebox.showinfo("Gotowe", f"Wygenerowano {len(self.links)} linków.")

    def open_all(self):
        if not self.links:
            messagebox.showinfo("Info", "Najpierw wygeneruj linki.")
            return
        for link in self.links:
            webbrowser.open(link)

    def copy_all(self):
        if not self.links:
            messagebox.showinfo("Info", "Najpierw wygeneruj linki.")
            return
        text = "\n".join(self.links)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Skopiowano", "Wszystkie linki skopiowane do schowka.")

    def clear(self):
        self.result_text.delete(1.0, tk.END)
        self.links = []


if __name__ == "__main__":
    root = tk.Tk()
    app = PornLinkGenerator(root)
    root.mainloop()
