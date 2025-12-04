import unittest
import os

from src.utils import download_file_from_gdrive
from src.config import MASTERS_GDRIVE_FILES, LOCAL_MASTERS_TEMPLATE
from src.masters_pipeline import clean_player_name


class Tests(unittest.TestCase):
    def test_download_masters_2021(self):
        year = 2021
        url = MASTERS_GDRIVE_FILES[year]
        filename = LOCAL_MASTERS_TEMPLATE.format(year=year)

        path = download_file_from_gdrive(url, filename)
        self.assertTrue(os.path.exists(path))

    def test_clean_name(self):
        self.assertEqual(clean_player_name("Homa, Max"), "Max Homa")

if __name__ == "__main__":
    unittest.main()
