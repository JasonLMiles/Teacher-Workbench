#!/usr/bin/env python3
"""Descriptive matched pre/post analysis; no network or gradebook writes."""
import argparse,json,math,statistics,sys

def num(v,label):
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):raise ValueError(label+' must be a finite number')
    return float(v)
def analyze(data):
    p=data['policy']
    allowed={'comparable','comparability_note','analysis_scale','direction','score_min','score_max','pre_max','post_max','inference','confidence','normalized_gain'}
    if set(p)-allowed:raise ValueError('Unsupported policy keys: '+str(sorted(set(p)-allowed)))
    if p.get('comparable') is not True or not str(p.get('comparability_note','')).strip():raise ValueError('Document comparability before calculating growth')
    scale=p['analysis_scale'];direction=p['direction']
    if scale not in ('raw','percentage') or direction not in ('higher','lower'):raise ValueError('Invalid analysis_scale or direction')
    for flag in ('inference','normalized_gain'):
        if flag in p and not isinstance(p[flag],bool):raise ValueError(flag+' must be boolean')
    if scale=='raw':
        lo=num(p['score_min'],'score_min');hi=num(p['score_max'],'score_max')
        if hi<=lo:raise ValueError('score_max must exceed score_min')
    else:
        for k in ('pre_max','post_max'):
            if num(p[k],k)<=0:raise ValueError(k+' must be positive')
        lo,hi=0.,100.
    if p.get('normalized_gain',False) and direction!='higher':raise ValueError('Normalized gain supported only for higher-is-better bounded scores')
    def wave(key):
        out={}
        for r in data[key]:
            sid=r['student_code']
            if not isinstance(sid,str) or not sid.strip() or sid in out:raise ValueError('Missing or duplicate learner ID in '+key)
            status=r['status'];score=r.get('score')
            if status not in ('observed','missing','absent','not_administered','exempt'):raise ValueError('Unknown status')
            if status=='observed':
                score=num(score,'score');upper=hi if scale=='raw' else float(p[key+'_max']);lower=lo if scale=='raw' else 0.
                if not lower<=score<=upper:raise ValueError('Score outside bounds for '+sid)
                if scale=='percentage':score=score/upper*100.
            elif score is not None:raise ValueError('Nonobserved scores must be null')
            out[sid]={'status':status,'score':score}
        return out
    pre,post=wave('pre'),wave('post');pairs=[];excluded=[];sign=1 if direction=='higher' else -1
    for sid in sorted(set(pre)|set(post)):
        a=pre.get(sid,{'status':'no_record','score':None});b=post.get(sid,{'status':'no_record','score':None})
        if a['status']!='observed' or b['status']!='observed':
            excluded.append({'student_code':sid,'pre_status':a['status'],'post_status':b['status']});continue
        x,y=a['score'],b['score'];d=y-x
        row={'student_code':sid,'pre':x,'post':y,'change_post_minus_pre':d,'direction_adjusted_improvement':sign*d,'relative_percent_change':None if x==0 else 100*d/x}
        if p.get('normalized_gain',False):row['normalized_gain']=None if x==hi else d/(hi-x)
        pairs.append(row)
    n=len(pairs);xs=[r['pre'] for r in pairs];ys=[r['post'] for r in pairs];ds=[r['change_post_minus_pre'] for r in pairs]
    avg=lambda a:statistics.mean(a) if a else None
    sd=lambda a:statistics.stdev(a) if len(a)>1 else None
    mx,my,md=avg(xs),avg(ys),avg(ds);sx,sy,sdiff=sd(xs),sd(ys),sd(ds)
    sav=None if sx is None else (sx+sy)/2
    ratios={'d_z_change_over_sd_change':md/sdiff if sdiff else None,'d_av_change_over_mean_pre_post_sd':md/sav if sav else None,'change_over_baseline_sd':md/sx if sx else None}
    summary={'matched_n':n,'pre_mean_matched':mx,'post_mean_matched':my,'mean_change':md,'median_change':statistics.median(ds) if ds else None,'sd_change':sdiff,'min_change':min(ds) if ds else None,'max_change':max(ds) if ds else None,'improved':sum(sign*d>0 for d in ds),'unchanged':sum(d==0 for d in ds),'declined':sum(sign*d<0 for d in ds),'pre_at_ceiling':sum(x==hi for x in xs),'post_at_ceiling':sum(y==hi for y in ys),'standardized_change':ratios}
    if p.get('normalized_gain',False):
        gs=[r['normalized_gain'] for r in pairs if r['normalized_gain'] is not None]
        summary['normalized_gain']={'mean_individual_ratios':avg(gs),'eligible_n':len(gs),'ceiling_excluded_n':n-len(gs),'ratio_of_matched_means':None if not n or mx==hi else md/(hi-mx)}
    inference={'status':'not_requested'}
    if p.get('inference',False):
        confidence=num(p.get('confidence',.95),'confidence')
        if not 0<confidence<1:raise ValueError('confidence must be between zero and one')
        if n<2 or not sdiff:inference={'status':'unavailable','reason':'At least two pairs and nonzero change variance are required by this calculator.'}
        else:
            try:
                import scipy
                from scipy.stats import t
            except ImportError:inference={'status':'unavailable','reason':'Optional SciPy dependency is not installed.'}
            else:
                se=sdiff/math.sqrt(n);stat=md/se;crit=float(t.ppf((1+confidence)/2,n-1))
                inference={'status':'computed','method':'paired t on post-minus-pre differences','confidence':confidence,'df':n-1,'t':stat,'two_sided_p':float(2*t.sf(abs(stat),n-1)),'mean_change_ci':[md-crit*se,md+crit*se],'runtime':'scipy '+scipy.__version__,'assumptions':'Independent learners and appropriate difference distribution; sampling, clustering and causal interpretation require external design review.'}
    return {'analysis_scale':scale,'units':'percentage points' if scale=='percentage' else 'raw score units','policy':p,'audit':{'union_n':len(set(pre)|set(post)),'pre_observed_n':sum(r['status']=='observed' for r in pre.values()),'post_observed_n':sum(r['status']=='observed' for r in post.values()),'matched_n':n,'excluded_n':len(excluded)},'pairs':pairs,'excluded':excluded,'summary':summary,'inference':inference,'limits':['Complete-case descriptive changes do not establish intervention causality.','Standardized-change denominators differ; null denotes undefined, not zero.','Comparability is user-supplied and cannot be validated from numeric scores alone.']}

def main():
    a=argparse.ArgumentParser();a.add_argument('input');a.add_argument('output');args=a.parse_args()
    try:
        with open(args.input) as f:data=json.load(f)
        result=analyze(data)
        with open(args.output,'w') as f:json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
    except (ValueError,KeyError,TypeError,AssertionError) as e:print('Input error: '+str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
