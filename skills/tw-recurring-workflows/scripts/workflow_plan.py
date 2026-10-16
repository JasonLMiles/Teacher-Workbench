#!/usr/bin/env python3
"""Validate a weekly workflow draft. Never activates a scheduler."""
import argparse,datetime as dt,json,sys
from pathlib import Path
from zoneinfo import ZoneInfo,ZoneInfoNotFoundError
DAYS=['MO','TU','WE','TH','FR','SA','SU']
def plan(b):
    for field in ('title','timezone','start_local','prompt','destination'):
        if not isinstance(b.get(field),str) or not b[field].strip():raise ValueError('Missing '+field)
    if '\n' in b['timezone'] or '\r' in b['timezone']:raise ValueError('Invalid timezone')
    try:z=ZoneInfo(b['timezone'])
    except (ZoneInfoNotFoundError,ValueError):raise ValueError('Use a valid IANA timezone') from None
    t=dt.datetime.fromisoformat(b['start_local'])
    if t.tzinfo is not None:raise ValueError('start_local must be a local datetime without offset')
    if t.microsecond:raise ValueError('Use whole-second precision')
    candidates=[]
    for fold in (0,1):
        a=t.replace(tzinfo=z,fold=fold)
        if a.astimezone(dt.timezone.utc).astimezone(z).replace(tzinfo=None)==t:candidates.append(a)
    if not candidates:raise ValueError('Start time does not exist because of DST')
    ambiguous=len({a.utcoffset() for a in candidates})>1
    if ambiguous:raise ValueError('Ambiguous DST start; choose an unambiguous local start time')
    days=b.get('weekdays')
    if not isinstance(days,list) or not days or any(d not in DAYS for d in days) or len(set(days))!=len(days):raise ValueError('Provide unique weekdays using MO..SU')
    if DAYS[t.weekday()] not in days:raise ValueError('Start date must match a requested weekday')
    if t.hour in (1,2):raise ValueError('Weekly 01:00–02:59 may be ambiguous or nonexistent at DST transitions; choose another time or use a reviewed native schedule')
    count=b.get('count');rrule='FREQ=WEEKLY;BYDAY='+','.join(sorted(days,key=DAYS.index))
    if count is not None:
        if isinstance(count,bool) or not isinstance(count,int) or not 1<=count<=520:raise ValueError('count must be 1..520')
        rrule+=';COUNT='+str(count)
    dates=b.get('excluded_dates',[])
    if not isinstance(dates,list):raise ValueError('excluded_dates must be a list')
    for day in dates:dt.date.fromisoformat(day)
    prompt=b['prompt'].strip()
    if dates:prompt+='\nOn these local dates, report a calendar skip and do not generate a new draft: '+', '.join(dates)+'.'
    if b.get('sources'):prompt+='\nRead these teacher-designated sources: '+json.dumps(b['sources'],ensure_ascii=False)+'.'
    prompt+='\nDestination: '+b['destination']+'.'
    event='BEGIN:VEVENT\nDTSTART;TZID='+b['timezone']+':'+t.strftime('%Y%m%dT%H%M%S')+'\nRRULE:'+rrule+'\nEND:VEVENT'
    return {'status':'draft_not_scheduled','requires_live_source_read_and_scheduler_result':True,'payload':{'title':b['title'],'prompt':prompt,'schedule':event,'default_timezone':b['timezone'],'timing_mode':'exact_schedule'},'exclusion_behavior':'Scheduled invocations still occur; run prompt checks exclusions.','first_occurrence_utc':candidates[0].astimezone(dt.timezone.utc).isoformat()}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('brief');p.add_argument('--out',required=True);a=p.parse_args()
    try:r=plan(json.loads(Path(a.brief).read_text()));Path(a.out).write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
    except (ValueError,OSError,TypeError) as e:print(str(e),file=sys.stderr);return 2
    return 0
if __name__=='__main__':sys.exit(main())
