#!/usr/bin/env python3
"""Exact-decimal, explicit-policy classroom grade calculations."""
import argparse,collections,json,sys
from decimal import Decimal,InvalidOperation,ROUND_HALF_UP,ROUND_HALF_EVEN

def dec(x,name):
    if isinstance(x,bool) or not isinstance(x,(str,int,float)):raise ValueError(name+' must be numeric')
    try:v=Decimal(str(x))
    except InvalidOperation:raise ValueError(name+' must be numeric')
    if not v.is_finite():raise ValueError(name+' must be finite')
    return v

def calculate(data):
    p=data['policy'];allowed={'aggregation','missing','attempts','retake_comparable','drop_lowest','drop_min_keep','drop_missing_zeros','category_weights','empty_categories','extra_credit','allow_scores_above_max','floor_pct','cap_pct','round_digits','rounding','threshold_basis','thresholds'}
    if set(p)-allowed:raise ValueError('Unsupported policy keys: '+str(sorted(set(p)-allowed)))
    agg=p['aggregation'];missing=p['missing'];attempts=p['attempts']
    if agg not in ('points','equal_items') or missing not in ('error','exclude','zero') or attempts not in ('error','latest','highest'):raise ValueError('Invalid aggregation/missing/attempts rule')
    if p['empty_categories'] not in ('error','renormalize') or p['extra_credit'] not in ('forbid','points_bonus'):raise ValueError('Invalid empty-category/extra-credit rule')
    if not isinstance(p['allow_scores_above_max'],bool) or not isinstance(p['drop_missing_zeros'],bool):raise ValueError('Boolean policy required')
    digits=p['round_digits'];keep=p['drop_min_keep']
    if isinstance(digits,bool) or not isinstance(digits,int) or not 0<=digits<=8:raise ValueError('round_digits must be 0..8')
    if isinstance(keep,bool) or not isinstance(keep,int) or keep<1:raise ValueError('drop_min_keep must be positive integer')
    if p['rounding'] not in ('half_up','half_even') or p['threshold_basis'] not in ('raw','rounded'):raise ValueError('Invalid rounding/threshold rule')
    weights=p['category_weights']
    if weights is not None:
        if not isinstance(weights,dict) or not weights:raise ValueError('category_weights must be null or a nonempty mapping')
        weights={k:dec(v,'weight') for k,v in weights.items()}
        if any(v<=0 for v in weights.values()) or sum(weights.values())!=1:raise ValueError('Positive category weights must sum exactly to one')
    drops=p['drop_lowest']
    if isinstance(drops,dict):
        if weights is None or set(drops)-set(weights):raise ValueError('Per-category drops require declared categories')
        for v in drops.values():
            if isinstance(v,bool) or not isinstance(v,int) or v<0:raise ValueError('Drops must be nonnegative integers')
    elif isinstance(drops,bool) or not isinstance(drops,int) or drops<0:raise ValueError('Drops must be integer or category mapping')
    floor=None if p['floor_pct'] is None else dec(p['floor_pct'],'floor_pct');cap=None if p['cap_pct'] is None else dec(p['cap_pct'],'cap_pct')
    if floor is not None and cap is not None and floor>cap:raise ValueError('floor exceeds cap')
    thresholds=[]
    for t in p['thresholds']:
        v=dec(t['min'],'threshold');label=t['label']
        if not isinstance(label,str) or not label:raise ValueError('Threshold label required')
        thresholds.append((v,label))
    if len({v for v,l in thresholds})!=len(thresholds):raise ValueError('Duplicate thresholds')
    thresholds.sort(reverse=True)
    bystudent=collections.defaultdict(lambda:collections.defaultdict(list));seen=set()
    for r in data['records']:
        sid,aid=r['student_code'],r['assignment_id'];order=r['attempt_order']
        if any(not isinstance(x,str) or not x.strip() for x in (sid,aid)):raise ValueError('Student/assignment IDs required')
        if isinstance(order,bool) or not isinstance(order,int) or order<1:raise ValueError('attempt_order must be positive integer')
        key=(sid,aid,order)
        if key in seen:raise ValueError('Duplicate attempt identity')
        seen.add(key);cat=r['category']
        if weights is not None and cat not in weights:raise ValueError('Undeclared category')
        status=r['status'];bonus=r.get('extra_credit',False)
        if not isinstance(bonus,bool):raise ValueError('extra_credit must be boolean')
        if status not in ('observed','missing','exempt'):raise ValueError('Unknown status')
        possible=dec(r['possible'],'possible')
        if (bonus and possible!=0) or (not bonus and possible<=0):raise ValueError('Positive regular maximum required; points bonus uses zero maximum')
        if bonus and (p['extra_credit']!='points_bonus' or agg!='points'):raise ValueError('Bonus points require points aggregation and points_bonus policy')
        earned=r.get('earned')
        if status=='observed':
            earned=dec(earned,'earned')
            if earned<0 or (not bonus and earned>possible and not p['allow_scores_above_max']):raise ValueError('Earned score outside allowed range')
        elif earned is not None:raise ValueError('Missing/exempt scores must be null')
        bystudent[sid][aid].append({'assignment_id':aid,'attempt_order':order,'category':cat,'status':status,'earned':earned,'possible':possible,'extra_credit':bonus})
    results=[]
    for sid,assignments in sorted(bystudent.items()):
        audit=[];selected=[]
        for aid,rows in sorted(assignments.items()):
            if len({(r['category'],r['extra_credit']) for r in rows})!=1:raise ValueError('Attempt category/bonus type changed for '+aid)
            if any(r['status']=='exempt' for r in rows) and any(r['status']!='exempt' for r in rows):raise ValueError('Exemption must be consistent across assignment attempts')
            if len(rows)>1:
                if attempts=='error':raise ValueError('Multiple attempts require an explicit selection rule')
                if p.get('retake_comparable') is not True:raise ValueError('Document retake comparability before selecting attempts')
            if any(r['status']=='missing' for r in rows) and missing=='error':raise ValueError('Missing record encountered under error policy')
            # For highest: missing-to-zero participates only when that is the explicit policy;
            # otherwise nonobserved attempts cannot be ranked and are logged.
            candidates=rows
            if attempts=='highest':
                candidates=[r for r in rows if r['status']=='observed' or (r['status']=='missing' and missing=='zero')]
                if not candidates:candidates=rows
                def rank(r):
                    val=r['earned'] if r['earned'] is not None else Decimal(0)
                    return (val if r['extra_credit'] else val/r['possible'],r['attempt_order'])
                chosen=max(candidates,key=rank)
            else:chosen=max(rows,key=lambda r:r['attempt_order'])
            for r in rows:
                if r is not chosen:audit.append({'assignment_id':aid,'attempt_order':r['attempt_order'],'action':'unselected_attempt','selection_rule':attempts})
            chosen=dict(chosen)
            if chosen['status']=='exempt' or (chosen['status']=='missing' and missing=='exclude'):
                audit.append({'assignment_id':aid,'attempt_order':chosen['attempt_order'],'action':'excluded_'+chosen['status']});continue
            if chosen['status']=='missing':chosen['earned']=Decimal(0);audit.append({'assignment_id':aid,'action':'missing_converted_to_zero_by_policy'})
            selected.append(chosen);audit.append({'assignment_id':aid,'attempt_order':chosen['attempt_order'],'action':'selected','earned':str(chosen['earned']),'possible':str(chosen['possible'])})
        categories=list(weights) if weights is not None else ['__all__'];parts=[];unavailable=[]
        for cat in categories:
            rr=[r for r in selected if weights is None or r['category']==cat];regular=[r for r in rr if not r['extra_credit']];bonus=sum((r['earned'] for r in rr if r['extra_credit']),Decimal(0))
            drop_n=drops.get(cat,0) if isinstance(drops,dict) else drops
            eligible=[r for r in regular if r['status']=='observed' or p['drop_missing_zeros']]
            eligible.sort(key=lambda r:(r['earned']/r['possible'],r['assignment_id']))
            count=min(drop_n,max(0,len(regular)-keep),len(eligible));dropped=eligible[:count]
            for r in dropped:audit.append({'assignment_id':r['assignment_id'],'action':'dropped_lowest_percentage','category':cat})
            retained=[r for r in regular if r not in dropped]
            earned=sum((r['earned'] for r in retained),Decimal(0));possible=sum((r['possible'] for r in retained),Decimal(0))
            percent=None
            if retained:percent=(earned+bonus)/possible*100 if agg=='points' else sum((r['earned']/r['possible'] for r in retained),Decimal(0))/len(retained)*100
            else:unavailable.append(cat)
            parts.append({'category':cat,'regular_retained_n':len(retained),'earned_regular':str(earned),'possible_regular':str(possible),'bonus_points':str(bonus),'percent':None if percent is None else str(percent),'requested_drops':drop_n,'actual_drops':count,'retained_assignments':[r['assignment_id'] for r in retained]})
        final=None;active=[r for r in parts if r['percent'] is not None];renorm=False
        if active and not (unavailable and p['empty_categories']=='error'):
            if weights is None:final=dec(active[0]['percent'],'percent')
            else:
                mass=sum(weights[r['category']] for r in active);final=sum(dec(r['percent'],'percent')*weights[r['category']] for r in active)/mass;renorm=bool(unavailable)
        before=final;rounded=None;label=None
        if final is not None:
            if floor is not None:final=max(final,floor)
            if cap is not None:final=min(final,cap)
            mode=ROUND_HALF_UP if p['rounding']=='half_up' else ROUND_HALF_EVEN
            rounded=final.quantize(Decimal(1).scaleb(-digits),rounding=mode)
            basis=final if p['threshold_basis']=='raw' else rounded
            label=next((lab for minimum,lab in thresholds if basis>=minimum),None)
        results.append({'student_code':sid,'status':'computed_for_review' if final is not None else 'insufficient_evidence_or_category_coverage','categories':parts,'missing_categories':unavailable,'weights_renormalized':renorm,'percent_before_floor_cap':None if before is None else str(before),'percent_unrounded':None if final is None else str(final),'percent_rounded':None if rounded is None else str(rounded),'threshold_label':label,'audit':audit})
    return {'policy':p,'students':results,'limits':['Results implement the stated policy for teacher review; they are not official grade changes.','Drops use lowest percentage, with assignment-ID tie break, not optimization of final grade.','Latest attempt selection precedes missing exclusion; highest ranks observed scores and explicit missing-zero values.','A points bonus with no retained regular denominator cannot produce a grade.','Final caps/floors and display rounding do not alter source scores.']}

def main():
    a=argparse.ArgumentParser();a.add_argument('input');a.add_argument('output');args=a.parse_args()
    try:
        with open(args.input) as f:d=json.load(f)
        r=calculate(d)
        with open(args.output,'w') as f:json.dump(r,f,indent=2,allow_nan=False);f.write('\n')
    except (ValueError,KeyError,TypeError,InvalidOperation) as e:print('Input error: '+str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
