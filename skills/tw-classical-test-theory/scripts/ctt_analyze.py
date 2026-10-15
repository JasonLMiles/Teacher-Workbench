#!/usr/bin/env python3
"""Auditable classroom CTT descriptives. No network; standard-library Python only."""
import argparse
import collections
import csv
import hashlib
import json
import math
import platform
import statistics
from pathlib import Path

VERSION = '1.0.0'

def pearson(xs, ys):
    if len(xs) < 2:
        return None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    xx = sum((x-mx)**2 for x in xs)
    yy = sum((y-my)**2 for y in ys)
    if xx == 0 or yy == 0:
        return None
    value = sum((x-mx)*(y-my) for x, y in zip(xs, ys)) / math.sqrt(xx*yy)
    return max(-1.0, min(1.0, value))

def analyze(csv_path, config_path):
    csv_path, config_path = Path(csv_path), Path(config_path)
    cfg = json.loads(config_path.read_text(encoding='utf-8'))
    mode = cfg.get('mode')
    if mode not in ('raw', 'scored'):
        raise ValueError('mode must be raw or scored')
    idcol = cfg.get('id_column', 'anonymous_id')
    items = cfg.get('items')
    if not isinstance(items, dict) or not items or idcol in items:
        raise ValueError('items must be a nonempty item-ID object, separate from id_column')
    item_ids = list(items)
    omitted_policy = cfg.get('omitted_policy')
    invalid_policy = cfg.get('invalid_policy', 'error')
    blank_rule = cfg.get('blank_rule', 'error')
    if omitted_policy not in ('zero', 'missing'):
        raise ValueError('explicit omitted_policy must be zero or missing')
    if invalid_policy not in ('error', 'missing'):
        raise ValueError('invalid_policy must be error or missing')
    if blank_rule not in ('error', 'omitted', 'not_administered', 'invalid'):
        raise ValueError('invalid blank_rule')
    tokens = cfg.get('missing_tokens', {'omitted':'OM','not_administered':'NA','invalid':'INV'})
    if set(tokens) != {'omitted','not_administered','invalid'} or any(not isinstance(t,str) or not t.strip() or t != t.strip() for t in tokens.values()) or len(set(tokens.values())) != 3:
        raise ValueError('missing_tokens must have three distinct nonempty trimmed strings')
    token_kinds = {v:k for k,v in tokens.items()}
    maxima = {}
    for item, spec in items.items():
        if not isinstance(spec, dict):
            raise ValueError('each item specification must be an object')
        if mode == 'raw':
            choices = spec.get('choices')
            key = spec.get('key')
            if not isinstance(choices,list) or len(choices)<2 or any(not isinstance(c,str) or not c or c != c.strip() for c in choices) or len(set(choices)) != len(choices) or key not in choices:
                raise ValueError(f'{item}: provide distinct string choices and a key among them')
            if set(choices).intersection(token_kinds):
                raise ValueError(f'{item}: choices collide with missing tokens')
            maxima[item] = 1.0
        else:
            maximum = spec.get('max_score')
            if isinstance(maximum,bool) or not isinstance(maximum,(int,float)) or not math.isfinite(maximum) or maximum <= 0:
                raise ValueError(f'{item}: max_score must be finite and positive')
            for token in token_kinds:
                try:
                    float(token)
                except ValueError:
                    continue
                raise ValueError('scored-mode missing tokens must be nonnumeric')
            maxima[item] = float(maximum)
    counts = {i:collections.Counter() for i in items}
    options = {i:collections.Counter() for i in items}
    scores = []
    ids = set()
    with csv_path.open(newline='',encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError('CSV needs unique column headers')
        if set(reader.fieldnames) != {idcol,*item_ids}:
            raise ValueError('CSV columns must be exactly id_column plus configured items; remove unnecessary personal/group fields')
        for rownum, row in enumerate(reader,start=2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'row {rownum}: wrong number of fields')
            anon = row[idcol].strip()
            if not anon or anon in ids:
                raise ValueError(f'row {rownum}: anonymous ID missing or duplicated')
            ids.add(anon)
            scored = []
            for item in items:
                value = row[item].strip()
                kind = token_kinds.get(value)
                if value == '':
                    if blank_rule == 'error':
                        raise ValueError(f'row {rownum}, {item}: blank is ambiguous; set blank_rule explicitly')
                    kind = blank_rule
                if kind:
                    counts[item][kind] += 1
                    if kind == 'invalid' and invalid_policy == 'error':
                        raise ValueError(f'row {rownum}, {item}: invalid response; inspect or explicitly choose invalid_policy=missing')
                    scored.append(0.0 if kind=='omitted' and omitted_policy=='zero' else None)
                    continue
                if mode == 'raw':
                    if value not in items[item]['choices']:
                        if invalid_policy == 'error':
                            raise ValueError(f'row {rownum}, {item}: response not among configured choices')
                        counts[item]['invalid'] += 1
                        scored.append(None)
                        continue
                    options[item][value] += 1
                    score = float(value == items[item]['key'])
                else:
                    try:
                        score = float(value)
                    except ValueError as e:
                        raise ValueError(f'row {rownum}, {item}: nonnumeric score') from e
                    if not math.isfinite(score) or not 0 <= score <= maxima[item]:
                        raise ValueError(f'row {rownum}, {item}: score must be finite and between 0 and max_score')
                counts[item]['observed_valid'] += 1
                scored.append(score)
            scores.append(scored)
    if not scores:
        raise ValueError('CSV contains no examinee rows')
    complete = [r for r in scores if all(s is not None for s in r)]
    k, n = len(items), len(complete)
    totals = [sum(r) for r in complete]
    warnings = []
    if n != len(scores):
        warnings.append('Reliability, corrected item-total and total-score summaries use listwise complete cases; omitted-as-zero counts as scored. Per-item descriptives use available scored responses. Compare denominators.')
    if n < 30:
        warnings.append('Small complete-case classroom sample: treat results as descriptive and potentially unstable. This 30-case warning is a convenience flag, not an adequacy threshold.')
    if cfg.get('example_status') == 'synthetic':
        warnings.append('SYNTHETIC EXAMPLE: these are not actual students or calibrated items.')
    per_item = []
    for j,item in enumerate(item_ids):
        available = [r[j] for r in scores if r[j] is not None]
        corr = pearson([r[j] for r in complete], [sum(r)-r[j] for r in complete]) if k>1 else None
        if corr is not None and corr < 0:
            warnings.append(f'{item}: negative corrected item-total correlation; inspect key, content, data and assumptions. Key was not changed.')
        rec = {'item':item,'max_score':maxima[item],'n_rows':len(scores),'n_scored':len(available),
               'n_observed_valid':counts[item]['observed_valid'],'n_omitted':counts[item]['omitted'],
               'n_not_administered':counts[item]['not_administered'],'n_invalid':counts[item]['invalid'],
               'mean_score':statistics.mean(available) if available else None,
               'facility_mean_over_max':statistics.mean(available)/maxima[item] if available else None,
               'corrected_item_total_complete_cases':corr,'corrected_item_total_n':n}
        if mode=='raw':
            rec['key'] = items[item]['key']
            rec['option_counts_observed_valid'] = {c:options[item][c] for c in items[item]['choices']}
        per_item.append(rec)
    alpha = None
    sem = None
    total_var = statistics.variance(totals) if n>=2 else None
    if k>=2 and n>=2 and total_var > 0:
        item_vars = [statistics.variance([r[j] for r in complete]) for j in range(k)]
        alpha = k/(k-1)*(1-sum(item_vars)/total_var)
        if 0 <= alpha <= 1:
            sem = math.sqrt(total_var)*math.sqrt(1-alpha)
        else:
            warnings.append('Alpha is outside [0,1]; it is reported without clipping and conventional SEM is withheld. Inspect structure/scoring/sample before interpretation.')
    else:
        warnings.append('Alpha/SEM unavailable: need at least two items, two complete cases, and positive total-score variance.')
    return {'analysis':'classical_test_theory_descriptives','calculator_version':VERSION,
            'example_status':cfg.get('example_status','not_declared'),
            'provenance':{'python':platform.python_version(),'data_file':csv_path.name,'data_sha256':hashlib.sha256(csv_path.read_bytes()).hexdigest(),'config_file':config_path.name,'config_sha256':hashlib.sha256(config_path.read_bytes()).hexdigest()},
            'scoring':cfg,'n_rows':len(scores),'n_items':k,'n_complete_cases':n,'n_incomplete_cases':len(scores)-n,
            'total_score_complete_cases':{'maximum':sum(maxima.values()),'mean':statistics.mean(totals) if totals else None,'sample_sd':math.sqrt(total_var) if total_var is not None else None,'minimum':min(totals) if totals else None,'maximum_observed':max(totals) if totals else None},
            'alpha_complete_cases':alpha,'conventional_sem_complete_cases':sem,
            'items':per_item,'warnings':warnings,
            'interpretation_limits':['No validity, unidimensionality, classification accuracy or mastery claim follows from alpha.','No confidence intervals or rater/test-retest reliability are estimated by this calculator.','Per-item available-case facilities may describe different subsets; use the reported denominators.','No IRT calibration, linking, equating or automatic key correction is performed.']}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',required=True)
    parser.add_argument('--config',required=True)
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    output=Path(args.output)
    if output.resolve() in (Path(args.data).resolve(),Path(args.config).resolve()):
        parser.error('output must not overwrite raw data or configuration')
    try:
        result=analyze(args.data,args.config)
    except (ValueError,KeyError,TypeError,OSError) as e:
        parser.error(str(e))
    output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(f'Wrote {output.name}: {result["n_rows"]} rows, {result["n_complete_cases"]} complete cases; inspect warnings.')

if __name__=='__main__':
    main()
