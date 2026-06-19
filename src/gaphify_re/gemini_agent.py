"""Gemini-backed bug-finding agent for EX04 token-efficiency evidence."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from .token_meter import estimate_tokens

DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


@dataclass(frozen=True)
class AgentPrompt:
    mode: str
    files: tuple[str, ...]
    prompt: str
    estimated_tokens: int


@dataclass(frozen=True)
class GeminiResult:
    mode: str
    model: str
    estimated_prompt_tokens: int
    response_text: str
    files_sent: tuple[str, ...]
    generated_at_utc: str


PROMPT_HEADER = """You are an AI debugging agent for EX04.
Goal: identify bugs, explain root causes, and propose fixes.
Rules:
1. Use Grphify/Obsidian evidence first when available.
2. Request or inspect raw code only after the graph-guided context identifies hot files.
3. Report root cause, fix summary, and verification evidence.
"""


MODE_FILES = {
    "naive": (
        "data/upstream_broken_python/mathsquiz/mathsquiz.py",
        "data/upstream_broken_python/mathsquiz/mathsquiz-step1.py",
        "data/upstream_broken_python/mathsquiz/mathsquiz-step2.py",
        "data/upstream_broken_python/mathsquiz/mathsquiz-step3.py",
        "data/upstream_broken_python/polygons/polygons.py",
        "fixed/broken-python/mathsquiz/quiz_core.py",
        "fixed/broken-python/polygons/polygons.py",
        "tests/test_broken_python_fixed.py",
    ),
    "graph-guided": (
        "artifacts/grphify_summary.json",
        "obsidian/index.md",
        "obsidian/hot.md",
        "reports/BROKEN_PYTHON_REPAIR_MATRIX.md",
        "tests/test_broken_python_fixed.py",
    ),
    "minimal": (
        "artifacts/grphify_summary.json",
        "obsidian/hot.md",
        "reports/BROKEN_PYTHON_REPAIR_MATRIX.md",
    ),
}


def build_agent_prompt(repo_root: Path, mode: str = "minimal") -> AgentPrompt:
    """Build the exact context packet sent to Gemini for one mode."""
    if mode not in MODE_FILES:
        raise ValueError(f"unknown mode: {mode}")
    sections = [PROMPT_HEADER.strip()]
    for relative in MODE_FILES[mode]:
        path = repo_root / relative
        sections.append(f"\n--- FILE: {relative} ---\n{path.read_text(encoding='utf-8')}")
    prompt = "\n".join(sections)
    return AgentPrompt(mode, MODE_FILES[mode], prompt, estimate_tokens(prompt))


def run_gemini_agent(repo_root: Path, mode: str = "minimal", model: str | None = None) -> GeminiResult:
    """Run Gemini on the selected prompt packet.

    Requires GEMINI_API_KEY in the environment and the optional google-genai
    dependency installed in the active virtual environment.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Copy .env.example to .env or set it in the shell.")
    prompt = build_agent_prompt(repo_root, mode)
    selected_model = model or os.environ.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Install google-genai in .venv to run Gemini: python -m pip install google-genai") from exc

    client = genai.Client(api_key=api_key)
    try:
        response = client.models.generate_content(model=selected_model, contents=prompt.prompt)
    except Exception as exc:
        response, selected_model = _retry_default_model_if_env_is_stale(
            client, prompt.prompt, selected_model, model, exc
        )
    return GeminiResult(
        prompt.mode,
        selected_model,
        prompt.estimated_tokens,
        response.text or "",
        prompt.files,
        datetime.now(timezone.utc).isoformat(),
    )


def _retry_default_model_if_env_is_stale(client, prompt: str, selected_model: str, explicit_model: str | None, exc: Exception):
    message = str(exc)
    is_missing = "NOT_FOUND" in message or "not found" in message
    if is_missing and explicit_model is None and selected_model != DEFAULT_GEMINI_MODEL:
        return client.models.generate_content(model=DEFAULT_GEMINI_MODEL, contents=prompt), DEFAULT_GEMINI_MODEL
    if is_missing:
        raise RuntimeError(
            f"Gemini model {selected_model!r} is not available for this API key. "
            f"Try `--model {DEFAULT_GEMINI_MODEL}` or run "
            "`python -m gaphify_re gemini-models --repo .` to see available models. "
            "If your .env has GEMINI_MODEL=gemini-1.5-flash, replace it with "
            f"GEMINI_MODEL={DEFAULT_GEMINI_MODEL}."
        ) from exc
    raise exc


def list_gemini_models() -> list[str]:
    """Return Gemini model names available to the configured API key."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Set it before listing models.")
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Install google-genai in .venv: python -m pip install google-genai") from exc
    client = genai.Client(api_key=api_key)
    return sorted(model.name for model in client.models.list())


def write_gemini_artifacts(repo_root: Path, result: GeminiResult) -> tuple[Path, Path]:
    """Persist the latest Gemini agent run as JSON and Markdown evidence."""
    artifacts_dir = repo_root / "artifacts"
    reports_dir = repo_root / "reports"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    json_path = artifacts_dir / "gemini_agent_result.json"
    md_path = reports_dir / "GEMINI_AGENT_REPORT.md"
    json_path.write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")
    md_path.write_text(_format_markdown_report(result), encoding="utf-8")
    return json_path, md_path


def _format_markdown_report(result: GeminiResult) -> str:
    files = "\n".join(f"- `{name}`" for name in result.files_sent)
    return f"""# Gemini Agent Report

Generated at: `{result.generated_at_utc}`

| Field | Value |
|---|---|
| Mode | `{result.mode}` |
| Model | `{result.model}` |
| Estimated prompt tokens | `{result.estimated_prompt_tokens}` |
| Files sent | `{len(result.files_sent)}` |

## Files Sent To Gemini

{files}

## Agent Output

{result.response_text}
"""
