from PIL import Image, ImageTk
import os


from io import BytesIO
import requests
from PIL import Image, ImageTk


import tkinter as tk
from tkinter import ttk, messagebox

from core import PokedexCore


class PokedexApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pokédex")
        self.geometry("720x460")
        self.minsize(720, 460)

        self.core = PokedexCore()
        self.current_pokemon = None

        # ----- BACKGROUND IMAGE -----
        self.bg_image = Image.open("background.avif")
        self.bg_image = self.bg_image.resize((720, 460))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(self, width=720, height=460, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        
        self.container = ttk.Frame(self.canvas)
        self.container_window = self.canvas.create_window(
            0, 0, anchor="nw", window=self.container
        )

        self._build_ui()
        self._refresh_favorites_list()


    def _build_ui(self):
    
        top = ttk.Frame(self.container, padding=12)
        top.pack(fill="x")

        ttk.Label(top, text="Search Pokémon (name or id):").pack(side="left")

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(top, textvariable=self.search_var, width=28)
        self.search_entry.pack(side="left", padx=(8, 8))
        self.search_entry.bind("<Return>", lambda e: self.on_search())

        ttk.Button(top, text="Search", command=self.on_search).pack(side="left")
        ttk.Button(top, text="Add to Favorites", command=self.on_add_favorite).pack(side="left", padx=(10, 0))

        
        mid = ttk.Frame(self.container, padding=(12, 0, 12, 12))  
        mid.pack(fill="both", expand=True)

        
        results = ttk.LabelFrame(mid, text="Pokémon Info", padding=12)
        results.pack(side="left", fill="both", expand=True, padx=(0, 12))

        self.sprite_label = ttk.Label(results)
        self.sprite_label.pack(anchor="center", pady=(0, 10))
        self.sprite_photo = None  

        self.name_var = tk.StringVar(value="Name: —")
        self.id_var = tk.StringVar(value="ID: —")
        self.types_var = tk.StringVar(value="Types: —")
        self.hw_var = tk.StringVar(value="Height/Weight: —")
        self.stats_var = tk.StringVar(value="Stats: —")

        ttk.Label(results, textvariable=self.name_var, font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(results, textvariable=self.id_var).pack(anchor="w", pady=(6, 0))
        ttk.Label(results, textvariable=self.types_var).pack(anchor="w", pady=(6, 0))
        ttk.Label(results, textvariable=self.hw_var).pack(anchor="w", pady=(6, 0))
        ttk.Label(results, textvariable=self.stats_var, wraplength=420, justify="left").pack(anchor="w", pady=(10, 0))

        ttk.Separator(results).pack(fill="x", pady=12)

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(results, textvariable=self.status_var, foreground="gray").pack(anchor="w")

        
        favs = ttk.LabelFrame(mid, text="Favorites", padding=12)
        favs.pack(side="right", fill="y")

        self.fav_list = tk.Listbox(favs, height=14)
        self.fav_list.pack(fill="both", expand=True)
        self.fav_list.bind("<Double-Button-1>", lambda e: self.on_load_favorite())

        btn_row = ttk.Frame(favs)
        btn_row.pack(fill="x", pady=(10, 0))

        ttk.Button(btn_row, text="Load", command=self.on_load_favorite).pack(side="left", expand=True, fill="x", padx=(0, 6))
        ttk.Button(btn_row, text="Remove", command=self.on_remove_favorite).pack(side="left", expand=True, fill="x")

        ttk.Button(favs, text="Refresh", command=self._refresh_favorites_list).pack(fill="x", pady=(10, 0))




    def _refresh_favorites_list(self):
        self.fav_list.delete(0, tk.END)
        for name in self.core.list_favorites():
            self.fav_list.insert(tk.END, name)

    def _set_sprite_from_url(self, url):
        if not url:
            self.sprite_label.configure(image="")
            self.sprite_photo = None
            return

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            image = Image.open(BytesIO(response.content)).convert("RGBA")
            image = image.resize((120, 120))  

            self.sprite_photo = ImageTk.PhotoImage(image)
            self.sprite_label.configure(image=self.sprite_photo)

        except Exception:
            self.sprite_label.configure(image="")
            self.sprite_photo = None


    def _show_pokemon(self, p):
        
        self.current_pokemon = p
        self._set_sprite_from_url(p.sprite_url)

        self.name_var.set(f"Name: {p.name}")
        self.id_var.set(f"ID: {p.id}")
        self.types_var.set(f"Types: {' / '.join(p.types) if p.types else 'Unknown'}")
        self.hw_var.set(p.height_weight_str())

        
        hp = p.stats.get("hp", "?")
        atk = p.stats.get("attack", "?")
        defense = p.stats.get("defense", "?")
        spa = p.stats.get("special-attack", "?")
        spd = p.stats.get("special-defense", "?")
        spe = p.stats.get("speed", "?")
        self.stats_var.set(f"Stats: HP {hp}, ATK {atk}, DEF {defense}, SpA {spa}, SpD {spd}, SPE {spe}")

    def on_search(self):
        query = self.search_var.get().strip()
        if not query:
            messagebox.showinfo("Search", "Type a Pokémon name or id first.")
            return

        self.status_var.set("Searching...")
        self.update_idletasks()

        p = self.core.search(query)
        if not p:
            self.status_var.set("Not found (or no internet).")
            messagebox.showerror("Not found", "Could not find that Pokémon (or the API is unavailable).")
            return

        self._show_pokemon(p)
        self.status_var.set("Loaded Pokémon successfully.")

    def on_add_favorite(self):
        if not self.current_pokemon:
            messagebox.showinfo("Favorites", "Search a Pokémon first.")
            return

        self.core.add_favorite(self.current_pokemon.name)
        self._refresh_favorites_list()
        self.status_var.set(f"Added {self.current_pokemon.name} to favorites.")

    def on_load_favorite(self):
        sel = self.fav_list.curselection()
        if not sel:
            messagebox.showinfo("Favorites", "Select a favorite first.")
            return

        name = self.fav_list.get(sel[0])
        self.search_var.set(name)
        self.on_search()

    def on_remove_favorite(self):
        sel = self.fav_list.curselection()
        if not sel:
            messagebox.showinfo("Favorites", "Select a favorite first.")
            return

        name = self.fav_list.get(sel[0])
        self.core.remove_favorite(name)
        self._refresh_favorites_list()
        self.status_var.set(f"Removed {name} from favorites.")


if __name__ == "__main__":
    app = PokedexApp()
    app.mainloop()
