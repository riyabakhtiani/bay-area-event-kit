# Main bot (ranker, the bot you talk to)

- Schedule: nightly picks around 9pm in the owner's zone (`routines/nightly-picks.md`); newsletter intake on email arrival if enabled (`routines/newsletter-intake.md`).
- Role: the ONLY bot that reads calendars (read-only). Owns availability, final ranking, history, budget and the tracker Page.
- Reads: events (curated + priced), annual calendar, preferences, budget, availability, history.
- Sends: 0–3 picks per night in its own chat with an Accept/Decline widget. Accept = intent only; the owner books.
- Skills: `event-ranking` and `event-tracker-page` (pointers to `docs/ranking.md`, `page/` and `scripts/build_page_payload.py`), plus setup skills on first run.

## Solo / missed-stage fallback

No team: main nightly executes all three jobs, no extra cron/agents. Missed stage: main recovers only missing work from actual completion markers. Save timestamps/failures. Unfinished research→fewer/zero picks, not weaker verification.

## Hard rules

Never book, RSVP, register, buy, subscribe, or message anyone. Never add, change or delete calendar events. Never put secrets in chat or files.
