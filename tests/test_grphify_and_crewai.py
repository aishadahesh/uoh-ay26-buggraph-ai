import unittest
from pathlib import Path

from gaphify_re.crew_agent import run_crewai_bug_hunt
from gaphify_re.grphify_runner import build_grphify_graph, summarize_graph
from gaphify_re.token_meter import compare_modes


ROOT = Path(__file__).resolve().parents[1]


class GrphifyAndCrewTests(unittest.TestCase):
    def test_grphify_graph_has_evidence_scale(self):
        graph = build_grphify_graph(ROOT)
        evidence = {edge["evidence"] for edge in graph["edges"]}
        self.assertIn("extracted", evidence)
        self.assertIn("inferred", evidence)
        self.assertGreater(len(graph["nodes"]), 20)

    def test_graph_summary_names_minimal_route(self):
        summary = summarize_graph(build_grphify_graph(ROOT))
        self.assertIn("obsidian/hot.md", summary["minimal_route"])
        self.assertGreater(summary["edge_count"], 30)

    def test_crewai_bug_hunt_uses_graph_first_context(self):
        result = run_crewai_bug_hunt(ROOT)
        self.assertEqual(result.files_read[0], "artifacts/grphify_summary.json")
        self.assertIn("global score", result.root_cause)
        self.assertGreater(result.estimated_tokens, 0)

    def test_minimal_context_uses_fewer_tokens_than_guided(self):
        modes = {mode.name: mode for mode in compare_modes(ROOT)}
        self.assertLess(modes["minimal-sufficient"].estimated_tokens, modes["graph-guided"].estimated_tokens)
        self.assertLess(modes["graph-guided"].estimated_tokens, modes["naive"].estimated_tokens)


if __name__ == "__main__":
    unittest.main()
