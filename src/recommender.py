from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


NUMERIC_FIELDS = {"energy", "tempo_bpm", "danceability", "acousticness", "valence"}

DEFAULT_WEIGHTS = {
    "genre": 2.0,
    "mood": 1.0,
    "energy": 2.0,
    "tempo_bpm": 1.0,
    "danceability": 0.8,
    "acousticness": 0.7,
    "valence": 1.0,
}


def load_songs(csv_path: str | Path) -> list[dict[str, Any]]:
    """Load song rows from CSV and convert numeric columns into numbers."""
    songs: list[dict[str, Any]] = []

    with Path(csv_path).open("r", encoding="utf-8", newline="") as file_obj:
        reader = csv.DictReader(file_obj)
        for row in reader:
            song: dict[str, Any] = {}
            for key, value in row.items():
                if key in NUMERIC_FIELDS:
                    if key == "tempo_bpm":
                        song[key] = int(float(value))
                    else:
                        song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs


def _normalized_similarity(song_value: float, target_value: float, max_gap: float) -> float:
    """Return similarity in [0, 1], where 1 is exact match and 0 is too far away."""
    if max_gap <= 0:
        return 0.0
    gap = abs(song_value - target_value)
    return max(0.0, 1.0 - (gap / max_gap))


def score_song(
    user_prefs: dict[str, Any],
    song: dict[str, Any],
    weights: dict[str, float] | None = None,
    include_mood: bool = True,
) -> tuple[float, list[str]]:
    """Compute weighted relevance score and human-readable reasons for one song."""
    active_weights = DEFAULT_WEIGHTS.copy()
    if weights:
        active_weights.update(weights)

    score = 0.0
    reasons: list[str] = []

    preferred_genre = user_prefs.get("favorite_genre")
    if preferred_genre and song.get("genre") == preferred_genre:
        pts = active_weights["genre"]
        score += pts
        reasons.append(f"genre match (+{pts:.2f})")

    preferred_mood = user_prefs.get("favorite_mood")
    if include_mood and preferred_mood and song.get("mood") == preferred_mood:
        pts = active_weights["mood"]
        score += pts
        reasons.append(f"mood match (+{pts:.2f})")

    numeric_map = {
        "energy": ("target_energy", 1.0),
        "tempo_bpm": ("target_tempo_bpm", 120.0),
        "danceability": ("target_danceability", 1.0),
        "acousticness": ("target_acousticness", 1.0),
        "valence": ("target_valence", 1.0),
    }

    for feature_name, (pref_key, max_gap) in numeric_map.items():
        target = user_prefs.get(pref_key)
        if target is None:
            continue
        similarity = _normalized_similarity(float(song[feature_name]), float(target), max_gap)
        pts = similarity * active_weights[feature_name]
        score += pts
        reasons.append(f"{feature_name} similarity {similarity:.2f} (+{pts:.2f})")

    if not reasons:
        reasons.append("baseline: no strong preference match")

    return round(score, 4), reasons


def recommend_songs(
    user_prefs: dict[str, Any],
    songs: list[dict[str, Any]],
    k: int = 5,
    weights: dict[str, float] | None = None,
    include_mood: bool = True,
    diversity_penalty: float = 0.0,
) -> list[dict[str, Any]]:
    """Rank songs by score and return top-k recommendations with explanations."""
    scored_rows: list[dict[str, Any]] = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights=weights, include_mood=include_mood)
        scored_rows.append({"song": song, "score": score, "reasons": reasons})

    ranked = sorted(scored_rows, key=lambda row: row["score"], reverse=True)

    if diversity_penalty <= 0:
        return ranked[:k]

    selected: list[dict[str, Any]] = []
    seen_genres: dict[str, int] = {}
    seen_artists: dict[str, int] = {}

    for row in ranked:
        genre = str(row["song"]["genre"])
        artist = str(row["song"]["artist"])
        adjusted_score = row["score"]

        adjusted_score -= seen_genres.get(genre, 0) * diversity_penalty
        adjusted_score -= seen_artists.get(artist, 0) * diversity_penalty

        candidate = {
            "song": row["song"],
            "score": round(adjusted_score, 4),
            "reasons": list(row["reasons"]),
        }

        if adjusted_score != row["score"]:
            candidate["reasons"].append(
                f"diversity penalty applied (-{row['score'] - adjusted_score:.2f})"
            )

        selected.append(candidate)
        seen_genres[genre] = seen_genres.get(genre, 0) + 1
        seen_artists[artist] = seen_artists.get(artist, 0) + 1

        if len(selected) >= k:
            break

    return selected
