#!/usr/bin/env python3
"""Validate evidence ratings and summarize coverage; does not judge pedagogy."""
import argparse,json,sys
from pathlib import Path
DEFAULT=Path(__file__).resolve().parents[1]/'assets/rubrics.json'
STATUSES={'pass','fail','not_applicable','insufficient_evidence'}
def report(review,rubric=None):
    rub=rubric or json.loads(DEFAULT.read_text())
    if not review.get('artifact') or not review.get('reviewer'):raise ValueError('Identify artifact and reviewer')
    sets=review.get('sets',[])
    if not isinstance(sets,list) or 'common' not in sets or len(sets)!=len(set(sets)):raise ValueError('Select common and unique applicable sets')
    if any(s not in rub['sets'] for s in sets):raise ValueError('Unknown criterion set')
    criteria={c['id']:dict(c,set=s) for s in sets for c in rub['sets'][s]}
    ratings={}
    for r in review.get('ratings',[]):
        cid=r.get('id');status=r.get('status')
        if cid not in criteria or cid in ratings:raise ValueError('Unknown or duplicate criterion '+str(cid))
        if status not in STATUSES or not str(r.get('reason','')).strip():raise ValueError('Rating needs valid status and reason')
        if status in ('pass','fail') and not str(r.get('locator','')).strip():raise ValueError('Pass/fail needs artifact locator')
        if status=='not_applicable' and criteria[cid].get('required'):raise ValueError('Required criterion cannot be omitted: '+cid)
        ratings[cid]=r
    rows=[dict(c,**{k:v for k,v in ratings.get(cid,{'status':'unreviewed','reason':'No rating supplied','locator':''}).items() if k!='id'}) for cid,c in criteria.items()]
    blockers=[r['id'] for r in rows if r['status']=='fail' and r['severity']=='blocker']
    unresolved=[r['id'] for r in rows if r['status'] in ('unreviewed','insufficient_evidence')]
    failed=[r['id'] for r in rows if r['status']=='fail']
    disposition='revise_before_use' if blockers else 'incomplete_review' if unresolved else 'revise_before_use' if failed else 'selected_checks_passed'
    return {'artifact':review['artifact'],'reviewer':review['reviewer'],'rubric_version':rub['version'],'sets':sets,'excluded_sets':review.get('excluded_sets',{}),'disposition':disposition,'blockers':blockers,'unresolved':unresolved,'counts':{s:sum(r['status']==s for r in rows) for s in sorted(STATUSES|{'unreviewed'})},'ratings':rows,'limit':'Summarizes supplied reviewer judgments only; no claim of classroom efficacy, psychometric validity or independent automated pedagogical evaluation.'}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('ratings');p.add_argument('--rubric');p.add_argument('--out',required=True);a=p.parse_args()
    try:r=report(json.loads(Path(a.ratings).read_text()),json.loads(Path(a.rubric).read_text()) if a.rubric else None);Path(a.out).write_text(json.dumps(r,indent=2)+'\n');print(r['disposition'])
    except (ValueError,OSError,KeyError,TypeError) as e:print(str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
