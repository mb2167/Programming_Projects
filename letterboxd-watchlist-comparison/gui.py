import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import re
import requests
from PIL import Image, ImageTk
import io
from utils import parse_runtime

class LetterboxdGUI(tk.Tk):
    def __init__(self, all_watchlists, scrape_callback):
        super().__init__()
        self.all_watchlists = all_watchlists
        self.scrape_callback = scrape_callback  # Function to rescrape
        self.status_label = None

        self.title("Letterboxd Scraper & Comparison")
        self.geometry("420x230")
        self.build_main_frame()
        self.mainloop()

    # --- Main GUI ---
    def build_main_frame(self):
        frame = tk.Frame(self)
        frame.pack(expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Choose an option:").pack(pady=6)
        ttk.Button(frame, text="Rescrape Watchlists", command=self.start_scraping).pack(pady=6, fill="x")
        ttk.Button(frame, text="Go to Comparisons", command=self.open_comparison).pack(pady=6, fill="x")

        self.status_label = ttk.Label(frame, text="")
        self.status_label.pack(pady=6)

    def start_scraping(self):
        self.status_label.config(text="Scraping...")
        self.after(100, lambda: self.scrape_callback(self.on_scrape_done))

    def on_scrape_done(self):
        self.status_label.config(text="Scraping done!")
        self.after(1000, self.open_comparison)

    def open_comparison(self):
        ComparisonGUI(self, self.all_watchlists)


class ComparisonGUI(tk.Toplevel):
    def __init__(self, root, all_watchlists):
        super().__init__(root)
        self.root = root
        self.all_watchlists = all_watchlists

        # --- Shared state ---
        self.selected_vars = {}
        self.exclude_others_var = tk.BooleanVar()
        self.max_runtime_var = tk.StringVar(value="")
        self.current_common_films = []
        self.side_panel = None
        self.panel_open = tk.BooleanVar(value=False)
        self.sort_mode = tk.StringVar(value="alphabetical")
        self.poster_images = []

        # --- Window setup ---
        self.title("Letterboxd – Common Films Viewer")
        self.geometry("500x550")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.main_frame = tk.Frame(self.container, width=500)
        self.main_frame.pack(side="left", fill="both")
        self.main_frame.pack_propagate(False)

        self.build_top_frame()
        self.build_output_listbox()
        self.build_bottom_frame()
        self.update_output()

    # --- Build frames ---
    def build_top_frame(self):
        top_frame = tk.Frame(self.main_frame)
        top_frame.pack(fill="x", padx=10, pady=5)
        top_frame.columnconfigure(0, weight=1, uniform="half")
        top_frame.columnconfigure(1, weight=1, uniform="half")

        # --- User checkboxes ---
        checkbox_frame = ttk.LabelFrame(top_frame, text="Select Users")
        checkbox_frame.grid(row=0, column=0, sticky="nsew", padx=(0,5))
        names = list(self.all_watchlists.keys())
        for idx, name in enumerate(names):
            var = tk.BooleanVar()
            self.selected_vars[name] = var
            row, col = divmod(idx, 2)
            cb = ttk.Checkbutton(checkbox_frame, text=name, variable=var, command=self.update_output)
            cb.grid(row=row, column=col, sticky="w", padx=5, pady=2)

        # --- Random + runtime filter ---
        top_right_frame = tk.Frame(top_frame)
        top_right_frame.grid(row=0, column=1, sticky="nsew", padx=(5,0))
        top_right_frame.rowconfigure(0, weight=1)
        top_right_frame.rowconfigure(1, weight=0)
        top_right_frame.columnconfigure(0, weight=1)

        # Random film frame
        random_frame = ttk.LabelFrame(top_right_frame, text="Random Film")
        random_frame.grid(row=0, column=0, sticky="nsew", pady=(0,5))
        random_frame.columnconfigure(0, weight=1)
        random_frame.rowconfigure(2, weight=1)
        self.random_label = ttk.Label(random_frame, text="None yet", wraplength=180, justify="center")
        self.random_label.grid(row=0, column=0, padx=1, pady=(1,0), sticky="n")
        random_btn = ttk.Button(random_frame, text="Pick Random", command=self.pick_random_film)
        random_btn.grid(row=2, column=0, padx=1, pady=(0,5), sticky="s")

        # Max runtime filter
        runtime_frame = ttk.LabelFrame(top_right_frame, text="Max Runtime Filter", height=50)
        runtime_frame.grid(row=1, column=0, sticky="ew")
        runtime_frame.grid_propagate(False)
        runtime_frame.columnconfigure(0, weight=1)
        runtime_entry = ttk.Entry(runtime_frame, textvariable=self.max_runtime_var, width=10)
        runtime_entry.pack(fill="x", padx=5, pady=5)
        runtime_entry.bind("<KeyRelease>", lambda e: self.update_output())

    def build_output_listbox(self):
        self.output_listbox = tk.Listbox(self.main_frame, selectmode="extended")
        self.output_listbox.pack(fill="both", expand=True, padx=10, pady=(0,10))

    def build_bottom_frame(self):
        bottom_frame = tk.Frame(self.main_frame)
        bottom_frame.pack(fill="x", padx=15, pady=5)

        exclude_cb = ttk.Checkbutton(bottom_frame, text="Exclude films in unchecked users' lists",
                                     variable=self.exclude_others_var, command=self.update_output)
        exclude_cb.pack(side="left")

        self.sort_btn = ttk.Button(bottom_frame, text="Sort: Alphabetical", command=self.toggle_sort)
        self.sort_btn.pack(side="left", padx=10)

        self.open_panel_btn = ttk.Button(bottom_frame, text="➡️ Open Panel", command=self.toggle_side_panel)
        self.open_panel_btn.pack(side="left", padx=10)

    # --- Functional methods ---
    def toggle_sort(self):
        if self.sort_mode.get() == "alphabetical":
            self.sort_mode.set("runtime")
            self.sort_btn.config(text="Sort: Runtime")
        else:
            self.sort_mode.set("alphabetical")
            self.sort_btn.config(text="Sort: Alphabetical")
        self.update_output()

    def pick_random_film(self):
        if self.current_common_films:
            if self.sort_mode.get()=="alphabetical":
                title, year = random.choice(self.current_common_films)
            else:
                title, year, _ = random.choice(self.current_common_films)
            self.random_label.config(text=f"{title} ({year})")
        else:
            self.random_label.config(text="No films available")

    def toggle_side_panel(self):
        if not self.panel_open.get():
            self.geometry("900x550")
            if not self.side_panel:
                # --- Side panel frame ---
                self.side_panel = tk.Frame(self.container, relief="sunken", borderwidth=1, width=400)
                self.side_panel.pack(side="right", fill="y")
                self.side_panel.pack_propagate(False)

                side_label = ttk.Label(self.side_panel, text="Film Details Panel")
                side_label.pack(padx=5, pady=5)

                self.detail_box = scrolledtext.ScrolledText(self.side_panel, wrap=tk.WORD, state="disabled", height=30)
                self.detail_box.pack(fill="both", expand=True, padx=5, pady=5)

                self.poster_images = []

            # Bind listbox select
            self.output_listbox.bind("<<ListboxSelect>>", self.refresh_details)
            self.panel_open.set(True)
            self.open_panel_btn.config(text="Close Panel")
        else:
            if self.side_panel:
                self.side_panel.destroy()
                self.side_panel = None
            self.geometry("500x550")
            self.panel_open.set(False)
            self.open_panel_btn.config(text="Open Panel")

    def refresh_details(self, event=None):
        if not self.side_panel:
            return
        self.detail_box.config(state="normal")
        self.detail_box.delete(1.0, tk.END)
        self.poster_images.clear()

        for idx in self.output_listbox.curselection():
            selected_text = self.output_listbox.get(idx)
            match = re.match(r"(.+?) \((\d*)\)", selected_text)
            if match:
                title, year = match.groups()
                year = year.strip()
                found = False
                for user, films in self.all_watchlists.items():
                    for film in films:
                        if film.get("title","").strip()==title and str(film.get("year","")).strip()==year:
                            found = True
                            self.show_film_details(film, title, year)
                            break
                    if found:
                        break
        self.detail_box.config(state="disabled")

    def show_film_details(self, film, title, year):
        overview = film.get("overview") or "No overview available."
        genres = film.get("genres") or "N/A"
        runtime = film.get("runtime") or "N/A"
        providers = film.get("providers") or "N/A"
        users_with_film = [u for u, fs in self.all_watchlists.items()
                           if any(f.get("title","").strip()==title and str(f.get("year","")).strip()==year for f in fs)]
        users_line = ", ".join(users_with_film)

        self.detail_box.insert(tk.END, f"🎬 {title} ({year})\n")
        self.detail_box.insert(tk.END, f"Users with this film: {users_line}\n")
        self.detail_box.insert(tk.END, f"Genres: {genres}\n")
        self.detail_box.insert(tk.END, f"Runtime: {runtime} min\n")
        self.detail_box.insert(tk.END, f"Providers: {providers}\n")
        self.detail_box.insert(tk.END, f"Overview:\n{overview}\n")

        poster_url = film.get("poster_url")
        if poster_url:
            try:
                response = requests.get(poster_url, timeout=10)
                img_data = response.content
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((200,300))
                photo = ImageTk.PhotoImage(img)
                self.poster_images.append(photo)
                self.detail_box.image_create(tk.END, image=photo)
                self.detail_box.insert(tk.END, "\n----------------------\n")
            except Exception as e:
                print(f"Failed to load poster: {e}")
        else:
            self.detail_box.insert(tk.END, "No poster available.\n----------------------\n")

    # --- Update output ---
    def update_output(self):
        self.current_common_films = []
        selected_users = [u for u, var in self.selected_vars.items() if var.get()]
        self.output_listbox.delete(0, tk.END)
        self.random_label.config(text="None yet")

        if not selected_users:
            self.output_listbox.insert(tk.END, "Select one or more users to view shared films.")
            return

        # Compute common films
        user_sets = [
            set((f["title"], str(f.get("year","")).strip()) for f in self.all_watchlists.get(u, []))
            for u in selected_users
        ]
        common_films = set.intersection(*user_sets) if user_sets else set()

        if self.exclude_others_var.get():
            other_films = set()
            for u in self.all_watchlists:
                if u not in selected_users:
                    other_films.update((f["title"], str(f.get("year","")).strip()) for f in self.all_watchlists[u])
            common_films -= other_films

        # Sorting
        if self.sort_mode.get()=="alphabetical":
            self.current_common_films = sorted(common_films, key=lambda f: f[0])
        else:
            enriched = []
            for title, year in common_films:
                runtime = None
                for user, films in self.all_watchlists.items():
                    for f in films:
                        if f.get("title","").strip()==title and str(f.get("year","")).strip()==year:
                            runtime = parse_runtime(f.get("runtime"))
                            break
                    if runtime is not None:
                        break
                enriched.append((title, year, runtime))
            self.current_common_films = sorted(enriched, key=lambda f: (f[2] if f[2] is not None else 9999, f[0]))

        # Max runtime filter
        max_rt_str = self.max_runtime_var.get().strip()
        if max_rt_str.isdigit():
            max_rt = int(max_rt_str)
            filtered = []
            for item in self.current_common_films:
                if self.sort_mode.get()=="alphabetical":
                    title, year = item
                    runtime = None
                else:
                    title, year, runtime = item
                if runtime is None or runtime <= max_rt:
                    filtered.append(item)
            self.current_common_films = filtered

        # Display
        self.output_listbox.insert(tk.END, f"🎞️ {len(self.current_common_films)} films in common between {', '.join(selected_users)}")
        if self.exclude_others_var.get():
            self.output_listbox.insert(tk.END, " (excluding others)")
        self.output_listbox.insert(tk.END, "------------------------")

        if self.sort_mode.get()=="alphabetical":
            for title, year in self.current_common_films:
                self.output_listbox.insert(tk.END, f"🎬 {title} ({year})")
        else:
            for title, year, runtime in self.current_common_films:
                rt_display = f"{runtime} min" if runtime else "N/A"
                self.output_listbox.insert(tk.END, f"🎬 {title} ({year}) – {rt_display}")
