---
name: event-data-setup
description: Initialize shared event contracts and owner-specific files, preserving existing data; research the annual planning calendar.
---
Use `/workspace/events/` or setup's instance-specific folder. Shell creates ONLY missing files, never copies exporter data. Save onboarding in preferences.json: bot_name, city, region, home_base, timezone(IANA), currency(ISO), interests[], goals_ranked[], free_windows[{weekdays:[0..6],start,end}], company[], transport_modes[], max_travel_minutes, hard_limits[], calendar_enabled/scope[], newsletter_enabled, teammates_enabled, tracker_enabled, notification_time, all_days. Runtime handles only in setup-state.json; no secrets/raw calendars.

## Exact schemas
Run this Python3 generator with resolved folder (same code as kit `scripts/generate_schemas.py --dir <folder>`; shared-write helper: kit `scripts/jsonstore.py`). JSON Schema2020-12; extensions allowed, canonical keys only (no bargain/ranked/actual_spend aliases). Initialize budget/availability from answers afterward. Unknown=null, never fabricated zero. Validate using jsonschema Draft202012Validator + FormatChecker before replacement.

```python
import json, pathlib
p=pathlib.Path('/workspace/events'); p.mkdir(parents=True,exist_ok=True)
def obj(props,required=()):
    return dict(type='object',properties=props,required=list(required),additionalProperties=True)
def arr(t): return {'type':'array','items':t}
def en(*v): return {'enum':list(v)}
S={'type':'string'}; N={'type':'number','minimum':0}; B={'type':'boolean'}
def z(t): return {'anyOf':[t,{'type':'null'}]}
D={'type':'string','format':'date'}; TS={'type':'string','format':'date-time'}
T={'type':'string','pattern':r'^([01][0-9]|2[0-3]):[0-5][0-9]$'}
URL={'type':'string','format':'uri'}
Q={'type':'integer','minimum':1,'maximum':5}
EVID=obj({'text':S,'source':URL},['text','source'])
RATING=obj({'value':{'type':'number'},'scale':{'type':'number','exclusiveMinimum':0},'text':z(S),'source':URL},['value','scale','source'])
SESSION=obj({'id':S,'date':D,'time':T,'end_time':z(T),'end_date':z(D),'timezone':S,'source':URL},'id date time end_time timezone source'.split())
PRICING=obj({
 'best_price':z(N),'best_source':z(S),'best_url':z(URL),
 'face_value':z(N),'face_value_source':z(URL),'conditions':z(S),
 'deadline':z(TS),'verified_at':TS,'confidence':en('verified','unverified'),
 'fees_included':z(B),'eligibility_confirmed':z(B),
 'availability':en('available','sold_out','waitlist','unknown'),
 'notes':S,'options':arr(obj({'label':S,'price':z(N),'url':URL,
 'conditions':z(S),'verified':B},'label price url conditions verified'.split()))
},'best_price best_source best_url face_value conditions deadline verified_at confidence fees_included eligibility_confirmed availability notes'.split())
DIMS='interest life_value value_for_money novelty uniqueness quality logistics urgency'.split()
SCORES=obj({'dimensions':obj({k:z({'type':'number','minimum':0,'maximum':1}) for k in DIMS},DIMS),
 'base_total':z({'type':'number','minimum':0,'maximum':100}),
 'final_total':z({'type':'number','minimum':0,'maximum':100}),
 'confidence':en('low','medium','high'),'rationale':S,'scored_at':TS,
 'availability':en('fits','conflict','unverified','blackout','on_call'),
 'on_call_ok':z(B),'chosen_session_id':z(S),'adjustments':arr(S)},
 'dimensions base_total final_total confidence rationale scored_at availability on_call_ok chosen_session_id adjustments'.split())
EVENT=obj({
 'id':S,'name':S,'url':URL,'date':z(D),'time':z(T),'end_time':z(T),
 'timezone':S,'venue':z(S),'neighborhood':z(S),'city':z(S),
 'date_start':z(D),'date_end':z(D),'sessions':arr(SESSION),
 'price_min':z(N),'price_max':z(N),'currency':S,
 'cost_bucket':en('free','low','medium','high','premium','over_cap','unknown'),
 'type':z(S),'tags':arr(S),'popularity_signal':z(EVID),'rating':z(RATING),
 'exclusivity':z(Q),'uniqueness':z(Q),'life_value':arr(S),
 'energy_level':en('low','medium','high',None),'solo_friendly':z(B),
 'indoor_outdoor':en('indoor','outdoor','mixed',None),
 'booking_urgency':en('none','low','medium','high',None),'last_chance':z(B),
 'recurring_series':z(B),'series_note':z(S),'travel_notes':z(S),
 'scoring_rationale':z(S),
 'better_alternative':z(obj({'annual_id':S,'name':S,'date':z(D),'reason':S},'annual_id name date reason'.split())),
 'source':URL,'source_label':z(S),'source_urls':arr(URL),
 'discovered_on':D,'published_at':z(TS),'source_checked_at':z(TS),
 'verification_status':en('needs_review','verified','price_uncertain','unverifiable','past','cancelled'),
 'status':en('new','curated','recommended','accepted','declined','attended'),
 'curated_on':z(D),'curated_by':z(S),'notes':arr(S),
 'pricing':z(PRICING),'scores':z(SCORES)
},'id name url date time end_time timezone venue city price_min price_max currency cost_bucket type tags popularity_signal rating exclusivity uniqueness life_value energy_level solo_friendly indoor_outdoor booking_urgency last_chance recurring_series source discovered_on verification_status status notes'.split())
ENTRY=obj({'id':S,'event_id':S,'session_id':z(S),
 'status':en('recommended','accepted','declined','attended','cancelled','booked','refunded','feedback'),
 'date':TS,'event_date':z(D),'rating':z(Q),
 'worth_it':en('worth_it','mixed','not_worth_it',None),'more_like_this':z(B),
 'feedback_notes':z(S),'decline_reason':z(S),
 'recommendation_score':z({'type':'number','minimum':0,'maximum':100}),
 'explanation':z(S),'delivery_id':z(S)},'id event_id status date'.split())
TRANSACTION=obj({'id':S,'event_id':z(S),'session_id':z(S),'date':D,
 'amount':{'type':'number'},'currency':S,'kind':en('payment','refund'),
 'included_in_baseline':B,'notes':z(S)},'id event_id date amount currency kind included_in_baseline'.split())
COMMITMENT=obj({'event_id':S,'session_id':z(S),'event_date':D,'amount':z(N),
 'currency':S,'state':en('unpaid','paid','cancelled'),'notes':z(S)},'event_id event_date amount currency state'.split())
HISTORY=obj({'entries':arr(ENTRY),'transactions':arr(TRANSACTION),'commitments':arr(COMMITMENT)},['entries','transactions','commitments'])
ANNUAL=obj({'id':S,'name':S,'city':S,'category':S,'timing':S,
 'typical_months':arr({'type':'integer','minimum':1,'maximum':12}),
 'date_start':z(D),'date_end':z(D),'dates_confirmed':B,
 'typical_price_min':z(N),'typical_price_max':z(N),'currency':S,
 'price_basis':en('published','historical','planning_estimate','unknown'),
 'why_standout':S,'official_url':URL,'source_urls':arr(URL),
 'worth_splurge':B,'best_free':B,'booking_window':z(S),
 'on_sale_at':z(TS),'booking_deadline':z(TS),
 'verified_on':D,'verification_status':en('verified','typical_only','needs_review'),'notes':arr(S)
},'id name city category timing typical_months date_start date_end dates_confirmed typical_price_min typical_price_max currency price_basis why_standout official_url source_urls worth_splurge best_free booking_window verified_on verification_status notes'.split())
BUDGET=obj({'currency':S,'budget_year_start':z(D),'budget_year_end_exclusive':z(D),
 'annual_budget':z(N),'per_event_max':z(N),'baseline_spend':z(N),
 'baseline_as_of':z(D),'scope':S,'events_per_month_cap':z({'type':'integer','minimum':0}),
 'cap_counts_free_events':B,'allow_exceptional_cap_override':B,'reserve_amount':z(N),
 'cost_bucket_edges':arr(N),'notes':arr(S)},
 'currency budget_year_start budget_year_end_exclusive annual_budget per_event_max baseline_spend baseline_as_of scope events_per_month_cap cap_counts_free_events allow_exceptional_cap_override reserve_amount cost_bucket_edges notes'.split())
BLOCK=obj({'id':S,'start':TS,'end':TS,'kind':en('blackout','travel','sick','busy','on_call'),
 'source':en('chat','calendar'),'note':z(S)},'id start end kind source'.split())
AVAILABILITY=obj({'timezone':S,'blackouts':arr(BLOCK),'on_call':arr(BLOCK),
 'calendar_enabled':B,'calendar_scope':arr(S),'calendar_last_success_at':z(TS),
 'calendar_status':en('disabled','connected','unverified','error'),
 'meeting_buffer_minutes':{'type':'integer','minimum':0},
 'on_call_max_duration_minutes':{'type':'integer','minimum':0},
 'travel_return_confirmed':z(TS),'notes':arr(S)},
 'timezone blackouts on_call calendar_enabled calendar_scope calendar_last_success_at calendar_status meeting_buffer_minutes on_call_max_duration_minutes travel_return_confirmed notes'.split())
schemas={'events':arr(EVENT),'history':HISTORY,'annual_calendar':arr(ANNUAL),'budget':BUDGET,'availability':AVAILABILITY}
for name,schema in schemas.items():
    schema={'$schema':'https://json-schema.org/draft/2020-12/schema',**schema}
    f=p/(name+'.schema.json')
    if not f.exists(): f.write_text(json.dumps(schema,indent=2)+'\n')
for name,data in {'events':[],'annual_calendar':[],
 'history':{'entries':[],'transactions':[],'commitments':[]}}.items():
    f=p/(name+'.json')
    if not f.exists(): f.write_text(json.dumps(data,indent=2)+'\n')
# Create budget.json and availability.json from the answers using the contracts above.
# Validate with jsonschema.Draft202012Validator and FormatChecker before any replace.
```

## Initialization and README.md contract
Create budget.json from answers: currency, year start/next-anniversary exclusive end (handle leap day explicitly), annual/per-event budgets, baseline/as-of, scope, monthly cap/free counting, exceptional override=false unless approved, reserve=null unless approved. Availability: timezone, supplied chat intervals or [], chosen calendar scope/read-tested status, last_success=null until tested, 30min meeting buffer, 180min on-call max, return_confirmation=null. No fake events/history. Validate starts<ends, price min<=max, unique IDs, currencies, transaction signs. README.md is Markdown, not JSON: write these semantics, preferences field list, schema version and links to the five exact schemas above (which define every field):
- Scout appends; Curator patches tags/verification/scores; Bargain pricing only; main owns availability/final rank/history/budget/Page. Lifecycle new→curated→recommended→accepted/declined→attended; never demote user decisions on refresh. History is the audit trail, not proof of payment/attendance.
- date/time=concrete session, date_start/end=run, sessions=published occurrences only. End before start needs explicit next-day end_date. Dates/timestamps zone-aware; no invented daily sessions or shifted-year dates. discovered_on≠published_at. Rating includes scale/source; exclusivity/uniqueness are justified judgments. Unknown prices=null, verified free=0. USD bucket edges [25,75,150,300]: free0; low(0,25); medium[25,75); high[75,150); premium[150,300]; over_cap>300. For other currencies configure local edges with owner. Per-event ceiling independent.
- Shared writes: prepare owned-field patches outside lock. Acquire fcntl.flock on .write.lock; re-read, dedupe, patch by ID preserving EVERY other field/record, backup, validate, unique same-folder temp+os.replace, release. Never hold lock across web calls; re-read alone is insufficient concurrency protection. Conflicting same-field edits need re-evaluation. Malformed JSON: stop, never truncate. README section edits same protocol. UUIDs or under-lock sequence IDs; dedupe canonical URL and normalized name/date/venue, preserving distinct sessions.
- Spending uses unique transactions: payments positive/refunds negative; exclude included_in_baseline. Commitments reserve only unpaid amounts, not paid twice. Accept=intent only; unknown unpaid amount≠zero. Monthly counts dedupe decision changes per outing/session. Silence≠decline; attendance requires explicit feedback. Chat availability survives calendar refresh; source-specific cache replacement never erases chat intervals. No raw calendar titles stored/shared.

## Annual research
Rolling year in owner's city, broad seasonal coverage (~25–50 meaningful entries if evidence permits), rare splurges AND free gems, not a quota. Official festival/museum/sports/university/civic calendars: typical months, standout reason, single-session price range+basis, actual future edition dates, booking/on-sale window and source-check date. Unpublished: dates_confirmed=false, exact dates=null, “typically [month]”. Historical/planning prices aren't live quotes; unknown booking window=null, monitor rather than invent lead time.
SF/Bay Area research examples only: Sketchfest, FOG, SFFILM, Noise Pop, Cherry Blossom, Carnaval, Stern Grove, Outside Lands, Hardly Strictly Bluegrass, Litquake, ArtSpan, Maker Faire, West Coast Craft, Renegade, DanceFest, museum nights/sports schedules. Elsewhere find equivalents. Refresh stale entries before paid-pick comparisons/new editions. HTTP200 isn't evidence of usable content. No old owner dates/prices copied.
