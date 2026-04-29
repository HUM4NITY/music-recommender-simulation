from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .main import PROFILES
from .rag import KnowledgeRetriever
from .recommender import load_songs, recommend_songs


@dataclass
class AgentStep:
    name: str
    details: str


class AppliedMusicAgent:
    """Agentic workflow: validate -> plan -> retrieve -> recommend -> self-check."""

    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir)
        self.songs = load_songs(self.base_dir / "data" / "songs.csv")
        self.retriever = KnowledgeRetriever(self.base_dir / "knowledge")
        self.retriever.build_index(self.songs)

    def _validate_query(self, query: str) -> tuple[bool, list[str]]:
        issues: list[str] = []
        if len(query.strip()) < 5:
            issues.append("query too short")
        banned = {"hate", "violence", "self-harm"}
        lowered = query.lower()
        if any(word in lowered for word in banned):
            issues.append("unsafe request content")
        return len(issues) == 0, issues

    def _choose_profile(self, query: str) -> str:
        q = query.lower()
        if any(word in q for word in ["focus", "study", "calm", "lofi"]):
            return "Chill Lofi"
        if any(word in q for word in ["rock", "intense", "heavy", "gym"]):
            return "Deep Intense Rock"
        if any(word in q for word in ["sad", "dark", "conflict"]):
            return "Adversarial: Sad but High Energy"
        return "High-Energy Pop"

    def _specialize_tone(self, text: str, mode: str) -> str:
        if mode == "dj":
            return f"DJ Coach: {text} Keep the energy arc smooth and intentional."
        if mode == "analyst":
            return f"System Analyst: {text} Decision justified by weighted feature alignment."
        return text

    def run(self, query: str, mode: str = "dj", top_k: int = 5) -> dict[str, Any]:
        steps: list[AgentStep] = []

        valid, issues = self._validate_query(query)
        steps.append(AgentStep("validate", "passed" if valid else f"failed: {issues}"))
        if not valid:
            return {
                "ok": False,
                "answer": "Request blocked by safety guardrails.",
                "confidence": 0.0,
                "steps": [step.__dict__ for step in steps],
                "issues": issues,
            }

        profile_name = self._choose_profile(query)
        steps.append(AgentStep("plan", f"selected profile={profile_name}"))

        context_chunks = self.retriever.retrieve(query, k=4)
        context_score = sum(chunk.score for chunk in context_chunks) / max(1, len(context_chunks))
        steps.append(
            AgentStep(
                "retrieve",
                f"chunks={len(context_chunks)}, avg_score={context_score:.2f}",
            )
        )

        profile = PROFILES[profile_name]
        recommendations = recommend_songs(profile, self.songs, k=top_k, diversity_penalty=0.25)
        steps.append(AgentStep("recommend", f"generated {len(recommendations)} ranked songs"))

        top_score = recommendations[0]["score"] if recommendations else 0.0
        confidence = min(0.99, round((top_score / 10.0) * 0.75 + context_score * 0.25, 4))
        confidence = max(0.05, confidence)
        steps.append(AgentStep("self_check", f"confidence={confidence:.2f}"))

        lines = [
            f"Profile used: {profile_name}",
            f"Top recommendation: {recommendations[0]['song']['title']} ({recommendations[0]['score']:.2f})",
            "Top 3 songs:",
        ]
        for rec in recommendations[:3]:
            song = rec["song"]
            lines.append(
                f"- {song['title']} by {song['artist']} [{song['genre']}/{song['mood']}] score={rec['score']:.2f}"
            )

        if context_chunks:
            lines.append("Retrieved context:")
            for chunk in context_chunks[:2]:
                lines.append(f"- ({chunk.source}, {chunk.score:.2f}) {chunk.text[:110]}...")

        answer = self._specialize_tone("\n".join(lines), mode=mode)

        return {
            "ok": True,
            "answer": answer,
            "confidence": confidence,
            "profile": profile_name,
            "recommendations": recommendations,
            "retrieved_context": [chunk.__dict__ for chunk in context_chunks],
            "steps": [step.__dict__ for step in steps],
            "issues": [],
        }
