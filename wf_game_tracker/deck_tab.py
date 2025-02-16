# deck_tab.py

import tkinter as tk
from tkinter import ttk


###############################################################################
# The DeckTab widget: displays a single deck (factions, warlords, summary).
# We update cells in-place (no flicker).
###############################################################################
class DeckTab(tk.Frame):
    def __init__(self, parent, deck_obj, app):
        """
        parent: the ttk.Frame we attach to
        deck_obj: the deck dictionary (with "deck_name", "factions" list, etc.)
        app: reference to the main application (for saving, etc.)
        """
        super().__init__(parent)
        self.app = app
        self.deck_obj = deck_obj
        self.label_refs = {}
        self.faction_wr_labels = {}

        # Build the UI
        self.build_ui()

        # Now that canvas exists, bind scroll wheel
        self._bind_scroll_wheel()

    def build_ui(self):
        title_frame = ttk.Frame(self)
        title_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(title_frame, text="Deck Title:").pack(side=tk.LEFT)
        entry_title = ttk.Entry(title_frame, width=40)
        entry_title.insert(0, self.deck_obj.get("deck_name", "Unnamed Deck"))
        entry_title.pack(side=tk.LEFT, padx=5)

        def update_deck_name(*_):
            self.deck_obj["deck_name"] = entry_title.get()
            idx = self.app.notebook.index(self)
            self.app.notebook.tab(idx, text=entry_title.get())

        entry_title.bind("<KeyRelease>", update_deck_name)

        self.pack(fill=tk.BOTH, expand=True)  # Ensure DeckTab expands
        self.grid_rowconfigure(0, weight=1)  # Allow vertical expansion
        self.grid_columnconfigure(0, weight=1)

        # Scrollable container
        container = ttk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)
        container.pack_propagate(False)  # Prevent container from resizing unnecessarily

        self.canvas = tk.Canvas(container)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Inner frame within the canvas
        self.inner_frame = ttk.Frame(self.canvas)
        self.inner_frame_id = self.canvas.create_window(
            (0, 0), window=self.inner_frame, anchor="nw"
        )

        self.inner_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # Ensure the frame inside the canvas resizes properly
        self.inner_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self._bind_scroll_wheel()

        self.build_faction_rows()
        self.build_summary_rows()

    def build_faction_rows(self):
        headers = [
            "Faction",
            "Warlord",
            "Matches",
            "Off. Wins",
            "Off. Losses",
            "Def. Wins",
            "Def. Losses",
            "Total Wins",
            "Total Losses",
            "Win Rate",
        ]
        for col_idx, hdr in enumerate(headers):
            lbl = tk.Label(
                self.inner_frame,
                text=hdr,
                bg="#aaa",
                fg="black",
                width=17,
                relief=tk.RIDGE,
                borderwidth=1,
            )
            lbl.grid(row=0, column=col_idx, sticky="nsew")

        row_counter = 1
        for faction_data in self.deck_obj["factions"]:
            faction_name = faction_data["faction_name"]
            warlords = faction_data["warlords"]
            n_warlords = len(warlords)

            # Merged Faction cell
            faction_lbl = tk.Label(
                self.inner_frame,
                text=faction_name,
                bg="#cce",
                relief=tk.RIDGE,
                borderwidth=1,
            )
            faction_lbl.grid(
                row=row_counter,
                column=0,
                rowspan=n_warlords,
                sticky="nsew",
                padx=1,
                pady=1,
            )

            for i, wlord in enumerate(warlords):
                current_row = row_counter + i
                # Warlord name
                lbl_warlord = tk.Label(
                    self.inner_frame,
                    text=wlord["warlord_name"],
                    bg="#eef",
                    relief=tk.RIDGE,
                    borderwidth=1,
                )
                lbl_warlord.grid(
                    row=current_row, column=1, sticky="nsew", padx=1, pady=1
                )

                # Create dynamic labels for stats
                self.create_stat_cells(current_row, wlord, faction_data)

            row_counter += n_warlords

    def create_stat_cells(self, row, wlord, faction_data):
        """Create labels for stats and store them for updating later."""

        # Matches
        lbl_matches = tk.Label(
            self.inner_frame, bg="#fff", relief=tk.RIDGE, borderwidth=1
        )
        lbl_matches.grid(row=row, column=2, sticky="nsew", padx=1, pady=1)
        self.label_refs[(row, "matches")] = lbl_matches

        # Off. Wins
        self.make_clickable_stat(row, 3, wlord, "off_wins", bg="#bfb")

        # Off. Losses
        self.make_clickable_stat(row, 4, wlord, "off_losses", bg="#fbb")

        # Def. Wins
        self.make_clickable_stat(row, 5, wlord, "def_wins", bg="#bfb")

        # Def. Losses
        self.make_clickable_stat(row, 6, wlord, "def_losses", bg="#fbb")

        # Total Wins
        lbl_total_wins = tk.Label(
            self.inner_frame, bg="#dfd", relief=tk.RIDGE, borderwidth=1
        )
        lbl_total_wins.grid(row=row, column=7, sticky="nsew", padx=1, pady=1)
        self.label_refs[(row, "tot_wins")] = lbl_total_wins

        # Total Losses
        lbl_total_losses = tk.Label(
            self.inner_frame, bg="#fdd", relief=tk.RIDGE, borderwidth=1
        )
        lbl_total_losses.grid(row=row, column=8, sticky="nsew", padx=1, pady=1)
        self.label_refs[(row, "tot_losses")] = lbl_total_losses

        # Win Rate
        lbl_win_rate = tk.Label(
            self.inner_frame, bg="#eee", relief=tk.RIDGE, borderwidth=1
        )
        lbl_win_rate.grid(row=row, column=9, sticky="nsew", padx=1, pady=1)
        self.label_refs[(row, "win_rate")] = lbl_win_rate

        # Initial update
        self.update_warlord_row(row, wlord)

    def make_clickable_stat(self, row, col, wlord_dict, key, bg):
        """Create a clickable stat label that updates when clicked."""
        lbl = tk.Label(self.inner_frame, bg=bg, relief=tk.RIDGE, borderwidth=1)
        lbl.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

        # Store label reference for updating
        self.label_refs[(row, key)] = lbl

        # Left-click increases value, right-click decreases
        lbl.bind(
            "<Button-1>",
            lambda _evt: self.update_warlord_row(row, wlord_dict, key, delta=1),
        )
        lbl.bind(
            "<Button-3>",
            lambda _evt: self.update_warlord_row(row, wlord_dict, key, delta=-1),
        )

        lbl.config(text=str(wlord_dict[key]))  # Set initial value

    def update_warlord_row(self, row, wlord_dict, key=None, delta=0):
        """
        Updates a warlord's row stats and increments/decrements a value if key and delta are provided.
        """
        if key is not None:
            # Apply change if key and delta are provided
            wlord_dict[key] += delta

        # Calculate updated values
        ow = wlord_dict["off_wins"]
        ol = wlord_dict["off_losses"]
        dw = wlord_dict["def_wins"]
        dl = wlord_dict["def_losses"]

        matches = ow + ol + dw + dl
        tot_wins = ow + dw
        tot_losses = ol + dl
        win_rate = (100.0 * tot_wins / matches) if matches > 0 else 0.0

        # Update labels
        self.label_refs[(row, "matches")].config(text=str(matches))
        self.label_refs[(row, "off_wins")].config(text=str(ow))
        self.label_refs[(row, "off_losses")].config(text=str(ol))
        self.label_refs[(row, "def_wins")].config(text=str(dw))
        self.label_refs[(row, "def_losses")].config(text=str(dl))
        self.label_refs[(row, "tot_wins")].config(text=str(tot_wins))
        self.label_refs[(row, "tot_losses")].config(text=str(tot_losses))
        self.label_refs[(row, "win_rate")].config(text=f"{win_rate:.1f}%")

    def create_summary_line(self, row, summary_dict, highlight_bg):
        lbl_m = tk.Label(
            self.inner_frame,
            bg=highlight_bg,
            fg="white",
            relief=tk.RIDGE,
            borderwidth=1,
        )
        lbl_m.grid(row=row, column=2, sticky="nsew")
        summary_dict["matches"] = lbl_m

        lbl_w = tk.Label(
            self.inner_frame,
            bg=highlight_bg,
            fg="white",
            relief=tk.RIDGE,
            borderwidth=1,
        )
        lbl_w.grid(row=row, column=3, sticky="nsew")
        summary_dict["wins"] = lbl_w

        lbl_l = tk.Label(
            self.inner_frame,
            bg=highlight_bg,
            fg="white",
            relief=tk.RIDGE,
            borderwidth=1,
        )
        lbl_l.grid(row=row, column=4, sticky="nsew")
        summary_dict["losses"] = lbl_l

        lbl_wr = tk.Label(
            self.inner_frame,
            bg=highlight_bg,
            fg="white",
            relief=tk.RIDGE,
            borderwidth=1,
        )
        lbl_wr.grid(row=row, column=5, columnspan=5, sticky="nsew")
        summary_dict["win_rate"] = lbl_wr

    def update_summary_rows(self):
        off_matches = off_wins = off_losses = 0
        def_matches = def_wins = def_losses = 0
        total_matches = total_wins = total_losses = 0

        for faction_data in self.deck_obj["factions"]:
            for w in faction_data["warlords"]:
                ow = w["off_wins"]
                ol = w["off_losses"]
                dw = w["def_wins"]
                dl = w["def_losses"]

                off_matches += ow + ol
                off_wins += ow
                off_losses += ol

                def_matches += dw + dl
                def_wins += dw
                def_losses += dl

        total_matches = off_matches + def_matches
        total_wins = off_wins + def_wins
        total_losses = off_losses + def_losses

        # Going First
        self.summary_row_off["matches"].config(text=str(off_matches))
        self.summary_row_off["wins"].config(text=str(off_wins))
        self.summary_row_off["losses"].config(text=str(off_losses))
        off_wr = (100.0 * off_wins / off_matches) if off_matches > 0 else 0.0
        self.summary_row_off["win_rate"].config(text=f"{off_wr:.1f}%")

        # Going Second
        self.summary_row_def["matches"].config(text=str(def_matches))
        self.summary_row_def["wins"].config(text=str(def_wins))
        self.summary_row_def["losses"].config(text=str(def_losses))
        def_wr = (100.0 * def_wins / def_matches) if def_matches > 0 else 0.0
        self.summary_row_def["win_rate"].config(text=f"{def_wr:.1f}%")

        # Overall
        self.summary_row_total["matches"].config(text=str(total_matches))
        self.summary_row_total["wins"].config(text=str(total_wins))
        self.summary_row_total["losses"].config(text=str(total_losses))
        total_wr = (100.0 * total_wins / total_matches) if total_matches > 0 else 0.0
        self.summary_row_total["win_rate"].config(text=f"{total_wr:.1f}%")

    def build_summary_rows(self):
        """Create summary rows for going first, going second, and total results."""
        self.summary_start_row = self.inner_frame.grid_size()[
            1
        ]  # Correct row index after warlords

        # Row for "Going First" summary
        lbl_title1 = tk.Label(
            self.inner_frame,
            text="Going First",
            bg="#888",
            fg="white",
            relief=tk.RIDGE,
            borderwidth=1,
        )
        lbl_title1.grid(
            row=self.summary_start_row, column=0, columnspan=2, sticky="nsew"
        )

        self.summary_row_off = {}
        self.create_summary_line(
            self.summary_start_row, self.summary_row_off, highlight_bg="#999"
        )

        # Row for "Going Second" summary
        lbl_title2 = tk.Label(
            self.inner_frame,
            text="Going Second",
            bg="#666",
            fg="white",
            relief=tk.RIDGE,
            borderwidth=1,
        )
        lbl_title2.grid(
            row=self.summary_start_row + 1, column=0, columnspan=2, sticky="nsew"
        )

        self.summary_row_def = {}
        self.create_summary_line(
            self.summary_start_row + 1, self.summary_row_def, highlight_bg="#777"
        )

        # Row for "Total" summary
        lbl_title3 = tk.Label(
            self.inner_frame,
            text="TOTAL",
            bg="#444",
            fg="white",
            relief=tk.RIDGE,
            borderwidth=1,
        )
        lbl_title3.grid(
            row=self.summary_start_row + 2, column=0, columnspan=2, sticky="nsew"
        )

        self.summary_row_total = {}
        self.create_summary_line(
            self.summary_start_row + 2, self.summary_row_total, highlight_bg="#555"
        )

        self.update_summary_rows()

    def update_faction_wr_label(self, faction_name):
        faction_data = next(
            (f for f in self.deck_obj["factions"] if f["faction_name"] == faction_name),
            None,
        )
        if not faction_data:
            return

        stats = self.compute_deck_vs_faction(faction_data)
        merged_lbl = self.faction_wr_labels[faction_name]
        merged_lbl.config(
            text=(
                f"(vs {faction_name})\n"
                f"Matches: {stats['matches']}\n"
                f"Wins: {stats['wins']}\n"
                f"Losses: {stats['losses']}\n"
                f"WR: {stats['wr']:.1f}%"
            )
        )

    def _on_canvas_resize(self, event):
        """Ensures the canvas resizes properly to fit the content."""
        self.inner_frame.update_idletasks()
        self.canvas.itemconfig(
            self.inner_frame_id,
            height=self.inner_frame.winfo_reqheight(),  # Only adjust height
        )

        # Ensure scroll region is updated correctly
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        """Handles mouse wheel scrolling for both Windows and Linux/Mac."""
        if event.num == 4:  # Linux/macOS scroll up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux/macOS scroll down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_scroll_wheel(self):
        """Binds scroll wheel events to the canvas."""
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # Windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # Linux/macOS Scroll Up
        self.canvas.bind_all(
            "<Button-5>", self._on_mousewheel
        )  # Linux/macOS Scroll Down

    def _on_frame_configure(self, event=None):
        """Ensures the inner frame expands correctly within the canvas."""
        self.inner_frame.update_idletasks()  # Ensure content sizes are updated
        inner_width = self.inner_frame.winfo_reqwidth()  # Get required width
        inner_height = self.inner_frame.winfo_reqheight()  # Get required height

        # Set the width dynamically
        self.canvas.itemconfig(self.inner_frame_id, width=inner_width, height=inner_height)

        # Ensure the canvas scroll region is updated
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
