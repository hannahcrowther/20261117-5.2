import unittest
import pandas as pd
from data_cleaning import load_file, quarantine


class TestOperations(unittest.TestCase):

    def test_load(self):
        input = "tests/test_data.csv"
        self.assertIsNotNone(load_file(input), "File not loaded")

    def test_quarantine(self):
        input = pd.read_csv("tests/test_data.csv")

        clean_df, quarantine_df = quarantine(
        input,
        ("test_id", "test_number"),
        {"test_date": "%d/%m/%Y"}
    )
        self.assertEqual(len(clean_df), 6, "Not the right number of cleaned rows" )
        self.assertEqual(len(quarantine_df), 4, "Not the right number of quarantined rows" )
        self.assertEqual(len(clean_df) + len(quarantine_df), 10, "Number of rows changed")


if __name__ == "__main__":
    unittest.main()