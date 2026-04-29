# Reflection Notes: Applied AI System

## Biggest Learning Moment

The biggest learning moment was that reliability is not one feature, it is a stack of small mechanisms. Guardrails, retrieval grounding, visible planning steps, and confidence scoring together made the system feel far more trustworthy than scoring alone.

## Helpful AI Suggestion

AI helped by proposing a modular separation between recommender, retrieval, and orchestration. That made it easier to build a clear architecture diagram and write focused tests.

## Flawed AI Suggestion

AI suggested an isolated retrieval demo script. That would have failed rubric integration criteria because retrieval was not altering final system behavior. I corrected this by routing retrieval output directly into agent responses and confidence computation.

## What Surprised Me in Testing

Two prompts with similar intent can produce different retrieval quality due to wording. The lexical retriever is transparent but brittle, which surfaced the need for semantic retrieval in future iterations.

## Future Extension Ideas

1. Add embedding-based retrieval and compare quality against lexical baseline.
2. Add multi-objective ranking that balances preference match and novelty.
3. Add a simple web UI for better user testing and human rating collection.
