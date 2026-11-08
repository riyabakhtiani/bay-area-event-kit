# Nightly picks routine (main bot)

Schedule: daily ~9pm in the owner IANA zone, all seven days. Save with UpdateRoutine; reuse an existing job instead of duplicating.

The "Saved prompt" section is the routine prompt; paste it as-is after resolving the folder path and zone.

Load routines; discover UpdateRoutine. Get/reuse matching imported job, not a duplicate. Save around9pm in owner IANA zone, all seven days for personal-life/weekend plans; use current timestamp-based minute/timing policy and report actual time. Resolve shared folder, store returned ID, verify save before activation claim. No email trigger here.

## Saved prompt
Load and follow **event-ranking** in full (source: `/workspace/event-kit/docs/ranking.md`; `git -C /workspace/event-kit pull --ff-only` first). Read preferences/shared README/freshness; if solo mode or missed stages, execute missing Scout→Curator→Bargain jobs from `/workspace/event-kit/agents/*.md`. Reverify finalists; check read-only calendars/chat blackouts, budget/cap and annual alternatives. Send0–3 strong picks and honest accept/decline widget per ranking skill. Intent never books. Handle due feedback once, no inferred attendance/spending. Merge safely and refresh the existing tracker via **event-tracker-page** (`/workspace/event-kit/scripts/build_page_payload.py` + the same Page id) if enabled. Never book, RSVP, register, buy, subscribe, contact organizers or write calendars. Unconfigured setup: report once/pause, don't fabricate readiness. Repeated auth failure: follow routines guidance.

Deliver to the owner in this Grok Bot chat. Nothing qualifies: event-ranking's one-line fallback, worthwhile alternative only, no decision widget.
