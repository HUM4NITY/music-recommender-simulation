# Music Recommender Simulation

CLI-first simulation of a content-based music recommender inspired by Spotify/TikTok-style ranking loops.

## How The System Works

Real-world recommenders usually combine many signals: user behavior (likes, skips, repeat plays, playlists, watch/listen time), item metadata (genre, mood, audio features), and ranking objectives (engagement, novelty, retention). This project focuses on a **content-based** approach: we compare each song's attributes against a user taste profile, compute a weighted relevance score, and sort songs by score. In short: **Input data** (song features + profile preferences) -> **Scoring rule** (per-song weighted match/similarity) -> **Ranking rule** (sort all songs, return top-k).

### Collaborative vs Content-Based (Quick Distinction)

- Collaborative filtering: recommends songs because similar users liked/listened to them.
- Content-based filtering: recommends songs because their attributes match your declared taste profile.

### Features Used in This Simulation

- Categorical: `genre`, `mood`
- Numeric: `energy`, `tempo_bpm`, `danceability`, `acousticness`, `valence`
- User profile includes: `favorite_genre`, `favorite_mood`, and target values for numeric features.

## Algorithm Recipe

Per song:

- +2.0 points for exact genre match.
- +1.0 point for exact mood match.
- Numeric features use closeness scoring:
  - similarity = max(0, 1 - gap/max_gap)
  - points = similarity * feature_weight
- Example defaults:
  - energy 2.0
  - tempo 1.0
  - danceability 0.8
  - acousticness 0.7
  - valence 1.0

Across list:

- Score every song in the catalog with the same scoring function.
- Sort by score descending.
- Return top `k` songs.
- Optional diversity penalty reduces repeated artists/genres in top results.

## Why Both Scoring and Ranking Rules Matter

- Scoring rule answers: "How well does this one song match this user?"
- Ranking rule answers: "Among all songs, which are best right now?"

Without scoring, we cannot compare songs consistently. Without ranking, we cannot produce a recommendation list.

## Data

- File: `data/songs.csv`
- Songs: 20
- Genres include pop, rock, lofi, hip-hop, rnb, electronic, folk, edm, jazz, country, metal, dream-pop, ambient, hyperpop, soul, afrobeats, phonk, world, k-pop.

## Run Instructions

```bash
python -m src.main
```

## Sample CLI Output

Use your own run output as screenshots for submission.

```text
Loaded songs: 20

Profile: High-Energy Pop
 1. Sunrise Pulse - Astra Nova [pop/happy] | score=7.406
    reasons: genre match (+2.00); mood match (+1.00); energy similarity 0.97 (+1.94)
```

## Required Submission Screenshot Slots

Add these screenshots after running locally:

1. `python -m src.main` output for profile `High-Energy Pop`
2. output for profile `Chill Lofi`
3. output for profile `Deep Intense Rock`
4. output for profile `Adversarial: Sad but High Energy`
5. output section for experiment `Weight Shift`

## Potential Biases to Expect

- Genre overweight can create filter bubbles by suppressing cross-genre discoveries.
- Small catalog size can make repetition look like confidence.
- Exact mood matching may ignore songs with nearby emotional tone labels.
- User profile design strongly affects outcomes; poor profile definitions can mislead rankings.
