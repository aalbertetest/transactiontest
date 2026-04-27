"""Run the self-improvement loop end-to-end.

Loop structure (3 iterations as required by the task):

    iteration 1:  generator_v1  -> 5 prompts -> evaluate -> diagnose
    iteration 2:  generator_v2  -> 5 prompts -> evaluate -> diagnose
    iteration 3:  generator_v3  -> 5 prompts -> evaluate -> diagnose

After the third evaluation, the diagnosis is fed forward to produce the
*final improved generator*: ``generator_v4``.  v4 also emits 5 sample
prompts so the reader can compare the final output against the earlier
generations.

All artifacts (per-iteration prompt batches, scored evaluations, and a
human-readable evolution log) are written to ``outputs/``.
"""
from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Dict, List

from prompt_generator.evaluator import (
    aggregate,
    diagnose,
    evaluate_batch,
)


GENERATIONS = ["generator_v1", "generator_v2", "generator_v3"]
FINAL_GENERATION = "generator_v4"

OUT_DIR = Path(__file__).parent / "outputs"
OUT_DIR.mkdir(exist_ok=True)


def run_generation(module_name: str, seed: int) -> Dict:
    mod = importlib.import_module(f"prompt_generator.{module_name}")
    prompts: List[str] = mod.generate(5, seed=seed)
    results = evaluate_batch(prompts)
    return {
        "generator": module_name,
        "seed": seed,
        "prompts": prompts,
        "results": results,
        "aggregate": aggregate(results),
        "diagnosis": diagnose(results),
    }


def render_iteration(it_no: int, data: Dict) -> str:
    lines: List[str] = []
    lines.append(f"## Iteration {it_no} — `{data['generator']}`\n")
    lines.append("**Generated prompts**\n")
    for i, p in enumerate(data["prompts"], 1):
        lines.append(f"{i}. {p}")
    lines.append("")
    lines.append("**Per-prompt evaluation**\n")
    lines.append(
        "| # | tokens | complexity | creativity | token_usage | useful | total |"
    )
    lines.append(
        "|---|--------|------------|------------|-------------|--------|-------|"
    )
    for r in data["results"]:
        s = r["scores"]
        lines.append(
            f"| {r['index']} | {r['tokens']} | {s['complexity']} | "
            f"{s['creativity']} | {s['token_usage']} | "
            f"{s['real_world_useful']} | {s['total']} |"
        )
    lines.append("")
    agg = data["aggregate"]
    lines.append(
        f"**Averages** — complexity: {agg['complexity']}, "
        f"creativity: {agg['creativity']}, "
        f"token_usage: {agg['token_usage']}, "
        f"useful: {agg['real_world_useful']}, "
        f"**total: {agg['total']}**\n"
    )
    lines.append("**Diagnosis (feeds the next generator)**\n")
    for note in data["diagnosis"]:
        lines.append(f"- {note}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    log_lines: List[str] = []
    log_lines.append("# Self-Improving Coding-Prompt Generator — Evolution Log\n")
    log_lines.append(
        "Three iterations of the loop are run in order. After each "
        "iteration the evaluator's diagnosis is used to motivate the "
        "next generator. The fourth file, `generator_v4`, is the final "
        "improved generator emitted after iteration 3.\n"
    )

    all_runs: List[Dict] = []
    for i, gen in enumerate(GENERATIONS, start=1):
        data = run_generation(gen, seed=42 + i)
        all_runs.append(data)
        log_lines.append(render_iteration(i, data))

    # final, improved generator (post-loop)
    final = run_generation(FINAL_GENERATION, seed=99)
    log_lines.append("---\n")
    log_lines.append("## Final Improved Generator — `generator_v4`\n")
    log_lines.append(
        "After three rounds of evaluate-and-rewrite, the final generator "
        "uses *candidate-and-select self-tuning*: it oversamples prompts, "
        "scores each one with the same evaluator used by the loop, and "
        "returns the top-scoring, opener-diverse subset.\n"
    )
    log_lines.append("**Sample output (5 prompts)**\n")
    for i, p in enumerate(final["prompts"], 1):
        log_lines.append(f"{i}. {p}")
    log_lines.append("")
    agg = final["aggregate"]
    log_lines.append(
        f"**v4 averages** — complexity: {agg['complexity']}, "
        f"creativity: {agg['creativity']}, "
        f"token_usage: {agg['token_usage']}, "
        f"useful: {agg['real_world_useful']}, "
        f"**total: {agg['total']}**\n"
    )

    # trajectory summary
    log_lines.append("## Score Trajectory\n")
    log_lines.append("| iteration | generator | complexity | creativity | token_usage | useful | total |")
    log_lines.append("|-----------|-----------|------------|------------|-------------|--------|-------|")
    for i, r in enumerate(all_runs, start=1):
        a = r["aggregate"]
        log_lines.append(
            f"| {i} | {r['generator']} | {a['complexity']} | "
            f"{a['creativity']} | {a['token_usage']} | "
            f"{a['real_world_useful']} | {a['total']} |"
        )
    a = final["aggregate"]
    log_lines.append(
        f"| final | {final['generator']} | {a['complexity']} | "
        f"{a['creativity']} | {a['token_usage']} | "
        f"{a['real_world_useful']} | {a['total']} |"
    )
    log_lines.append("")

    (OUT_DIR / "evolution_log.md").write_text("\n".join(log_lines))

    # per-iteration JSON dumps
    for i, r in enumerate(all_runs, start=1):
        (OUT_DIR / f"iteration_{i}_{r['generator']}.json").write_text(
            json.dumps(r, indent=2)
        )
    (OUT_DIR / f"final_{final['generator']}.json").write_text(
        json.dumps(final, indent=2)
    )

    # console summary
    print("=" * 72)
    print("Self-improvement loop complete.")
    print("=" * 72)
    for i, r in enumerate(all_runs, start=1):
        a = r["aggregate"]
        print(f"  iter {i}  {r['generator']:<14}  total={a['total']}")
    a = final["aggregate"]
    print(f"  final   {final['generator']:<14}  total={a['total']}")
    print(f"\nArtifacts written to {OUT_DIR}/")


if __name__ == "__main__":
    main()
