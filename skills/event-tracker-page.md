---
name: event-tracker-page
description: Rebuild or refresh the visual five-tab tracker Page from real event data; decisions remain in chat.
---
# Event tracker Page (pointer to the kit)

The exact design is `/workspace/event-kit/page/tracker.canvas.tsx`. Never redesign it; only its data line changes.

1. Make sure the kit is current: `git -C /workspace/event-kit pull --ff-only` (or clone `https://github.com/riyabakhtiani/bay-area-event-kit.git` into `/workspace/event-kit`).
2. Build: `python3 /workspace/event-kit/scripts/build_page_payload.py --data-dir <events folder> --page /workspace/event-kit/page/tracker.canvas.tsx --out <events folder>/tracker.canvas.tsx [--top-ids id1,id2,id3]` (top ids default to `setup-state.json` `top_ids`). It replaces only the `const PAGE_DATA` line between `@@PAGE_DATA_START@@` and `@@PAGE_DATA_END@@`.
3. Optional check: `/workspace/event-kit/tests/render_test.sh <events folder>/tracker.canvas.tsx` (strict type-check + render of all five tabs; needs node).
4. Read the canvas skill, then WriteCanvas with the built file's full contents. First time: save the returned canvas id in `setup-state.json`. Later: overwrite the SAME Page (WriteCanvas with that id or EditCanvas), never a new one.
5. Reference/QA spec: `/workspace/event-kit/docs/tracker-page-spec.md`.

Rules: real data only (empty data → empty states, never examples); no calendar titles or private details on the Page; filters are temporary and decisions/feedback happen in chat. Report only after a successful Page write.
