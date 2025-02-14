import unittest
from unittest.mock import patch, mock_open
import json
import tkinter as tk
from wf_game_tracker.main_app import DeckTrackerApp


class TestDeckTrackerApp(unittest.TestCase):

    def setUp(self):
        """Set up a mock Tkinter root and DeckTrackerApp instance without displaying GUI."""
        self.root = tk.Tk()
        self.root.withdraw()  # Prevent the main window from appearing
        self.app = DeckTrackerApp()

    def tearDown(self):
        """Destroy Tkinter root after each test."""
        self.app.destroy()
        self.root.destroy()

    def test_initial_deck_list_empty(self):
        """Test that the app initializes with an empty deck list."""
        self.assertEqual(self.app.decks, [])

    def test_create_new_deck(self):
        """Test adding a new deck updates the deck list correctly."""
        self.app.create_new_deck()
        self.assertEqual(len(self.app.decks), 1)
        self.assertEqual(self.app.decks[0]["deck_name"], "New Deck")

    def test_merge_with_master_table(self):
        """Test merging loaded deck data with MASTER_TABLE to include new factions/warlords."""
        sample_loaded_deck = [
            {
                "deck_name": "Test Deck",
                "factions": [
                    {
                        "faction_name": "Ultramarines",
                        "warlords": [
                            {
                                "warlord_name": "Marneus Calgar",
                                "off_wins": 2,
                                "off_losses": 1,
                                "def_wins": 1,
                                "def_losses": 1,
                            }
                        ],
                    }
                ],
            }
        ]

        merged_decks = self.app.merge_with_master_table(sample_loaded_deck)

        # Ensure original warlord data is retained
        self.assertEqual(merged_decks[0]["factions"][0]["warlords"][0]["off_wins"], 2)

    @patch("tkinter.filedialog.askopenfilename", return_value="test_file.json")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=json.dumps([{"deck_name": "Test Deck", "factions": []}]),
    )
    def test_open_file(self, mock_open, mock_filedialog):
        """Test opening a JSON file and loading deck data."""
        self.app.open_file()
        self.assertEqual(len(self.app.decks), 1)
        self.assertEqual(self.app.decks[0]["deck_name"], "Test Deck")

    @patch("tkinter.filedialog.asksaveasfilename", return_value="test_file.json")
    @patch("builtins.open", new_callable=mock_open)
    @patch("tkinter.messagebox.showinfo")  # <-- Mock the pop-up
    def test_save_file_as(self, mock_messagebox, mock_open, mock_filedialog):
        """Test saving deck data to a JSON file without showing a messagebox."""
        self.app.create_new_deck()
        self.app.save_file_as()

        # Ensure file was written
        mock_open.assert_called_once_with("test_file.json", "w", encoding="utf-8")

        # Get the mock file handle and the written data
        handle = mock_open()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)

        # Ensure JSON data is valid
        json_content = json.loads(written_data)
        self.assertEqual(json_content[0]["deck_name"], "New Deck")

        # Ensure no real pop-up appears
        mock_messagebox.assert_called_with("Saved", "Data saved to test_file.json")

    @patch("tkinter.messagebox.showinfo")
    def test_show_overall_summary(self, mock_messagebox):
        """Test summary function correctly calculates total matches, wins, and losses."""
        self.app.decks = [
            {
                "deck_name": "Test Deck",
                "factions": [
                    {
                        "faction_name": "Ultramarines",
                        "warlords": [
                            {
                                "warlord_name": "Marneus Calgar",
                                "off_wins": 2,
                                "off_losses": 1,
                                "def_wins": 3,
                                "def_losses": 2,
                            }
                        ],
                    }
                ],
            }
        ]
        self.app.show_overall_summary()

        # Ensure messagebox was called with correct summary
        expected_message = (
            "Overall Matches: 8\n"
            "Overall Wins: 5\n"
            "Overall Losses: 3\n"
            "Overall Win Rate: 62.5%\n"
        )
        mock_messagebox.assert_called_with("Overall Summary", expected_message)


if __name__ == "__main__":
    unittest.main()
