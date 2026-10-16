# Response data and reproducible run

Requires Python 3.9+ with the standard library. No network or additional package is used. Run from this skill directory, or substitute its actual absolute path. Keep real data and outputs in the user's authorized task workspace, not inside this reusable skill.

```bash
python3 scripts/ctt_analyze.py --data assets/synthetic-responses.csv --config assets/scoring-config.json --output ctt-example-result.json
```

The included CSV is synthetic. Expected complete-case results: four rows; total scores 3, 2, 1, 0; mean 1.5; sample variance 5/3; facilities 0.75, 0.50, 0.25; alpha 0.75; conventional SEM `sqrt(5/12)` ≈ 0.645497. This tiny dataset illustrates arithmetic, not reliable population inference.

## Schema
CSV: exactly one anonymous-ID column plus the configured item columns. No names, emails or unnecessary group fields. One examinee per row; unique nonempty anonymous IDs. Raw response mode uses exact case-sensitive choice labels. Scored mode uses finite numeric values from zero through each item's maximum. Keep item-to-standard/construct mapping, response conditions and correction log in a separate authorized record.

JSON configuration:
- `mode`: `raw` or `scored`.
- `id_column`: ID header, defaults to `anonymous_id`.
- `items`: object keyed by item IDs. Raw specifications require string `key` and distinct `choices`. Scored specifications require positive `max_score`.
- `missing_tokens`: distinct strings for `omitted`, `not_administered`, and `invalid`; default OM, NA, INV. These are preserved in separate counts.
- `omitted_policy`: required `zero` or `missing`, chosen from the intended scoring rule, not silently assumed.
- `invalid_policy`: `error` (default) or `missing`. Unknown raw choices follow this rule; numeric scores outside range are always errors.
- `blank_rule`: defaults to `error`; explicitly select `omitted`, `not_administered`, or `invalid` only if the data definition supports it.
- `example_status`: set `synthetic` for simulated/tutorial data; use `real_deidentified` for actual authorized data.

Not-administered responses are always missing, not wrong. An omitted-as-zero response counts as scored in complete-case analyses. Blank, invalid and not-administered are not interchangeable. Output includes software/version, file hashes, exact configuration, denominators and warnings. The script never changes raw files or keys; confirmed corrections require a new version and audit note. Output contains aggregate statistics, no examinee IDs.

For scored responses, an item configuration could be `{"Q1":{"max_score":2},"Q2":{"max_score":4}}`. This computes raw-score alpha and facility normalized by the item maximum; it does not standardize item variances or decide whether the weighted composite is defensible.
