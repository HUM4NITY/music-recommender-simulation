from __future__ import annotations

from pathlib import Path

from .agent import AppliedMusicAgent


def print_run_result(title: str, result: dict) -> None:
    print("=" * 100)
    print(f"Input: {title}")
    print("-" * 100)
    print(result["answer"])
    print(f"\nconfidence={result['confidence']:.2f} ok={result['ok']}")
    print("steps:")
    for step in result["steps"]:
        print(f"  - {step['name']}: {step['details']}")
    print()


def main() -> None:
    agent = AppliedMusicAgent(Path(__file__).resolve().parents[1])

    demo_inputs = [
        "I need a high-energy playlist for a 45-minute workout.",
        "Give me calm study tracks for late-night focus.",
        "I want dark and sad but still energetic songs for a dramatic edit.",
    ]

    for query in demo_inputs:
        result = agent.run(query, mode="dj", top_k=5)
        print_run_result(query, result)


if __name__ == "__main__":
    main()
