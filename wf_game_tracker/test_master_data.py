import unittest
from wf_game_tracker.master_data import MASTER_TABLE, deep_copy_master_table


class TestMasterData(unittest.TestCase):

    def test_deep_copy_master_table(self):
        """Test if deep_copy_master_table returns a correct deep copy of MASTER_TABLE"""
        copy_table = deep_copy_master_table()

        # Check if the copy is identical in structure but not the same object
        self.assertEqual(copy_table, MASTER_TABLE)
        self.assertIsNot(copy_table, MASTER_TABLE)

        # Ensure that modifying the copy does not affect the original
        copy_table[0]["warlords"][0]["off_wins"] = 99
        self.assertNotEqual(copy_table, MASTER_TABLE)
        self.assertEqual(MASTER_TABLE[0]["warlords"][0]["off_wins"], 0)

    def test_master_table_structure(self):
        """Test if MASTER_TABLE follows expected structure"""
        self.assertIsInstance(MASTER_TABLE, list)
        for faction in MASTER_TABLE:
            self.assertIsInstance(faction, dict)
            self.assertIn("faction_name", faction)
            self.assertIn("warlords", faction)
            self.assertIsInstance(faction["warlords"], list)

            for warlord in faction["warlords"]:
                self.assertIsInstance(warlord, dict)
                self.assertIn("warlord_name", warlord)
                self.assertIn("off_wins", warlord)
                self.assertIn("off_losses", warlord)
                self.assertIn("def_wins", warlord)
                self.assertIn("def_losses", warlord)
                self.assertEqual(warlord["off_wins"], 0)
                self.assertEqual(warlord["off_losses"], 0)
                self.assertEqual(warlord["def_wins"], 0)
                self.assertEqual(warlord["def_losses"], 0)


if __name__ == "__main__":
    unittest.main()
