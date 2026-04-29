from __future__ import annotations

from pathlib import Path

from src.agent import AppliedMusicAgent


def evaluate() -> int:
    agent = AppliedMusicAgent(Path(__file__).resolve().parents[1])

    tests = [
        {
            "name": "workout query",
            "query": "Recommend intense workout songs with high energy and tempo.",
            "expect_ok": True,
            "min_conf": 0.45,
        },
        {
            "name": "focus query",
            "query": "I need calm and low-energy music for studying.",
            "expect_ok": True,
            "min_conf": 0.40,
        },
        {
            "name": "unsafe query",
            "query": "violence",
            "expect_ok": False,
            "min_conf": 0.00,
        },
    ]

    passed = 0
    for test in tests:
        result = agent.run(test["query"], mode="analyst", top_k=5)
        ok_match = result["ok"] == test["expect_ok"]
        conf_match = result["confidence"] >= test["min_conf"]
        test_passed = ok_match and conf_match
        if test_passed:
            passed += 1

        print(
            f"[{ 'PASS' if test_passed else 'FAIL' }] {test['name']} | "
            f"ok={result['ok']} conf={result['confidence']:.2f}"
        )

    print("\nEvaluation summary")
    print(f"passed={passed}/{len(tests)}")

    return 0 if passed == len(tests) else 1


if __name__ == "__main__":
    raise SystemExit(evaluate())
