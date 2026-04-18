from __future__ import annotations

from pathlib import Path

from .recommender import DEFAULT_WEIGHTS, load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_tempo_bpm": 126,
        "target_danceability": 0.86,
        "target_acousticness": 0.18,
        "target_valence": 0.9,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "calm",
        "target_energy": 0.25,
        "target_tempo_bpm": 78,
        "target_danceability": 0.45,
        "target_acousticness": 0.8,
        "target_valence": 0.5,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_tempo_bpm": 150,
        "target_danceability": 0.5,
        "target_acousticness": 0.1,
        "target_valence": 0.45,
    },
    "Adversarial: Sad but High Energy": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.92,
        "target_tempo_bpm": 142,
        "target_danceability": 0.7,
        "target_acousticness": 0.15,
        "target_valence": 0.2,
    },
}


def print_recommendations(profile_name: str, recs: list[dict], k: int = 5) -> None:
    """Print recommendations in a compact CLI-first layout."""
    print("=" * 84)
    print(f"Profile: {profile_name}")
    print("-" * 84)
    for idx, rec in enumerate(recs[:k], start=1):
        song = rec["song"]
        print(
            f"{idx:>2}. {song['title']} - {song['artist']} "
            f"[{song['genre']}/{song['mood']}] | score={rec['score']:.3f}"
        )
        print(f"    reasons: {'; '.join(rec['reasons'][:3])}")
    print()


def run_experiment(songs: list[dict], profile: dict) -> None:
    """Run one small sensitivity test: shift weight from genre to energy."""
    experiment_weights = DEFAULT_WEIGHTS.copy()
    experiment_weights["energy"] = DEFAULT_WEIGHTS["energy"] * 2
    experiment_weights["genre"] = DEFAULT_WEIGHTS["genre"] * 0.5

    baseline = recommend_songs(profile, songs, k=5, diversity_penalty=0.25)
    adjusted = recommend_songs(
        profile,
        songs,
        k=5,
        weights=experiment_weights,
        diversity_penalty=0.25,
    )

    print("=" * 84)
    print("Experiment: Weight Shift (energy x2, genre x0.5)")
    print("-" * 84)
    print("Baseline top 3:")
    for rec in baseline[:3]:
        print(f"  - {rec['song']['title']} ({rec['score']:.3f})")

    print("Adjusted top 3:")
    for rec in adjusted[:3]:
        print(f"  - {rec['song']['title']} ({rec['score']:.3f})")
    print()


def main() -> None:
    """Load songs, run profile recommendations, and print a sensitivity experiment."""
    csv_path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
    songs = load_songs(csv_path)

    print(f"Loaded songs: {len(songs)}")
    print()

    for profile_name, profile in PROFILES.items():
        recs = recommend_songs(profile, songs, k=5, diversity_penalty=0.25)
        print_recommendations(profile_name, recs, k=5)

    run_experiment(songs, PROFILES["High-Energy Pop"])


if __name__ == "__main__":
    main()
