# Token Efficiency Report

## Compared Modes

| Mode | Files / units read | Estimated tokens | Iterations | Result |
|---|---:|---:|---:|---|
| Naive raw-code reading | 15 files | 6,166 | 5 | Broad but noisy |
| Graph-guided reading | 5 files | 3,266 | 2 | Focused root cause |

## Interpretation

The naive mode reads all project source and upstream Python files before forming a repair hypothesis. The graph-guided mode starts from `obsidian/index.md`, `obsidian/hot.md`, and focused reports, then drills into only the broken-python repair path.

The graph-guided path saves about 47 percent of estimated context tokens while still finding the important bugs: syntax failures, global-score coupling, invalid polygon construction, and formula/drawing defects.

## Counting Method

The project uses a transparent approximation of four characters per token. Both modes use the same estimator, so the comparison is useful even if the exact tokenizer differs from a production LLM tokenizer.
