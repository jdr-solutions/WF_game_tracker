# main_app.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

# Import our local modules
from wf_game_tracker.master_data import MASTER_TABLE, deep_copy_master_table
from wf_game_tracker.deck_tab import DeckTab

class DeckTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Deck Tracker V1.1")

        # Set minimum size (adjust these values as needed)
        self.minsize(800, 400)

        self.decks = []
        self.deck_tabs = []
        self.current_file = None
        self.create_menu()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)  # Ensure notebook fills space
        self.notebook.grid_rowconfigure(0, weight=1)  # Ensure tabs take full space
        self.notebook.grid_columnconfigure(0, weight=1)

        # Bind scrolling events to all deck tabs in the notebook
        self.notebook.bind("<<NotebookTabChanged>>", self._update_scroll_binding)

        new_deck_btn = tk.Button(self, text="Create New Deck", command=self.handle_add_new_deck)
        new_deck_btn.pack(side=tk.BOTTOM, pady=5)
        default_save = "default_decks.json"
        if os.path.exists(default_save):
            self.load_data(default_save)

    def _on_mousewheel_windows(self, event):
        # Figure out which tab is active
        current_tab_idx = self.notebook.index("current")

        # If no tabs, do nothing
        if len(self.deck_tabs) == 0:
            return

        # Otherwise, get the corresponding DeckTab
        deck_tab_obj = self.deck_tabs[current_tab_idx]
        deck_tab_obj.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"

    def _on_mousewheel_other(self, event):
        current_tab_idx = self.notebook.index("current")
        if len(self.deck_tabs) == 0:
            return

        deck_tab_obj = self.deck_tabs[current_tab_idx]
        if event.num == 4:
            deck_tab_obj.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            deck_tab_obj.canvas.yview_scroll(1, "units")
        return "break"

    def _update_scroll_binding(self, event):
        """Ensure mouse scrolling affects the currently selected tab."""
        current_tab_idx = self.notebook.index("current")
        
        # If no tabs exist, do nothing
        if len(self.deck_tabs) == 0:
            return
        
        # Get the currently selected DeckTab
        deck_tab_obj = self.deck_tabs[current_tab_idx]

        # Rebind scrolling to the active tab's canvas
        self.unbind_all("<MouseWheel>")
        self.unbind_all("<Button-4>")
        self.unbind_all("<Button-5>")

        self.bind_all("<MouseWheel>", deck_tab_obj._on_mousewheel)
        self.bind_all("<Button-4>", deck_tab_obj._on_mousewheel)  # Linux/macOS Scroll Up
        self.bind_all("<Button-5>", deck_tab_obj._on_mousewheel)  # Linux/macOS Scroll Down


    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Save", command=self.save_file)
        filemenu.add_command(label="Save As", command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def merge_with_master_table(self, loaded_decks):
        """
        Merge the loaded deck data with the MASTER_TABLE, ensuring that
        new factions/warlords from the MASTER_TABLE are included.
        """
        updated_decks = []
        for loaded_deck in loaded_decks:
            merged_deck = {
                "deck_name": loaded_deck.get("deck_name", "Unnamed Deck"),
                "factions": []
            }

            # Merge each faction in MASTER_TABLE
            for master_faction in MASTER_TABLE:
                # Check if this faction exists in the loaded deck
                matching_faction = next(
                    (f for f in loaded_deck["factions"] if f["faction_name"] == master_faction["faction_name"]),
                    None
                )
                if matching_faction:
                    # Merge warlords
                    merged_faction = {
                        "faction_name": matching_faction["faction_name"],
                        "warlords": []
                    }
                    for master_warlord in master_faction["warlords"]:
                        # Check if this warlord exists in the loaded faction
                        matching_warlord = next(
                            (w for w in matching_faction["warlords"] if w["warlord_name"] == master_warlord["warlord_name"]),
                            None
                        )
                        if matching_warlord:
                            # Use the existing warlord's stats
                            merged_faction["warlords"].append(matching_warlord)
                        else:
                            # Add new warlord with zeroed stats
                            merged_faction["warlords"].append(master_warlord)
                    merged_deck["factions"].append(merged_faction)
                else:
                    # Add the entire new faction from MASTER_TABLE
                    merged_deck["factions"].append(master_faction)

            updated_decks.append(merged_deck)

        return updated_decks

    def handle_add_new_deck(self):
        self.create_new_deck()
        # tkinter not threadsafe
        # thread = threading.Thread(target=self.create_new_deck)
        # thread.start()

    def create_new_deck(self):
        new_deck = {
            "deck_name": "New Deck",
            "factions": deep_copy_master_table()
        }
        self.decks.append(new_deck)
        self.after(0, lambda: self.finalize_new_tab(new_deck))

    def finalize_new_tab(self, deck_obj):
        new_tab = DeckTab(self.notebook, deck_obj, self)
        self.notebook.add(new_tab, text=deck_obj["deck_name"])
        self.deck_tabs.append(new_tab)

    ###########################################################################
    # JSON file operations
    ###########################################################################
    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Open Save File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.load_data(filename)

    def load_data(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                loaded_decks = json.load(f)
            
            # Merge loaded data with MASTER_TABLE
            self.decks = self.merge_with_master_table(loaded_decks)
            self.current_file = filename
            self.build_tabs()
        except Exception as e:
            messagebox.showerror("Load Error", str(e))


    def save_file(self):
        if self.current_file:
            self.write_data(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        filename = filedialog.asksaveasfilename(
            title="Save File As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.write_data(filename)
            self.current_file = filename

    def write_data(self, filename):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.decks, f, indent=2)
            messagebox.showinfo("Saved", f"Data saved to {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    ###########################################################################
    # Deck & Tabs Management
    ###########################################################################
    def build_tabs(self):
        """Remove existing tabs and build them from self.decks."""
        # Clear old tabs
        for tab_id in self.notebook.tabs():
            self.notebook.forget(tab_id)

        # Also clear your deck_tabs list, so we don't mix old references
        self.deck_tabs.clear()

        for deck_index, deck_obj in enumerate(self.decks):
            deck_name = deck_obj.get("deck_name", f"Deck {deck_index+1}")
            
            # Create a DeckTab directly in the notebook
            deck_tab = DeckTab(self.notebook, deck_obj, self)
            
            # Add DeckTab as a new tab
            self.notebook.add(deck_tab, text=deck_name)
            self.deck_tabs.append(deck_tab)


    def add_new_deck(self):
        """
        Create a new deck with a copy of the MASTER_TABLE structure,
        set default name, then rebuild tabs to display it.
        """
        new_deck = {
            "deck_name": "New Deck",
            "factions": deep_copy_master_table()
        }
        self.decks.append(new_deck)
        self.build_tabs()

    ###########################################################################
    # Summary
    ###########################################################################
    def show_overall_summary(self):
        """
        Summarize across all decks: total matches, total wins, total losses, overall WR.
        """
        total_matches = 0
        total_wins = 0
        total_losses = 0

        for deck in self.decks:
            for faction_data in deck["factions"]:
                for wlord in faction_data["warlords"]:
                    ow = wlord["off_wins"]
                    ol = wlord["off_losses"]
                    dw = wlord["def_wins"]
                    dl = wlord["def_losses"]
                    matches = ow + ol + dw + dl
                    wins = ow + dw
                    losses = ol + dl

                    total_matches += matches
                    total_wins += wins
                    total_losses += losses

        if total_matches > 0:
            rate = 100.0 * total_wins / total_matches
        else:
            rate = 0.0

        msg = (
            f"Overall Matches: {total_matches}\n"
            f"Overall Wins: {total_wins}\n"
            f"Overall Losses: {total_losses}\n"
            f"Overall Win Rate: {rate:.1f}%\n"
        )
        messagebox.showinfo("Overall Summary", msg)
