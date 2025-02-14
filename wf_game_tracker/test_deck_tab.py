import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from wf_game_tracker.deck_tab import DeckTab


class TestDeckTab(unittest.TestCase):

    def setUp(self):
        """Set up a mock Tkinter root and a sample deck object for testing."""
        self.root = tk.Tk()  # Required for Tkinter initialization
        self.mock_app = MagicMock()  # Mock the main application

        self.sample_deck = {
            "deck_name": "Test Deck",
            "factions": [
                {
                    "faction_name": "Ultramarines",
                    "warlords": [
                        {
                            "warlord_name": "Marneus Calgar",
                            "off_wins": 0,
                            "off_losses": 0,
                            "def_wins": 0,
                            "def_losses": 0,
                        }
                    ],
                }
            ],
        }

        self.deck_tab = DeckTab(
            self.root, self.sample_deck, self.mock_app
        )  # Create instance

    def tearDown(self):
        """Destroy the Tkinter root after each test."""
        self.root.destroy()

    def test_initial_deck_name(self):
        """Test if the deck title is set correctly from the given deck object."""
        self.assertEqual(self.deck_tab.deck_obj["deck_name"], "Test Deck")

    def test_ui_elements_created(self):
        """Ensure UI components like the inner frame exist."""
        self.assertIsNotNone(self.deck_tab.inner_frame)
        self.assertIsNotNone(self.deck_tab.canvas)

    def test_warlord_stat_update(self):
        """Check if updating a warlord’s stats updates the correct values."""
        warlord = self.sample_deck["factions"][0]["warlords"][0]
        initial_wins = warlord["off_wins"]

        # Simulate updating the off_wins stat
        self.deck_tab.update_warlord_row(1, warlord, "off_wins", delta=1)

        # Ensure the value changed in the deck data
        self.assertEqual(warlord["off_wins"], initial_wins + 1)

    def test_scrollable_frame_exists(self):
        """Ensure the scrollable frame structure is correctly initialized."""
        self.assertIsNotNone(self.deck_tab.canvas)
        self.assertIsNotNone(self.deck_tab.inner_frame_id)

    @patch("tkinter.Label.config")
    def test_label_updates_correctly(self, mock_config):
        """Mock a label to test if update_warlord_row correctly updates its value."""
        warlord = self.sample_deck["factions"][0]["warlords"][0]
        self.deck_tab.label_refs[(1, "off_wins")] = MagicMock()

        # Simulate incrementing off_wins
        self.deck_tab.update_warlord_row(1, warlord, "off_wins", delta=2)

        # Ensure label's text was updated
        self.deck_tab.label_refs[(1, "off_wins")].config.assert_called_with(text="2")


if __name__ == "__main__":
    unittest.main()
