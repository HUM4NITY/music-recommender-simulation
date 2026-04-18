from pathlib import Path
import unittest

from src.recommender import load_songs, recommend_songs, score_song


class RecommenderTests(unittest.TestCase):
    def test_load_songs_converts_numeric_types(self) -> None:
        songs = load_songs(Path("data/songs.csv"))
        self.assertGreaterEqual(len(songs), 15)
        self.assertIsInstance(songs[0]["energy"], float)
        self.assertIsInstance(songs[0]["tempo_bpm"], int)

    def test_score_song_returns_number_and_reasons(self) -> None:
        songs = load_songs(Path("data/songs.csv"))
        user = {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.85,
        }
        score, reasons = score_song(user, songs[0])
        self.assertIsInstance(score, float)
        self.assertGreater(len(reasons), 0)

    def test_recommend_songs_is_sorted_descending(self) -> None:
        songs = load_songs(Path("data/songs.csv"))
        user = {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.9,
            "target_tempo_bpm": 145,
        }
        recs = recommend_songs(user, songs, k=5)
        self.assertEqual(len(recs), 5)
        self.assertGreaterEqual(recs[0]["score"], recs[1]["score"])
        self.assertGreaterEqual(recs[1]["score"], recs[2]["score"])


if __name__ == "__main__":
    unittest.main()
