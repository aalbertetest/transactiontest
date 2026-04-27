# Self-Improving Coding-Prompt Generator

A small, fully-deterministic harness that runs an autonomous
"evaluate → rewrite → repeat" loop over a coding-prompt generator.
Each generation is committed to its own file so the evolution is
explicit and auditable.

## Layout

```
prompt_generator/
    evaluator.py      # heuristic scorer + diagnosis
    generator_v1.py   # naive baseline (Mad-Libs)
    generator_v2.py   # domain-aware templates
    generator_v3.py   # composable scenarios + creative twists
    generator_v4.py   # final: candidate-and-select self-tuning
run_loop.py           # executes 3 iterations, then emits v4 + log
outputs/
    evolution_log.md          # human-readable evolution
    iteration_{1,2,3}_*.json  # raw per-iteration data
    final_generator_v4.json   # final-generator sample run
```

## Run

```bash
python3 run_loop.py
```

This prints a one-line summary per iteration and writes all artifacts
under `outputs/`.

## How the loop works

1. **Generate** five prompts with `generator_vN`.
2. **Evaluate** each prompt on four axes (complexity, creativity,
   token-usage, real-world usefulness). The evaluator is deterministic
   and lexicon-driven so successive generators are comparable.
3. **Diagnose** the batch: produce written notes about what was
   weakest. Those notes are the spec for the next generator.
4. **Rewrite** the generator (the next file) based on the diagnosis.
5. Repeat for three iterations. Then emit `generator_v4` as the final
   improved generator — it goes a step further by using the evaluator
   internally as a selection function (candidate-and-select), making
   the generator itself an optimizer rather than a fixed template.

## Score trajectory (run from `run_loop.py`)

| iter | generator    | complexity | creativity | token_usage | useful | total  |
|------|--------------|-----------:|-----------:|------------:|-------:|-------:|
| 1    | generator_v1 | 0.40       | 0.00       | 0.92        | 1.50   |  2.82  |
| 2    | generator_v2 | 4.60       | 0.00       | 8.15        | 8.50   | 21.25  |
| 3    | generator_v3 | 3.98       | 0.40       | 8.11        | 5.74   | 18.23  |
| final| generator_v4 | 5.88       | 2.00       | 8.16        | 7.58   | 23.62  |

Note the v2 → v3 regression on usefulness: v3 leaned into creative
framings and lost concrete deliverable signal. The v3 → v4 rewrite is
specifically a response to that regression.
