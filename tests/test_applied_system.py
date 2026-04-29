from pathlib import Path
import unittest

from src.agent import AppliedMusicAgent


class AppliedSystemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = AppliedMusicAgent(Path(__file__).resolve().parents[1])

    def test_agent_returns_recommendations_for_valid_query(self) -> None:
        result = self.agent.run("I need upbeat gym music", mode="dj", top_k=5)
        self.assertTrue(result["ok"])
        self.assertGreaterEqual(len(result["recommendations"]), 3)
        self.assertGreater(result["confidence"], 0.2)

    def test_guardrail_blocks_unsafe_or_too_short_input(self) -> None:
        blocked = self.agent.run("hate", mode="dj", top_k=5)
        self.assertFalse(blocked["ok"])
        self.assertEqual(blocked["confidence"], 0.0)

    def test_agent_steps_are_observable(self) -> None:
        result = self.agent.run("calm study vibes", mode="analyst", top_k=5)
        step_names = [step["name"] for step in result["steps"]]
        self.assertEqual(step_names[:5], ["validate", "plan", "retrieve", "recommend", "self_check"])


if __name__ == "__main__":
    unittest.main()
