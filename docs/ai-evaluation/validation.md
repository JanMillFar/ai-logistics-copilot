# Validation record

Date: 28 October 2026. Python 3.12.14; pandas 2.2.3.

Command: `python -m unittest discover -s docs/ai-evaluation/tests -v`

Result: 7 tests executed, 7 passed. Reviewed source blob hashes checked before execution.

- Baseline inventory value: 20.
- Duplicate sales join: value changes from 20 to 40.
- Missing sales record: value changes from 40 to 20.
- Zero stock and zero demand: coverage 999, classified healthy by the app rule.
- Negative sales: coverage 999.
- Unrounded coverage 6.96: returned coverage 7.0.
- Empty population: health score 0, Critical.

The join is reconstructed from app.py at the reviewed commit. The Python functions are pinned snapshots. This is an offline component review; UI flows, external AI responses and end-to-end production behaviour were not tested. Passing reproduction tests confirms observed limitations, not fixes.

The six conversation cards are unexecuted; two scoring examples are authored controls. No live-model pass rate is reported.
