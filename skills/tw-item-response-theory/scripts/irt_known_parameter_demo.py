#!/usr/bin/env python3
"""SYNTHETIC known-parameter dichotomous IRT curves; never a calibration tool."""
import argparse
import hashlib
import json
import math
import platform
from pathlib import Path

VERSION='1.0.0'

def curve(theta,a,b,c=0.0,d=1.0):
    z=d*a*(theta-b)
    if z>=0:
        ez=math.exp(-z)
        s=1/(1+ez)
    else:
        ez=math.exp(z)
        s=ez/(1+ez)
    p=c+(1-c)*s
    derivative=(1-c)*d*a*s*(1-s)
    information=derivative**2/(p*(1-p)) if 0<p<1 else 0.0
    return p,information

def demo(path):
    path=Path(path)
    cfg=json.loads(path.read_text())
    if cfg.get('status')!='synthetic_known_parameters_not_estimated':
        raise ValueError('status must label these as synthetic known parameters, not estimates')
    theta=cfg.get('theta')
    items=cfg.get('items')
    d=cfg.get('logistic_D',1.0)
    def finite_number(x):
        return not isinstance(x,bool) and isinstance(x,(int,float)) and math.isfinite(x)
    if not finite_number(d) or d<=0 or not isinstance(theta,list) or not theta or any(not finite_number(x) for x in theta) or not isinstance(items,list) or not items:
        raise ValueError('provide finite theta grid, positive logistic_D, and items')
    seen=set()
    for item in items:
        if not isinstance(item,dict):
            raise ValueError('items must be objects')
        name=item.get('id')
        if not isinstance(name,str) or not name or name in seen:
            raise ValueError('item IDs must be distinct nonempty strings')
        seen.add(name)
        a,b,c=item.get('a'),item.get('b'),item.get('c',0.0)
        if not all(finite_number(x) for x in (a,b,c)) or a<=0 or not 0<=c<1:
            raise ValueError('a must be positive, b finite, c in [0,1)')
    rows=[]
    for t in theta:
        results=[]
        for item in items:
            p,info=curve(t,item['a'],item['b'],item.get('c',0),d)
            results.append({'item':item['id'],'probability':p,'information':info})
        total=sum(x['information'] for x in results)
        rows.append({'theta':t,'items':results,'test_information_assuming_local_independence':total,'asymptotic_inverse_sqrt_information':1/math.sqrt(total) if total>0 else None})
    return {'status':'SYNTHETIC DEMONSTRATION; parameters supplied, not estimated; no student scoring or calibration',
            'version':VERSION,'python':platform.python_version(),'config_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'parameterization':'P(theta)=c+(1-c)*logistic(D*a*(theta-b))','config':cfg,'rows':rows,
            'limits':['Dichotomous known-parameter curves only; no fit, estimation, DIF or linking.','Summed information assumes local independence and a common scale.','Inverse-square-root information is an asymptotic illustration, not an estimated learner interval; it ignores parameter uncertainty.','Floating-point saturation at extreme theta yields zero information.']}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',required=True)
    p.add_argument('--output',required=True)
    args=p.parse_args()
    if Path(args.output).resolve()==Path(args.config).resolve():
        p.error('output must not overwrite configuration')
    try:
        result=demo(args.config)
    except (ValueError,TypeError,KeyError,OSError) as e:
        p.error(str(e))
    Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print('Wrote synthetic known-parameter demonstration; no model was calibrated.')

if __name__=='__main__':
    main()
