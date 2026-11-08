---
name: event-team-setup
description: Create and brief opted-in Scout, Curator and Bargain teammates with their own daily routines, or configure solo fallback.
---
# Event team setup (pointer to the kit)

1. Make sure the kit is current: `git -C /workspace/event-kit pull --ff-only` (or clone `https://github.com/riyabakhtiani/bay-area-event-kit.git` into `/workspace/event-kit`).
2. Read and follow `/workspace/event-kit/docs/team-setup.md` in full.
3. For each teammate use `/workspace/event-kit/agents/scout.md`, `curator.md`, `bargain.md` verbatim: CreateAgent with its "CreateAgent description", then SendToAgent with its briefing plus the FULL daily job pasted in (not just a path). Copy jobs to `<events folder>/workflow/` and `/workspace/event-kit/docs/ranking.md` to `<events folder>/workflow/event-ranking.md`.
4. Save this installation's agent ids and routine acknowledgements in `setup-state.json`; reuse them, never exported ids. Pending ≠ active.
5. Solo mode or a missed stage: the main bot runs the missing Scout → Curator → Bargain jobs itself (see the fallback section in team-setup.md).

Non-negotiable: only the main bot reads calendars. No teammate books, RSVPs, registers, buys, subscribes, claims passes or contacts organizers.
