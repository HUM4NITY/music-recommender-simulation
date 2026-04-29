# Safety and bias notes

Known recommender risks:
- Filter bubbles: over-recommending one genre or mood.
- Data imbalance: small catalogs can overfit recurring tracks.
- Label bias: if mood tags are simplistic, nuance is lost.

Guardrail ideas:
- Require bounded profile values (0.0 to 1.0 for normalized features).
- Add confidence score to communicate uncertainty.
- Enforce diversity penalties to reduce repetition.
- Explain recommendations so users can challenge the system.

Responsible use:
- Entertainment and learning only.
- Not for medical, legal, hiring, or high-stakes decisions.
