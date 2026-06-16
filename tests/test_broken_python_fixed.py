import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "data" / "upstream_broken_python"
FIXED = ROOT / "fixed" / "broken-python"


def load_module(name: str, path: Path, extra_sys_path: Path | None = None):
    if extra_sys_path is not None:
        sys.path.insert(0, str(extra_sys_path))
    try:
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        if extra_sys_path is not None:
            sys.path.remove(str(extra_sys_path))


def exec_function_prefix(path: Path) -> dict:
    """Load only function definitions from upstream checkpoint scripts."""
    source = path.read_text(encoding="utf-8")
    prefix = source.split("# display welcome message")[0]
    namespace: dict = {}
    exec(compile(prefix, str(path), "exec"), namespace)
    return namespace


class BrokenPythonRepairTests(unittest.TestCase):
    def test_upstream_mathsquiz_has_syntax_error(self):
        source = (UPSTREAM / "mathsquiz" / "mathsquiz.py").read_text(encoding="utf-8")
        with self.assertRaises(SyntaxError):
            compile(source, "mathsquiz.py", "exec")

    def test_fixed_mathsquiz_scores_all_correct_answers(self):
        core = load_module("fixed_quiz_core", FIXED / "mathsquiz" / "quiz_core.py")
        answers = iter(str(question.answer) for question in core.DEFAULT_QUESTIONS)
        output = io.StringIO()
        with redirect_stdout(output):
            score = core.run_quiz(core.DEFAULT_QUESTIONS, input_fn=lambda _prompt: next(answers))
        self.assertEqual(score, 10)
        self.assertIn("You scored 10 points", output.getvalue())

    def test_upstream_step2_final_scores_uses_global_score_bug(self):
        namespace = exec_function_prefix(UPSTREAM / "mathsquiz" / "mathsquiz-step2.py")
        namespace["score"] = 10
        output = io.StringIO()
        with redirect_stdout(output):
            namespace["print_final_scores"](3)
        self.assertIn("You scored 10 points", output.getvalue())
        self.assertNotIn("You scored 3 points", output.getvalue())

    def test_fixed_step2_final_scores_uses_parameter(self):
        core = load_module("fixed_quiz_core_step2", FIXED / "mathsquiz" / "quiz_core.py")
        output = io.StringIO()
        with redirect_stdout(output):
            core.print_final_scores(3, 10)
        self.assertIn("You scored 3 points", output.getvalue())

    def test_upstream_step3_final_scores_uses_global_score_bug(self):
        namespace = exec_function_prefix(UPSTREAM / "mathsquiz" / "mathsquiz-step3.py")
        namespace["score"] = 9
        output = io.StringIO()
        with redirect_stdout(output):
            namespace["print_final_scores"](2, 10)
        self.assertIn("You scored 9 points", output.getvalue())
        self.assertNotIn("You scored 2 points", output.getvalue())

    def test_fixed_step3_random_questions_are_testable(self):
        core = load_module("fixed_quiz_core_step3", FIXED / "mathsquiz" / "quiz_core.py")
        questions = core.random_questions(count=5, minimum=2, maximum=2)
        self.assertEqual(len(questions), 5)
        self.assertTrue(all(question.answer == 4 for question in questions))

    def test_upstream_polygons_has_syntax_error(self):
        source = (UPSTREAM / "polygons" / "polygons.py").read_text(encoding="utf-8")
        with self.assertRaises(SyntaxError):
            compile(source, "polygons.py", "exec")

    def test_fixed_polygons_calculates_general_formula(self):
        polygons = load_module("fixed_polygons", FIXED / "polygons" / "polygons.py")
        triangle = polygons.calc_polygon_details(3)
        pentagon = polygons.calc_polygon_details(5)
        self.assertEqual(triangle.internal_angles_sum, 180)
        self.assertEqual(triangle.internal_angle, 60)
        self.assertEqual(pentagon.internal_angles_sum, 540)
        self.assertEqual(pentagon.internal_angle, 108)
        self.assertEqual(pentagon.exterior_angle, 72)

    def test_fixed_polygons_rejects_invalid_side_count(self):
        polygons = load_module("fixed_polygons_invalid", FIXED / "polygons" / "polygons.py")
        with self.assertRaises(ValueError):
            polygons.calc_polygon_details(2)

    def test_fixed_folder_recreates_upstream_python_files(self):
        expected = {
            "mathsquiz/mathsquiz.py",
            "mathsquiz/mathsquiz-step1.py",
            "mathsquiz/mathsquiz-step2.py",
            "mathsquiz/mathsquiz-step3.py",
            "polygons/polygons.py",
        }
        actual = {
            str(path.relative_to(FIXED)).replace("\\", "/")
            for path in FIXED.rglob("*.py")
            if path.name != "quiz_core.py"
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
