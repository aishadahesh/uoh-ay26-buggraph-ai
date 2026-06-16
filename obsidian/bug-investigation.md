# Bug Investigation

## Before

The upstream snapshot used one loop for parsing, validation, and insertion. That made row order part of correctness.

## Investigation Steps

1. Build a graph from the local source tree.
2. Start from `index.md` and `hot.md` instead of loading all files.
3. Follow the parser-to-scheduler edge.
4. Reproduce the failing forward dependency case.
5. Add a regression test before confirming the fix.

## After

`parse_plan` separates parsing from validation. Row order no longer affects valid dependency declarations.
