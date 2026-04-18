# Reflection Notes

## Profile Output Comparisons

### High-Energy Pop vs Chill Lofi

High-Energy Pop favored high valence and high danceability tracks with faster tempos. Chill Lofi shifted strongly toward low-energy and high-acousticness songs. This makes sense because energy and acousticness targets are almost opposite.

### Chill Lofi vs Deep Intense Rock

Chill Lofi preferred calm songs with lower tempo and softer attributes. Deep Intense Rock moved toward high-energy/high-tempo tracks with intense mood. The output split is expected because both profile genre and numeric targets are far apart.

### Deep Intense Rock vs Adversarial: Sad but High Energy

Deep Intense Rock tends to surface aggressive rock/metal-like songs. The adversarial profile produces unusual mixes because it asks for high energy but low valence/sad mood, which can push dark high-BPM tracks above upbeat songs.

## What Changed in the Weight-Shift Experiment

When energy weight was doubled and genre weight halved, songs closer in energy jumped higher even without a genre match. This improved cross-genre flexibility but reduced genre purity.

## One Clear Limitation

The model can over-prioritize whichever feature has the highest weight. If genre is overweighted, it risks a filter bubble where songs from other genres are rarely explored, even if their vibe is a better overall fit.
