import os
import tempfile
import unittest
from pathlib import Path

from gaphify_re.gemini_agent import DEFAULT_GEMINI_MODEL, GeminiResult, build_agent_prompt, run_gemini_agent, write_gemini_artifacts


ROOT = Path(__file__).resolve().parents[1]


class GeminiAgentTests(unittest.TestCase):
    def test_minimal_prompt_is_smaller_than_naive_prompt(self):
        minimal = build_agent_prompt(ROOT, "minimal")
        naive = build_agent_prompt(ROOT, "naive")
        self.assertLess(minimal.estimated_tokens, naive.estimated_tokens)
        self.assertIn("reports/BROKEN_PYTHON_REPAIR_MATRIX.md", minimal.files)

    def test_graph_guided_prompt_uses_index_and_hot_pages(self):
        prompt = build_agent_prompt(ROOT, "graph-guided")
        self.assertIn("obsidian/index.md", prompt.files)
        self.assertIn("obsidian/hot.md", prompt.files)
        self.assertIn("Grphify/Obsidian evidence first", prompt.prompt)

    def test_default_model_is_current_flash(self):
        self.assertEqual(DEFAULT_GEMINI_MODEL, "gemini-2.5-flash")

    def test_stale_env_message_mentions_replacement(self):
        source = Path(__file__).resolve().parents[1] / "src" / "gaphify_re" / "gemini_agent.py"
        text = source.read_text(encoding="utf-8")
        self.assertIn("GEMINI_MODEL=gemini-1.5-flash", text)
        self.assertIn("GEMINI_MODEL={DEFAULT_GEMINI_MODEL}", text)

    def test_write_gemini_artifacts_updates_json_and_markdown(self):
        result = GeminiResult(
            mode="minimal",
            model="test-model",
            estimated_prompt_tokens=123,
            response_text="Test response",
            files_sent=("obsidian/hot.md",),
            generated_at_utc="2026-06-19T00:00:00+00:00",
        )
        with tempfile.TemporaryDirectory() as tmp:
            json_path, md_path = write_gemini_artifacts(Path(tmp), result)
            self.assertTrue(json_path.exists())
            self.assertTrue(md_path.exists())
            self.assertIn("Test response", md_path.read_text(encoding="utf-8"))

    def test_gemini_requires_api_key(self):
        old_key = os.environ.pop("GEMINI_API_KEY", None)
        try:
            with self.assertRaises(RuntimeError):
                run_gemini_agent(ROOT, "minimal")
        finally:
            if old_key is not None:
                os.environ["GEMINI_API_KEY"] = old_key


if __name__ == "__main__":
    unittest.main()
