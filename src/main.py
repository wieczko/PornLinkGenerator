import re
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import urllib.parse
import urllib.request
import webbrowser


class PornLinkGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Generator linków pornograficznych")
        self.root.geometry("780x620")
        self.root.minsize(600, 500)

        style = ttk.Style()
        style.theme_use("clam")

        main_frame = ttk.Frame(root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.LabelFrame(main_frame, text="Parametry", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(input_frame, text="Słowa kluczowe / kategoria:").grid(row=0, column=0, sticky="w", pady=3)
        self.keywords_entry = ttk.Entry(input_frame, width=50)
        self.keywords_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=3)
        self.keywords_entry.insert(0, "blonde anal")

        ttk.Label(input_frame, text="Tryb wyszukiwania:").grid(row=1, column=0, sticky="w", pady=3)
        self.search_mode = tk.StringVar(value="Losowe filmy z kategorii")
        self.search_mode_combo = ttk.Combobox(
            input_frame,
            textvariable=self.search_mode,
            values=["Losowe filmy z kategorii", "Wyszukiwanie"],
            state="readonly",
            width=28,
        )
        self.search_mode_combo.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=3)

        ttk.Label(input_frame, text="Liczba linków:").grid(row=2, column=0, sticky="w", pady=3)
        self.num_entry = ttk.Spinbox(input_frame, from_=1, to=50, width=10)
        self.num_entry.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=3)
        self.num_entry.set(10)

        input_frame.columnconfigure(1, weight=1)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(btn_frame, text="Generuj linki", command=self.generate).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Otwórz wszystkie", command=self.open_all).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Kopiuj wszystko", command=self.copy_all).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Wyczyść", command=self.clear).pack(side=tk.LEFT)

        result_frame = ttk.LabelFrame(main_frame, text="Wygenerowane linki", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)

        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20, font=("Consolas", 10))
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.links = []

        info = ttk.Label(main_frame, text="Program wyszukuje rzeczywiste filmy z podanej kategorii i pobiera działające linki bezpośrednie do nich z wyników wyszukiwania. Nie dodaje sztucznych dodatkowych kategorii.", foreground="gray")
        info.pack(pady=(8, 0))

    def get_site_templates(self, encoded):
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
        ]

    def open_url(self, url):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode("utf-8", errors="ignore")

    def extract_direct_video_links(self, site_name, query):
        encoded = urllib.parse.quote_plus(query)
        search_urls = {
            "Pornhub": f"https://www.pornhub.com/video/search?search={encoded}",
            "Xvideos": f"https://www.xvideos.com/?k={encoded}",
            "XNXX": f"https://www.xnxx.com/search/{encoded}",
            "SpankBang": f"https://spankbang.com/s/{encoded}/",
            "Eporner": f"https://www.eporner.com/search/{encoded}/",
            "XHamster": f"https://xhamster.com/search/{encoded}",
            "RedTube": f"https://www.redtube.com/?search={encoded}",
            "YouPorn": f"https://www.youporn.com/search/?query={encoded}",
            "Tube8": f"https://www.tube8.com/search.html?q={encoded}",
        }

        if site_name not in search_urls:
            return []

        try:
            html_text = self.open_url(search_urls[site_name])
        except Exception:
            return []

        patterns = {
            "Pornhub": r"https://(?:www\.)?pornhub\.com/view_video\.php\?viewkey=[A-Za-z0-9_\-]+",
            "Xvideos": r"https://(?:www\.)?xvideos\.com/video\d+/[^\s\"'<>]+",
            "XNXX": r"https://(?:www\.)?xnxx\.com/video-[0-9]+/[^\s\"'<>]+",
            "SpankBang": r"https://(?:www\.)?spankbang\.com/[A-Za-z0-9_\-]+/[0-9]+/",
            "Eporner": r"https://(?:www\.)?eporner\.com/video-[0-9]+/[^\s\"'<>]+",
            "XHamster": r"https://(?:www\.)?xhamster\.com/videos/[A-Za-z0-9_\-]+",
            "RedTube": r"https://(?:www\.)?redtube\.com/\d+",
            "YouPorn": r"https://(?:www\.)?youporn\.com/watch/\d+/[A-Za-z0-9_\-]+",
            "Tube8": r"https://(?:www\.)?tube8\.com/[A-Za-z0-9_\-]+/",
        }

        matches = re.findall(patterns.get(site_name, r"https?://[^\s\"'<>]+"), html_text, flags=re.IGNORECASE)
        seen = []
        result = []
        for match in matches:
            normalized = match.rstrip('/').rstrip('"')
            if normalized not in seen and "search" not in normalized.lower() and "google" not in normalized.lower():
                seen.append(normalized)
                result.append(normalized)
        return result[:10]

    def build_valid_search_url(self, site_name, query, page):
        encoded = urllib.parse.quote_plus(query)

        if site_name == "Pornhub":
            return f"https://www.pornhub.com/video/search?search={encoded}&page={page}"
        if site_name == "Xvideos":
            return f"https://www.xvideos.com/?k={encoded}&p={page}" if page > 1 else f"https://www.xvideos.com/?k={encoded}"
        if site_name == "XNXX":
            return f"https://www.xnxx.com/search/{encoded}/{page}" if page > 1 else f"https://www.xnxx.com/search/{encoded}"
        if site_name == "SpankBang":
            return f"https://spankbang.com/s/{encoded}/?page={page}" if page > 1 else f"https://spankbang.com/s/{encoded}/"
        if site_name == "Eporner":
            return f"https://www.eporner.com/search/{encoded}/{page}/" if page > 1 else f"https://www.eporner.com/search/{encoded}/"
        if site_name == "XHamster":
            return f"https://xhamster.com/search/{encoded}?page={page}" if page > 1 else f"https://xhamster.com/search/{encoded}"
        if site_name == "RedTube":
            return f"https://www.redtube.com/?search={encoded}&page={page}"
        if site_name == "YouPorn":
            return f"https://www.youporn.com/search/?query={encoded}&page={page}"
        if site_name == "Tube8":
            return f"https://www.tube8.com/search.html?q={encoded}&page={page}"
        return f"https://www.google.com/search?q={encoded}"

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

        mode = self.search_mode.get()
        self.links = []
        self.result_text.delete(1.0, tk.END)

        if mode == "Losowe filmy z kategorii":
            collected_links = []
            for site_name, _ in self.get_site_templates(urllib.parse.quote_plus(keywords)):
                collected_links.extend(self.extract_direct_video_links(site_name, keywords))

            unique_links = []
            for link in collected_links:
                if link not in unique_links:
                    unique_links.append(link)

            if not unique_links:
                messagebox.showwarning("Brak wyników", "Nie udało się pobrać prawdziwych filmów dla tej kategorii. Spróbuj inną frazę.")
                return

            import random
            if len(unique_links) > num:
                self.links = random.sample(unique_links, num)
            else:
                self.links = unique_links[:num]

            for i, url in enumerate(self.links, start=1):
                self.result_text.insert(tk.END, f"{i}. [Wideo] {url}\n\n")
        else:
            templates = self.get_site_templates(urllib.parse.quote_plus(keywords))
            for i in range(num):
                site_name, _ = templates[i % len(templates)]
                page = (i // len(templates)) + 1
                url = self.build_valid_search_url(site_name, keywords, page)
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
