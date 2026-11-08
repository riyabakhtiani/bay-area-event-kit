#!/usr/bin/env python3
"""Generate the event-kit JSON Schemas (Draft 2020-12).

Usage: python3 scripts/generate_schemas.py --dir /workspace/events
Creates ONLY missing files; existing data is never touched.
"""
import json, pathlib, argparse
ap=argparse.ArgumentParser(description="Write the five JSON Schemas (and empty events/annual/history files) into a data folder. Never overwrites existing files.")
ap.add_argument("--dir",default="/workspace/events",help="data folder (default /workspace/events)")
ap.add_argument("--schemas-only",action="store_true",help="write only *.schema.json files")
args=ap.parse_args()
p=pathlib.Path(args.dir); p.mkdir(parents=True,exist_ok=True)
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
if args.schemas_only: raise SystemExit(0)
for name,data in {'events':[],'annual_calendar':[],
 'history':{'entries':[],'transactions':[],'commitments':[]}}.items():
    f=p/(name+'.json')
    if not f.exists(): f.write_text(json.dumps(data,indent=2)+'\n')
# Create budget.json and availability.json from the answers using the contracts above.
# Validate with jsonschema.Draft202012Validator and FormatChecker before any replace.
