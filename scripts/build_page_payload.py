#!/usr/bin/env python3
"""Build the tracker Page data payload from an events folder and splice it into the Page source.

    python3 scripts/build_page_payload.py --data-dir /workspace/events \
        --page page/tracker.canvas.tsx --out /workspace/events/tracker.canvas.tsx

Reads (all optional; missing files mean empty data):
  events.json, annual_calendar.json, history.json, budget.json,
  preferences.json, setup-state.json (key "top_ids": latest real picks)
Writes: the Page source with ONLY the text between `@@PAGE_DATA_START@@` and
`@@PAGE_DATA_END@@` replaced by `const PAGE_DATA:PageData = {...};`.
Then pass --out to WriteCanvas (or EditCanvas on the existing Page).

Privacy: only safe summaries go into the Page. Calendar titles/locations,
emails, notes fields and raw availability are never copied.
Use --payload-only to print the JSON payload instead of writing a Page.
"""
import argparse, datetime, json, pathlib, re, sys

START, END = "@@PAGE_DATA_START@@", "@@PAGE_DATA_END@@"
VISIBLE = {"curated", "recommended", "accepted", "declined", "attended"}
HIDDEN_VERIFICATION = {"past", "cancelled", "unverifiable"}

# Page categories (drive the card art via keyword match in Glyph). First match wins.
CATEGORY_RULES = [
    ("Film & ideas", r"film|movie|cinema|screening|talk|lecture|author|book|reading|ideas|panel|ted"),
    ("Tech", r"tech|ai\b|startup|hackathon|science|maker|engineering|developer"),
    ("Music", r"music|concert|jazz|dj|band|orchestra|symphony|opera|reggae|bluegrass|club"),
    ("Performance", r"theat|comedy|dance|performance|circus|improv|cabaret|show"),
    ("Art", r"art|design|craft|gallery|museum|exhibit|sketch|fashion|photo"),
    ("Culture", r"culture|festival|heritage|community|parade|holiday|fair"),
    ("Food & drink", r"food|drink|coffee|wine|beer|tasting|dinner|market|culinary"),
    ("Outdoors", r"outdoor|hike|walk|run|fitness|sport|yoga|bike|skate|park|nature|game"),
]


def load(folder, name, default):
    p = folder / name
    if not p.exists():
        return default
    return json.loads(p.read_text())


def category(ev):
    hay = " ".join([ev.get("type") or "", " ".join(ev.get("tags") or []), ev.get("name") or ""]).lower()
    for label, pat in CATEGORY_RULES:
        if re.search(pat, hay):
            return label
    t = (ev.get("type") or "Other").split("/")[0].strip()
    return t[:1].upper() + t[1:] if t else "Other"


def short_text(ev):
    if ev.get("page_short"):
        return ev["page_short"]
    src = ev.get("scoring_rationale") or (ev.get("scores") or {}).get("rationale") or ev.get("type") or ""
    first = re.split(r"(?<=[.;:!?])\s", src, maxsplit=1)[0].rstrip(".;:")
    if len(first) > 70:
        first = first[:70].rsplit(" ", 1)[0] + "…"
    return first


def fmt_day(d):
    x = datetime.date.fromisoformat(d)
    return f"{x:%b} {x.day}, {x.year}"


AVAIL_LABEL = {"fits": "Fits your free time", "conflict": "Calendar conflict", "unverified": "Availability unverified",
               "blackout": "Blackout date", "on_call": "On-call day"}


def page_event(ev):
    pr = ev.get("pricing") or None
    sessions = [{"date": s["date"], "time": s["time"]} for s in (ev.get("sessions") or []) if s.get("date") and s.get("time")]
    date = ev.get("date") or (sessions[0]["date"] if sessions else ev.get("date_start"))
    time = ev.get("time") or (sessions[0]["time"] if sessions else "")
    out = {
        "id": ev["id"], "name": ev["name"], "date": date, "time": time or "",
        "venue": ", ".join(x for x in [ev.get("venue"), ev.get("neighborhood")] if x) or (ev.get("city") or ""),
        "category": ev.get("page_category") or category(ev),
        "lo": ev.get("price_min"), "hi": ev.get("price_max"),
        "url": ev.get("url") or ev.get("source"),
        "short": short_text(ev),
        "why": ev.get("page_why") or ev.get("scoring_rationale") or (ev.get("scores") or {}).get("rationale") or "",
    }
    if ev.get("end_time"):
        out["end"] = ev["end_time"]
    if len(sessions) > 1:
        out["sessions"] = sessions
    ds, de = ev.get("date_start"), ev.get("date_end")
    if ds and de and ds != de:
        out["run"] = f"{fmt_day(ds)}–{fmt_day(de)}"
    if pr:
        out["pricing"] = {k: pr.get(k) for k in ["best_price", "best_source", "best_url", "face_value", "conditions",
                                                 "deadline", "verified_at", "confidence", "notes", "availability"]}
    sc = ev.get("scores") or {}
    if sc.get("availability") in AVAIL_LABEL:
        out["availability"] = AVAIL_LABEL[sc["availability"]]
    if sc.get("on_call_ok") is not None:
        out["on_call_ok"] = bool(sc["on_call_ok"])
    return out


def price_basis(a):
    b = (a.get("price_basis") or "").lower()
    for k in ["published", "historical", "planning_estimate"]:
        if b.startswith(k.split("_")[0]):
            return k
    return "unknown" if not b else ("planning_estimate" if "planning" in b or "estimate" in b else "unknown")


def page_annual(a):
    return {
        "id": a.get("id") or a["name"], "name": a["name"], "date_start": a.get("date_start"),
        "timing": a.get("timing") or "", "category": a.get("category") or "",
        "price_min": a.get("typical_price_min"), "price_max": a.get("typical_price_max"),
        "price_basis": price_basis(a), "worth_splurge": bool(a.get("worth_splurge")),
        "best_free": bool(a.get("best_free")), "url": a.get("official_url") or (a.get("source_urls") or [""])[0],
        "dates_confirmed": bool(a.get("dates_confirmed")), "note": None,
    }


def page_budget(b, currency):
    end = b.get("budget_year_end")
    if not end and b.get("budget_year_end_exclusive"):
        end = (datetime.date.fromisoformat(b["budget_year_end_exclusive"]) - datetime.timedelta(days=1)).isoformat()
    g = lambda *ks: next((b[k] for k in ks if k in b), None)
    return {
        "budget_year_start": b.get("budget_year_start"), "budget_year_end": end,
        "currency": b.get("currency") or currency,
        "annual_budget": g("annual_budget", "annual_budget_usd"),
        "per_event_max": g("per_event_max", "per_event_max_usd"),
        "baseline_spend": g("baseline_spend", "baseline_spend_usd"),
        "events_per_month_cap": b.get("events_per_month_cap"),
        "cap_counts_free_events": b.get("cap_counts_free_events"),
        "scope": b.get("scope"),
    }


def history_entries(h, transactions):
    spend = {}
    for t in transactions or []:
        if t.get("event_id") and not t.get("included_in_baseline"):
            spend[t["event_id"]] = spend.get(t["event_id"], 0) + (t.get("amount") or 0)
    out = []
    for e in h.get("entries", []):
        if e.get("status") == "feedback":
            continue
        out.append({"event_id": e["event_id"], "status": e["status"], "date": e["date"],
                    "event_date": e.get("event_date"), "actual_spend": spend.get(e["event_id"], e.get("actual_spend")),
                    "worth_it": e.get("worth_it"), "decline_reason": e.get("decline_reason"),
                    "feedback_notes": e.get("feedback_notes")})
    return out


def nightly_label(t):
    if not t:
        return None
    try:
        h, m = map(int, t.split(":")[:2])
        return f"{h % 12 or 12}{'' if m == 0 else f':{m:02d}'}{'am' if h < 12 else 'pm'}"
    except Exception:
        return str(t)


def tz_label(tz):
    return {"America/Los_Angeles": "PT", "America/Denver": "MT", "America/Phoenix": "MST", "America/Chicago": "CT",
            "America/New_York": "ET", "Europe/London": "UK", "Asia/Kolkata": "IST"}.get(tz, tz.split("/")[-1].replace("_", " "))


def build(folder, top_ids=None, as_of=None):
    prefs = load(folder, "preferences.json", {})
    state = load(folder, "setup-state.json", {})
    tz = prefs.get("timezone") or "America/Los_Angeles"
    currency = prefs.get("currency") or "USD"
    if not as_of:
        try:
            from zoneinfo import ZoneInfo
            as_of = datetime.datetime.now(ZoneInfo(tz)).date().isoformat()
        except Exception:
            as_of = datetime.date.today().isoformat()
    events = load(folder, "events.json", [])
    visible = [e for e in events if e.get("status") in VISIBLE and e.get("verification_status") not in HIDDEN_VERIFICATION
               and ((e.get("date_end") or e.get("date") or "") >= as_of or any(s.get("date", "") >= as_of for s in e.get("sessions") or []))]
    visible.sort(key=lambda e: (e.get("date") or "", e.get("time") or ""))
    hist = load(folder, "history.json", {"entries": [], "transactions": []})
    if top_ids is None:
        top_ids = state.get("top_ids")
    if top_ids is None:  # latest delivered recommendation batch
        recs = [e for e in hist.get("entries", []) if e.get("status") == "recommended"]
        if recs:
            last = max(recs, key=lambda e: e["date"])
            top_ids = [e["event_id"] for e in recs if e.get("delivery_id") == last.get("delivery_id")] if last.get("delivery_id") else [last["event_id"]]
    ids = {e["id"] for e in visible}
    payload = {
        "preferences": {
            "bot_name": prefs.get("bot_name"),
            "page_eyebrow": prefs.get("page_eyebrow") or prefs.get("region") or prefs.get("city"),
            "city": prefs.get("city"), "timezone": tz, "tz_label": tz_label(tz), "currency": currency,
            "nightly_label": nightly_label(prefs.get("notification_time")),
            "free_windows_label": prefs.get("free_windows_label"),
        },
        "as_of": as_of,
        "events": [page_event(e) for e in visible],
        "annual": [page_annual(a) for a in load(folder, "annual_calendar.json", [])],
        "top_ids": [i for i in (top_ids or []) if i in ids][:3],
        "history": {"entries": history_entries(hist, hist.get("transactions"))},
        "budget": page_budget(load(folder, "budget.json", {}), currency),
    }
    return payload


def splice(page_src, payload):
    lines = page_src.split("\n")
    s = next(i for i, l in enumerate(lines) if l.lstrip().startswith("// " + START))
    e = next(i for i, l in enumerate(lines) if l.lstrip().startswith("// " + END))
    if e <= s:
        raise SystemExit("markers out of order")
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    return "\n".join(lines[:s + 1] + [f"const PAGE_DATA:PageData = {blob};"] + lines[e:])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--page", default=str(pathlib.Path(__file__).resolve().parent.parent / "page" / "tracker.canvas.tsx"))
    ap.add_argument("--out", help="output .tsx path (default: print to stdout)")
    ap.add_argument("--top-ids", help="comma-separated ids of tonight's real picks (max 3)")
    ap.add_argument("--as-of", help="YYYY-MM-DD snapshot date (default: today in owner zone)")
    ap.add_argument("--payload-only", action="store_true")
    a = ap.parse_args()
    top = [x for x in a.top_ids.split(",") if x] if a.top_ids else None
    payload = build(pathlib.Path(a.data_dir), top, a.as_of)
    if a.payload_only:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    out = splice(pathlib.Path(a.page).read_text(), payload)
    if a.out:
        pathlib.Path(a.out).write_text(out)
        print(f"wrote {a.out}: {len(payload['events'])} events, {len(payload['annual'])} annual, "
              f"{len(payload['top_ids'])} top picks, {len(payload['history']['entries'])} history entries, {len(out)} bytes",
              file=sys.stderr)
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
