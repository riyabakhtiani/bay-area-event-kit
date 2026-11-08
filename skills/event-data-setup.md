---
name: event-data-setup
description: Initialize shared event contracts and owner-specific files, preserving existing data; research the annual planning calendar.
---
# Event data setup (pointer to the kit)

1. Make sure the kit is current: `git -C /workspace/event-kit pull --ff-only` (or clone `https://github.com/riyabakhtiani/bay-area-event-kit.git` into `/workspace/event-kit`).
2. Read and follow `/workspace/event-kit/docs/data-setup.md` in full (field contracts, initialization, annual research).
3. Schemas: `python3 /workspace/event-kit/scripts/generate_schemas.py --dir <events folder>` (creates only missing files; copies also in `/workspace/event-kit/schemas/`).
4. All shared writes go through `/workspace/event-kit/scripts/jsonstore.py` (lock → re-read → merge by id → validate → atomic replace). Never rerun setup on live data; never overwrite or truncate.

Non-negotiable: never copy another owner's data; unknown = null, never an invented zero; no secrets or raw calendar contents in files.
