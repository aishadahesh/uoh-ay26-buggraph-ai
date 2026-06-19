"""Command-line entry points for the EX04 project."""

from __future__ import annotations

import argparse
from pathlib import Path

from .agent_workflow import run_workflow
from .crew_agent import run_crewai_bug_hunt
from .gemini_agent import build_agent_prompt, list_gemini_models, run_gemini_agent, write_gemini_artifacts
from .grphify_runner import write_grphify_outputs
from .parser import parse_plan
from .scheduler import schedule
from .token_meter import compare_modes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="EX04 graph-guided reverse engineering tools")
    parser.add_argument("command", choices=["graph", "agent", "crew", "gemini", "gemini-models", "gemini-prompt", "tokens", "demo"])
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--mode", choices=["naive", "graph-guided", "minimal"], default="minimal")
    parser.add_argument("--model", default=None)
    args = parser.parse_args(argv)

    if args.command == "graph":
        graph = write_grphify_outputs(args.repo)
        print(f"wrote {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")
        return 0
    if args.command == "agent":
        state = run_workflow(args.repo, "Which broken-python files fail, and how were they repaired?")
        print(state.root_cause)
        print(state.fix_summary)
        print(f"estimated tokens: {state.token_estimate}")
        return 0
    if args.command == "crew":
        result = run_crewai_bug_hunt(args.repo)
        print(result.root_cause)
        print(result.fix_summary)
        print(f"estimated tokens: {result.estimated_tokens}")
        return 0
    if args.command == "gemini-models":
        for model_name in list_gemini_models():
            print(model_name)
        return 0
    if args.command == "gemini-prompt":
        prompt = build_agent_prompt(args.repo, args.mode)
        print(f"mode: {prompt.mode}")
        print(f"files: {len(prompt.files)}")
        print(f"estimated prompt tokens: {prompt.estimated_tokens}")
        return 0
    if args.command == "gemini":
        result = run_gemini_agent(args.repo, args.mode, args.model)
        json_path, md_path = write_gemini_artifacts(args.repo, result)
        print(f"mode: {result.mode}")
        print(f"model: {result.model}")
        print(f"estimated prompt tokens: {result.estimated_prompt_tokens}")
        print(f"updated: {json_path}")
        print(f"updated: {md_path}")
        print(result.response_text)
        return 0
    if args.command == "demo":
        text = "deploy | Deploy app | 1 | test\ntest | Run tests | 2 |"
        plan = parse_plan(text)
        print(schedule(plan))
        return 0

    for mode in compare_modes(args.repo):
        print(f"{mode.name}: {mode.estimated_tokens} tokens, {mode.files_read} files, {mode.iterations} iterations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
