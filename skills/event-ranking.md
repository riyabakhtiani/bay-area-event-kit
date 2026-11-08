---
name: event-ranking
description: Rank nightly events, check read-only availability/budget/future opportunities, and persist explicit accept/decline/feedback without booking.
---
# Event ranking (pointer to the kit)

1. Make sure the kit is current: `git -C /workspace/event-kit pull --ff-only` (or clone `https://github.com/riyabakhtiani/bay-area-event-kit.git` into `/workspace/event-kit`). If both fail, use the copy at `<events folder>/workflow/event-ranking.md`.
2. Read and follow `/workspace/event-kit/docs/ranking.md` in full: availability (read-only calendars + chat blackouts/on-call), budget and monthly cap, annual opportunity cost, scoring, history/learning, verification and the message format.
3. Missing upstream stages: run them from `/workspace/event-kit/agents/*.md` per `/workspace/event-kit/docs/team-setup.md`.
4. Write history/events only via `/workspace/event-kit/scripts/jsonstore.py`. Save tonight's pick ids as `top_ids` in setup-state, then refresh the tracker Page (event-tracker-page skill).

Pick format (one line each, max 3, never pad): `1. [Event name](direct URL) · day/date/time [zone] · venue/neighborhood · best verified price (deal/source) — one sentence why it fits.` Then an Accept/Decline widget ("Intent only; you book yourself"). Nothing strong: one line "Nothing strong tonight." plus at most one truly worthwhile named alternative with a link, no widget.

Owner can say anytime: "I'm busy/traveling <dates>" or "on-call <dates>" (save to availability.json via jsonstore), "change my budget/interests" (update budget.json/preferences.json after confirming).

NEVER book, RSVP, register, buy, subscribe or message anyone, even on acceptance. NEVER write calendars.
