#!/usr/bin/env python3
"""Read-only scoped Learning Commons client. No third-party dependencies."""
import argparse, datetime as dt, json, os, re, sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, HTTPRedirectHandler, build_opener
from urllib.error import HTTPError, URLError
BASE = 'https://api.learningcommons.org/knowledge-graph/v0/'
UUID = r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
RESOURCES = re.compile(r'(standards-frameworks|academic-standards|courses|academic-standards/'+UUID+r'/(learning-components|prerequisites))\Z')
class ReadError(ValueError): pass
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ReadError('Redirect refused; verify official endpoint documentation.')
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def fetch(url, key):
    req = Request(url, headers={'x-api-key':key, 'Accept':'application/json'}, method='GET')
    try:
        with build_opener(NoRedirect()).open(req, timeout=25) as res:
            body=res.read(10_000_001)
            if len(body)>10_000_000: raise ReadError('Response exceeds 10 MB bound; narrow query.')
            return json.loads(body)
    except HTTPError as e: raise ReadError('HTTP '+str(e.code)+'; verify access or request parameters.') from None
    except (URLError, TimeoutError, json.JSONDecodeError): raise ReadError('Request failed or returned invalid JSON; no data verified.') from None

def api(resource, params=None, max_pages=3, key=None, transport=fetch):
    if not RESOURCES.fullmatch(resource): raise ReadError('Unsupported resource; use documented resource and returned UUID.')
    if not 1 <= max_pages <= 20: raise ReadError('max_pages must be 1..20')
    params=dict(params or {})
    if any(not re.fullmatch(r'[A-Za-z][A-Za-z0-9]*',k) or not isinstance(v,(str,int,float,bool)) for k,v in params.items()):
        raise ReadError('Parameters must be simple documented query fields.')
    if any(any(s in k.lower() for s in ('key','token','password','secret','authorization')) for k in params):
        raise ReadError('Credentials are not query parameters.')
    key=key or os.environ.get('Teacher_Workbench_LEARNING_COMMONS_API_KEY')
    if not key: raise ReadError('Learning Commons key is not configured in the approved runtime secret environment.')
    records=[]; pages=0; seen=set(); has_more=False; cursor=None
    for _ in range(max_pages):
        url=BASE+resource+('?' + urlencode(params) if params else '')
        payload=transport(url,key)
        if not isinstance(payload,dict) or not isinstance(payload.get('data'),list): raise ReadError('Unexpected response schema; no complete result can be claimed.')
        records.extend(payload['data']); pages+=1
        pagination=payload.get('pagination')
        if pagination is None:
            has_more=False; cursor=None; break
        if not isinstance(pagination,dict) or not isinstance(pagination.get('hasMore'),bool): raise ReadError('Unrecognized pagination metadata.')
        has_more=pagination['hasMore']; cursor=pagination.get('nextCursor')
        if not has_more: break
        if not isinstance(cursor,str) or not cursor or cursor in seen or cursor==params.get('cursor'): raise ReadError('Missing or repeated pagination cursor; do not claim complete coverage.')
        seen.add(cursor);params['cursor']=cursor
    return {'route':'rest','source':BASE+resource,'retrieved_at':now(),'pages_read':pages,'complete':not has_more,'next_cursor':cursor if has_more else None,'data':records}

def local(path, match, max_records=100, max_lines=100000):
    if not isinstance(match,dict) or not match: raise ReadError('Supply at least one exact-match field.')
    if not 1<=max_records<=10000 or not 1<=max_lines<=10000000: raise ReadError('Invalid local scan bounds.')
    data=[]; scanned=0; complete=True
    with Path(path).open(encoding='utf-8-sig') as f:
        for lineno,line in enumerate(f,1):
            if lineno>max_lines: complete=False;break
            scanned=lineno
            if not line.strip():continue
            try: record=json.loads(line)
            except json.JSONDecodeError: raise ReadError('Invalid JSON at line '+str(lineno)) from None
            if not isinstance(record,dict):raise ReadError('Expected a JSON object at line '+str(lineno))
            fields=record.get('properties',record)
            if not isinstance(fields,dict):raise ReadError('Invalid properties at line '+str(lineno))
            def matches(k,v):
                actual=fields.get(k,record.get(k))
                return v in actual if isinstance(actual,list) else actual==v
            if all(matches(k,v) for k,v in match.items()):
                if len(data)>=max_records:complete=False;break
                data.append({'line':lineno,'record':record})
    return {'route':'local_jsonl','source_file':Path(path).name,'retrieved_at':now(),'lines_scanned':scanned,'complete':complete,'match':match,'data':data,'note':'Exact-match file scan only; does not establish graph or dataset completeness.'}
def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='mode',required=True)
    a=sub.add_parser('api');a.add_argument('--resource',required=True);a.add_argument('--params',default='{}');a.add_argument('--max-pages',type=int,default=3);a.add_argument('--out',required=True)
    a=sub.add_parser('local');a.add_argument('--file',required=True);a.add_argument('--match',required=True);a.add_argument('--max-records',type=int,default=100);a.add_argument('--max-lines',type=int,default=100000);a.add_argument('--out',required=True)
    args=p.parse_args()
    try:
        result=api(args.resource,json.loads(args.params),args.max_pages) if args.mode=='api' else local(args.file,json.loads(args.match),args.max_records,args.max_lines)
        Path(args.out).write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n'); print(json.dumps({'status':'read','records':len(result['data']),'complete':result['complete']}))
    except (ValueError,OSError) as e: print(str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
