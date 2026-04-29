from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import re


TOKEN_RE = re.compile(r"[a-zA-Z0-9_]+")


@dataclass
class RetrievedChunk:
    source: str
    text: str
    score: float


def _tokenize(text: str) -> set[str]:
    return set(token.lower() for token in TOKEN_RE.findall(text))


class KnowledgeRetriever:
    """Simple local multi-source retriever using lexical overlap scoring."""

    def __init__(self, knowledge_dir: str | Path):
        self.knowledge_dir = Path(knowledge_dir)
        self._chunks: list[tuple[str, str, set[str]]] = []

    def build_index(self, songs: list[dict[str, Any]]) -> None:
        self._chunks.clear()

        # Source 1: curated docs
        for md_path in sorted(self.knowledge_dir.glob("*.md")):
            text = md_path.read_text(encoding="utf-8")
            for paragraph in [p.strip() for p in text.split("\n\n") if p.strip()]:
                self._chunks.append((f"doc:{md_path.name}", paragraph, _tokenize(paragraph)))

        # Source 2: generated song snippets from catalog
        for song in songs:
            snippet = (
                f"{song['title']} by {song['artist']} is {song['genre']} with mood {song['mood']}. "
                f"energy={song['energy']}, tempo_bpm={song['tempo_bpm']}, "
                f"danceability={song['danceability']}, acousticness={song['acousticness']}, "
                f"valence={song['valence']}"
            )
            self._chunks.append(("songs.csv", snippet, _tokenize(snippet)))

    def retrieve(self, query: str, k: int = 4) -> list[RetrievedChunk]:
        query_tokens = _tokenize(query)
        if not query_tokens or not self._chunks:
            return []

        rows: list[RetrievedChunk] = []
        for source, text, tokens in self._chunks:
            overlap = query_tokens.intersection(tokens)
            if not overlap:
                continue
            score = len(overlap) / max(1, len(query_tokens))
            rows.append(RetrievedChunk(source=source, text=text, score=round(score, 4)))

        rows.sort(key=lambda row: row.score, reverse=True)
        return rows[:k]
