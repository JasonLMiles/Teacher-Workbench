#!/usr/bin/env python3
"""Explicit-policy standards summaries and one-level domain rollups."""
import argparse,collections,datetime,json,math,statistics,sys

def number(x,name):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x):raise ValueError(name+' must be finite numeric data')
    return float(x)
def analyze(data):
    p=data['policy'];allowed={'method','window','min_evidence','scale_type','interval_assumption','decay','threshold','as_of','stale_days','levels','scale_min','scale_max'}
    if set(p)-allowed:raise ValueError('Unsupported policy keys: '+str(sorted(set(p)-allowed)))
    method=p['method'];methods={'latest','highest','median_low','mode_recent','recent_consistent_min','mean','decaying_mean'}
    if method not in methods:raise ValueError('Unsupported method')
    scale=p['scale_type']
    if scale not in ('ordinal','interval'):raise ValueError('Unsupported scale_type')
    numeric_ok=scale=='interval' and p.get('interval_assumption') is True
    if method in ('mean','decaying_mean') and not numeric_ok:raise ValueError('Numeric aggregation requires an explicit interval-like assumption')
    asof=datetime.date.fromisoformat(p['as_of']);threshold=number(p['threshold'],'threshold')
    minimum=p['min_evidence'];window=p['window'];stale=p['stale_days']
    if isinstance(minimum,bool) or not isinstance(minimum,int) or minimum<1:raise ValueError('min_evidence must be positive integer')
    if window is not None and (isinstance(window,bool) or not isinstance(window,int) or window<minimum):raise ValueError('window must be null or integer >= min_evidence')
    if isinstance(stale,bool) or not isinstance(stale,int) or stale<0:raise ValueError('stale_days must be nonnegative integer')
    levels=p.get('levels')
    if scale=='ordinal':
        if not isinstance(levels,list) or not levels:raise ValueError('Ordered numeric levels required for ordinal data')
        levels=[number(x,'level') for x in levels]
        if levels!=sorted(set(levels)) or threshold not in levels:raise ValueError('Levels must be unique/increasing and include threshold')
    else:
        low=number(p['scale_min'],'scale_min');high=number(p['scale_max'],'scale_max')
        if low>=high or not low<=threshold<=high:raise ValueError('Invalid scale range/threshold')
    decay=number(p.get('decay',.5),'decay')
    if not 0<decay<=1:raise ValueError('decay must be >0 and <=1')
    standards=data['standards']
    if not standards or any(not isinstance(x,str) or not x.strip() for x in standards) or len(set(standards))!=len(standards):raise ValueError('Unique standard IDs required')
    roster=data.get('students',sorted({r['student_code'] for r in data['records']}))
    if any(not isinstance(x,str) or not x.strip() for x in roster) or len(set(roster))!=len(roster):raise ValueError('Unique student codes required')
    groups=collections.defaultdict(list);seen=set();order_seen=set();excluded=[]
    for r in data['records']:
        sid,std,tid=r['student_code'],r['standard_id'],r['task_id']
        if sid not in roster or std not in standards or not isinstance(tid,str) or not tid:raise ValueError('Unknown student/standard or missing task ID')
        key=(sid,std,tid)
        if key in seen:raise ValueError('Duplicate evidence task; give reassessments distinct task IDs')
        seen.add(key);date=datetime.date.fromisoformat(r['date']);seq=r.get('sequence',0)
        if isinstance(seq,bool) or not isinstance(seq,int) or seq<0:raise ValueError('sequence must be nonnegative integer')
        ok=(sid,std,date,seq)
        if ok in order_seen:raise ValueError('Ambiguous same-day evidence: supply distinct sequence values')
        order_seen.add(ok);status=r['status'];value=r.get('value')
        if status not in ('observed','missing','absent','not_assessed','exempt'):raise ValueError('Unknown evidence status')
        if status=='observed':
            value=number(value,'value')
            if (scale=='ordinal' and value not in levels) or (scale=='interval' and not low<=value<=high):raise ValueError('Value outside declared scale')
        elif value is not None:raise ValueError('Nonobserved evidence must have null value')
        if date>asof:excluded.append({'student_code':sid,'standard_id':std,'task_id':tid,'reason':'after_as_of'});continue
        groups[(sid,std)].append(dict(r,value=value,_date=date,_seq=seq))
    rows=[];index={}
    for sid in roster:
        for std in standards:
            allrows=sorted(groups[(sid,std)],key=lambda r:(r['_date'],r['_seq']))
            observed=[r for r in allrows if r['status']=='observed'];selected=observed[-window:] if window else observed
            vals=[r['value'] for r in selected];n=len(vals);estimate=None
            if n>=minimum:
                if method=='latest':estimate=vals[-1]
                elif method=='highest':estimate=max(vals)
                elif method in ('median_low','recent_consistent_min'):estimate=statistics.median_low(vals) if method=='median_low' else min(vals)
                elif method=='mode_recent':
                    c=collections.Counter(vals);best=max(c.values());estimate=next(x for x in reversed(vals) if c[x]==best)
                elif method=='mean':estimate=statistics.mean(vals)
                else:
                    weights=[decay**(n-i-1) for i in range(n)];estimate=sum(v*w for v,w in zip(vals,weights))/sum(weights)
            trajectory=[{k:v for k,v in r.items() if not k.startswith('_')} for r in allrows]
            age=(asof-observed[-1]['_date']).days if observed else None
            slope=None
            if numeric_ok and len(observed)>=3 and len({r['_date'] for r in observed})>=3:
                xx=[(r['_date']-observed[0]['_date']).days for r in observed];yy=[r['value'] for r in observed];xm=statistics.mean(xx);ym=statistics.mean(yy)
                slope=sum((x-xm)*(y-ym) for x,y in zip(xx,yy))/sum((x-xm)**2 for x in xx)
            transitions=collections.Counter((a['value'],b['value']) for a,b in zip(observed,observed[1:]))
            result={'student_code':sid,'standard_id':std,'status':'insufficient_evidence' if estimate is None else 'summarized','summary':estimate,'meets_threshold':None if estimate is None else estimate>=threshold,'observed_n':len(observed),'selected_n':n,'selected_task_ids':[r['task_id'] for r in selected],'missing_states':dict(collections.Counter(r['status'] for r in allrows if r['status']!='observed')),'latest_age_days':age,'stale':None if age is None else age>stale,'observed_range':[min(r['value'] for r in observed),max(r['value'] for r in observed)] if observed else None,'consistent_selected_fraction':max(collections.Counter(vals).values())/n if n else None,'descriptive_slope_per_day':slope,'transitions':[{'from':a,'to':b,'count':v} for (a,b),v in transitions.items()],'chronology':trajectory}
            rows.append(result);index[(sid,std)]=result
    rollups=[];roll_ids=set()
    for rule in data.get('rollups',[]):
        rid=rule['id'];members=rule['members'];rm=rule['method'];coverage=number(rule['min_coverage'],'min_coverage');essential=rule.get('essential',[])
        if not isinstance(rid,str) or not rid or rid in roll_ids or rid in standards:raise ValueError('Rollup IDs must be unique')
        roll_ids.add(rid)
        if not members or len(set(members))!=len(members) or any(x not in standards for x in members):raise ValueError('Rollups require unique leaf standard IDs; nested rollups are not supported')
        if not 0<coverage<=1 or any(x not in members for x in essential):raise ValueError('Invalid coverage or essential members')
        if rm not in ('minimum','proportion_meeting','weighted_mean'):raise ValueError('Unsupported rollup method')
        weights=rule.get('weights',{})
        if rm=='weighted_mean':
            if not numeric_ok:raise ValueError('Weighted numeric rollup requires interval-like assumption')
            if set(weights)!=set(members) or any(number(v,'weight')<=0 for v in weights.values()) or not math.isclose(sum(weights.values()),1,abs_tol=1e-9):raise ValueError('Positive member weights must sum to one')
        for sid in roster:
            valid={k:index[(sid,k)]['summary'] for k in members if index[(sid,k)]['summary'] is not None};frac=len(valid)/len(members);met=sum(v>=threshold for v in valid.values());missing_ess=[k for k in essential if k not in valid];unmet_ess=[k for k in essential if k in valid and valid[k]<threshold]
            value=None
            if frac>=coverage:
                if rm=='minimum':value=min(valid.values())
                elif rm=='proportion_meeting':value=met/len(valid)
                else:value=sum(valid[k]*weights[k] for k in valid)/sum(weights[k] for k in valid)
            rollups.append({'student_code':sid,'rollup_id':rid,'method':rm,'value':value,'status':'insufficient_coverage' if value is None else 'summarized','member_n':len(members),'observed_member_n':len(valid),'coverage':frac,'meeting_n':met,'meeting_rate_observed':met/len(valid) if valid else None,'meeting_rate_all_required':met/len(members),'missing_members':[k for k in members if k not in valid],'essential_missing':missing_ess,'essential_not_meeting':unmet_ess,'essential_gate_met':not missing_ess and not unmet_ess,'weight_renormalization':rm=='weighted_mean' and len(valid)<len(members)})
    return {'policy':p,'audit':{'input_records':len(data['records']),'excluded':excluded,'student_n':len(roster),'standard_n':len(standards)},'profiles':rows,'rollups':rollups,'limits':['Summaries follow supplied policy and are not final grades.','Lower median is an observed category; ties in mode use the most recent tied category.','Slopes are descriptive for interval-like evidence only; no causal claim or forecast.','One-level rollups include coverage and essential-standard flags; the numeric result alone is not a course grade.']}

def main():
    a=argparse.ArgumentParser();a.add_argument('input');a.add_argument('output');args=a.parse_args()
    try:
        with open(args.input) as f:d=json.load(f)
        r=analyze(d)
        with open(args.output,'w') as f:json.dump(r,f,indent=2,allow_nan=False);f.write('\n')
    except (ValueError,KeyError,TypeError) as e:print('Input error: '+str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
