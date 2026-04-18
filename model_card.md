# Model Card: VibeFinder 1.0

## Model Name

VibeFinder 1.0

## Goal / Task

Recommend songs that best match a user's taste profile using song attributes and weighted scoring.

## Data Used

- Source: `data/songs.csv`
- Size: 20 songs
- Attributes:
  - Categorical: genre, mood
  - Numeric: energy, tempo_bpm, danceability, acousticness, valence
- Limits:
  - Small dataset
  - Label quality depends on manual curation
  - Not behavior-based (no likes/skips/play counts)

## Algorithm Summary

The system compares each song to a user profile.

- It gives points for exact matches (genre and mood).
- It gives partial points for closeness on numeric features (energy, tempo, etc.).
- Every song gets a final score.
- Songs are sorted from highest to lowest score.
- Top-k songs are shown with short reasons.

This is content-based ranking, not collaborative filtering.

## Observed Behavior / Biases

- When genre weight is large, recommendations cluster in one genre.
- Small catalogs can repeatedly surface the same songs.
- Exact mood matching can be rigid and miss close emotional alternatives.
- Some genres appear less often in data, which reduces their visibility.

## Evaluation Process

Profiles tested:

1. High-Energy Pop
2. Chill Lofi
3. Deep Intense Rock
4. Adversarial: Sad but High Energy

Evaluation steps:

- Ran `python -m src.main` for all profiles.
- Compared top 5 outputs per profile.
- Ran sensitivity experiment:
  - doubled energy weight
  - halved genre weight
- Observed how top-ranked songs changed.

## Intended Use

- Learning/demo project for recommendation basics
- Explainable ranking in small song catalogs
- Classroom experiments with scoring weights

## Non-Intended Use

- Real production personalization at scale
- Sensitive decision-making
- Any high-stakes recommendation context

## Ideas for Improvement

1. Add hybrid logic (content + collaborative signals)
2. Add novelty/diversity constraints directly in ranking
3. Learn weights from feedback instead of fixed manual values

## Personal Reflection

The biggest learning moment was seeing that small changes to weights can completely change recommendations. AI tools helped me move faster when drafting scoring logic and profile ideas, but I had to manually verify that math and reasoning matched my intent. What surprised me most is that even a simple weighted algorithm can feel "smart" when explanations are clear. If I continue this project, I would add user feedback loops and compare a content-based model against a collaborative baseline.
