# Model Card: VibePilot 2.0 Applied AI System

## Model Name

VibePilot 2.0

## Goal and Task

Provide explainable music recommendations from a local catalog while using retrieval context and an agentic decision chain to increase transparency and reliability.

## Data Used

- Core catalog: data/songs.csv (20 songs)
- Retrieval sources:
  - knowledge/genre_guides.md
  - knowledge/safety_and_bias.md
  - generated song snippets from songs.csv
- Features:
  - categorical: genre, mood
  - numeric: energy, tempo_bpm, danceability, acousticness, valence

## Algorithm and System Summary

1. Guardrail validation checks query quality and unsafe content.
2. Agent planning step maps query intent to a profile.
3. RAG retriever fetches top context chunks from multi-source local knowledge.
4. Recommender computes weighted scores and ranks songs.
5. Self-check computes confidence from recommendation strength and retrieval relevance.
6. Response composer outputs specialized tone and visible reasoning steps.

## Intended Use

- Educational demonstration of applied AI system design
- Explainable recommendation workflows
- Small-scale prototyping with transparent decision logic

## Non-Intended Use

- High-stakes decisions (medical, legal, hiring, finance)
- Large-scale production personalization
- Safety-critical automation without human review

## Reliability and Guardrails

- Input guardrails:
  - block unsafe terms
  - block underspecified queries
- Confidence score per response
- Automated evaluation harness (eval/evaluation.py)
- Unit tests for both recommender and applied agent behavior

## Evaluation Summary

Evaluation script tests:

1. workout-style query should pass with minimum confidence
2. focus-style query should pass with minimum confidence
3. unsafe/too-short query should be blocked

Recent evaluation summary target:

- passed=3/3

## Observed Behavior, Limitations, and Biases

- Small dataset increases repetition risk.
- Rule-based profile selection can misclassify nuanced prompts.
- Lexical retrieval can miss semantic matches with different wording.
- Genre/mood labels are subjective and can encode simplifications.
- Confidence score is heuristic, not calibrated probability.

## Potential Misuse and Mitigations

Potential misuse:

- Treating recommendations as objective truth.
- Using outputs without context in sensitive settings.

Mitigations:

- explicit intended/non-intended use
- visible reasons and step trace
- confidence display
- guardrail rejection path

## AI Collaboration Reflection

Helpful AI suggestion:

- AI suggested separating retrieval logic into its own module. This improved modularity and made evaluation easier because retrieval behavior is now testable in isolation.

Flawed AI suggestion:

- AI initially suggested only running a standalone retrieval demo script. That would not satisfy integration requirements, so the design was revised to ensure retrieval directly influences final recommendations and confidence.

## What Surprised Me in Reliability Testing

Even with deterministic scoring, output trust improves significantly when users can see intermediate steps and confidence. The guardrail layer caught short unsafe prompts that would otherwise generate noisy outputs.

## Future Improvements

1. Replace lexical retrieval with semantic embeddings for better context recall.
2. Add profile learning from user feedback.
3. Calibrate confidence against human-labeled benchmarks.
4. Expand catalog and add fairness-aware diversity constraints.
