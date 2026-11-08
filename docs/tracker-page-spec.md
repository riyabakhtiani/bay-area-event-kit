# Tracker Page spec (reference only)

The exact implementation is `/workspace/event-kit/page/tracker.canvas.tsx`; never redesign it. This spec documents intent and QA expectations.

Read canvas skill BEFORE WriteCanvas; discover runtime/imports/theme/tools. Create owner-specific Page after opt-in; save ID in setup-state, refresh same Page. No exporter URL/private calendars. Filters/drawers temporary; no fake saved Accept/Save/Rate, backend/storage promises. Footer/help: decisions/feedback in chat.

## Data
Validate/derive/embed safe JSON (no eval/runtime filesystem). Empty data→empty UI, never examples. Payload: preferences{bot_name,city,currency,timezone}, updated_at, events[], annual[], top_ids(actual latest recommendations,max3), history(latest decisions/feedback), budget{start,end_exclusive,target,actual_spent,unpaid_commitments,remaining,per_event_max,monthly_count,monthly_cap,free_counts,days_left}. Derive budget exactly per event-ranking, no hardcoded values. Carry null through all price/baseline calculations. Use canonical pricing.best_price/best_source/best_url/confidence/conditions/fees; ineligible member rates only in details. Only safe availability summaries, never calendar titles/locations.

## Components/layout
`App → Header + TabNav + ActivePanel + Footer + DetailDrawer/HelpDialog`.
State: tab/search/category/cost/dayFilter/freeOnly/browseAll/visibleMonth/selectedDate/selectedEventOrAnnual. Memoize filters/occurrences/annual groups. Dates/today/counts in owner zone; no fixed dates/counts/UTC shifts.
Frame height calc(100dvh−host padding), flex column, min-height:0, overflow:hidden. Header/nav fixed, only active panel scrolls. No five stacked sections/long webpage. Cards desktop3/tablet2/mobile1, 16px radii, 16–24px spacing, theme/light-dark/reduced-motion. Authentic imagery or abstract icons, no fake photos; detail in drawer.

## Exact tabs
**Picks**: “Next up” 0–3 actual qualified picks, not auto-top3. Explore toggle for verified candidates, dynamic count. Visual card: date chip, category art/icon, name, local date/time, venue/neighborhood, short hook, honest best-price chip, availability badge. Click drawer: why-fit, selected session vs run, source/check date, eligible deal/fees/conditions, verified logistics/access, direct event/deal links (“View event/price”, not “Book”). Nothing strong/no data empty states.
**Calendar**: real 7-column month, correct offsets/weeks, prev/next/Today. Only verified session dots/counts, no invented daily runs. Date click→desktop side panel/mobile below-grid list→details. Free-window shading labeled “usual preferences, not confirmed availability”; safe blackout/on-call/unknown overlays with labels, no private details or color-only meaning.
**Save for later**: horizontal annual timeline with snap month columns plus recurring/year-round. Confirmed dates vs “typically [month]”; approximate/published/historical/planning price labels, booking windows, compelling free/splurge badges. Search/free filter; full details in drawer. Watchlist view, not pretend persistent Save button.
**History**: real latest accepted/declined/attended/cancelled actions/feedback, status filter. Attendance never inferred from date; empty state and “Feedback in chat” help.
**Budget**: SVG actual/target ring, separate unpaid commitments/remaining, year/days-left/per-event ceiling. Unknown baseline=dashed ring/“Baseline needed”, not0. Monthly accepted count/cap meter and free-count rule, month by event date. Unlimited cap explicit; clamp drawing ratios but show overspend text; zero target no divide-by-zero. “Update baseline in chat”, no unsaved form controls.

Picks/Calendar filter pills: category from real dataset, cost incl Unknown, weekday evenings/weekend, Free, name/venue search, Reset, selected count and pressed state. Free requires verified0. Filters don't change preferences. Header city/bot/freshness/time; footer snapshot+zone/recommend-only/decisions-in-chat, not live-sync.

## QA/accessibility
Tablist arrows/Home/End, labeled panel/aria-selected/tabIndex. Mobile bottom five-icon labeled nav, safe-area inset, ≥44px targets. Drawer overlay/close/Escape, initial focus/trap/restore, dialog label, internal scrolling. Semantic buttons/links, contrast/focus, no nested interactive elements. Test keyboard/mobile, empty data, unknown costs/baseline, zero/overspent budget, long names, DST/multi-day/month rollover; counts/links match actual payload. Report only after successful Page write.
