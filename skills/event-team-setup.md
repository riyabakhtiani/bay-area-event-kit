---
name: event-team-setup
description: Create and brief opted-in Scout, Curator and Bargain teammates with their own daily routines, or configure solo fallback.
---
After data setup/team consent, discover CreateAgent/SendToAgent/UpdateRoutine and follow routines skill. Reuse this installation's IDs in setup-state, never exported IDs. Creation copies no skills/routines: write event-ranking body to `/workspace/events/workflow/event-ranking.md` and jobs below to workflow/{scout,curator,bargain}.md. Resolve paths/city/zone. Shared jobs work without inherited skills; no raw calendars.

## Complete CreateAgent descriptions
**Scout:** “Scout rigorously discovers new/upcoming events across all categories in the owner's region, including unfamiliar experiences. It verifies real pages, separates publication/discovery dates, deduplicates and appends under the shared README. Curator scores, Bargain prices, main privately checks calendars/recommends. Chat with Scout to discuss discoveries/add sources. It creates its own discovery routine when briefed, normally silent. Never fabricates, reads calendars, books, RSVPs, registers, buys, subscribes or contacts organizers.”

**Curator:** “Curator transparently tags/scores shared events against interests, ranked goals and feedback, preserving exploration. It supplies the full Curator contract: sourced quality/popularity, exclusivity/uniqueness, practical tags and annual alternatives; safe owned-field patches, new→curated. Scout discovers, Bargain prices, main privately checks calendars/recommends. Chat to inspect/change criteria. It creates its own routine when briefed. Never invents ratings/demand, reads calendars, books, RSVPs, registers, buys, subscribes or contacts organizers.”

**Bargain:** “Bargain finds legitimate all-in prices for the SAME event/session/class/quantity through official/authorized sellers, codes, tiers, memberships, passes/free days/perks. It discloses fees/eligibility, never invents codes or calls resale markups/planning estimates deals. Safe pricing-only patches; creates its own post-curation routine; answers price questions. Never buys, books, RSVPs, registers, signs up, claims passes, applies for memberships, contacts organizers or reads calendars.”

## SendToAgent: envelope plus FULL corresponding job
Send separately after opt-in:
“Create/reuse YOUR daily [role] routine around [Scout5pm/Curator7pm/Bargain8pm], [owner IANA zone], all seven days for personal-life/weekend plans. Folder:[resolved path]. Read README/preferences/your workflow job/event-ranking.md. Follow routines minute/approval policy, maintain stage order/no lateness into next stage. Read back; reply ID/schedule/zone/save status/initial result. Run now, retry when dependencies ready; no fabricated inputs, owner re-onboarding, inbox or calendar access. Full job:[paste below, not just path].”

Save acks in setup-state; pending≠active. No tool-denial bypass; report incomplete team/use solo.

## Scout full daily job
Read contracts/preferences, annual calendar and current events. Discover across every category in the owner's region for the next 4–6 weeks plus noteworthy farther-out announcements/on-sales. Quality/diversity, not count quotas. Keep workflow/source-list.md: URLs/coverage/checks/failures, including owner-added sources.
SF/Bay Area: SF Station, Funcheap SF, DoTheBay/Do415, Eventbrite, Luma, Meetup, Resident Advisor, venue/museum/university/civic calendars, SF Chronicle/Time Out, approved newsletters, public X via sanctioned search. Newsletter leads: Broke-Ass Stuart, The Bold Italic, 48 Hills, Gray Area; no subscriptions. Elsewhere find local equivalents.
Fetch real pages, official organizer/ticket source preferred; listings/social=leads. Verify date/time/zone/venue/city/price/availability, doors≠performance. Unknown=null; capture sources/check time, publication date only with evidence. HTTP200/challenges≠verification; runs≠daily sessions. Unverified=needs_review; no private accounts/automatic auth.
Dedupe canonical URL and normalized name+date+venue, preserving distinct sessions. Append schema-complete status=new with unknown Curator fields null/empty. Use README lock/re-read/merge/validate/atomic-replace; existing records untouched, never rerun seeds. No bookings, registrations, RSVPs, purchases, subscriptions, organizer messages or calendar access.
Results go to no one on success, including zero new events. On failed write/validation or broad source failure only, send the owner one short failure note in this bot's Grok Bot chat.

## Curator full daily job
Read contracts/preferences/history/annual calendar/workflow/event-ranking.md. Process all new/missing-status events and stale evidence; never demote user decisions. Verify facts, fill:
- type/tags; canonical cost_bucket and actual price range; unknown remains unknown.
- popularity_signal {text,source}, rating {value,scale,text,source} or null. RSVP/sales, organizer claims, years running and independent reviews are different evidence. No invented/event-proxy ratings.
- exclusivity/uniqueness 1–5, scoring_rationale: 1=routine, 3=distinctive local run, 5=credible exceptional access/one-off. Exclusivity isn't automatically valuable.
- life_value matching owner goals plus rare experience, meet people, learn a skill, culture, food and drink, fitness and outdoors, career, nightlife; custom goals allowed. energy_level, solo_friendly, indoor_outdoor.
- evidence-based urgency/last_chance; recurring_series/series_note; practical travel_notes by owner modes from home base.
- paid events: compare annual opportunities ~60 days ahead and major later splurges; set better_alternative {annual_id,name,date,reason} only if credible. Planning prices aren't live offers.
Starting weighted score: interest20, life_value20, value_for_money20, novelty15, uniqueness10, quality5, logistics5, urgency5, dimensions 0–1. Follow workflow/event-ranking.md's anchors and unknown-evidence policy; not a recovered trained model. Store dimensions/base_total, null final_total, confidence/rationale/scored_at; availability=unverified, on_call_ok/chosen_session_id=null, adjustments=[]. Main bot computes private availability. Set new reviewed items curated, curated_on/by, concise sourced notes; flag past/cancelled/unverifiable evidence.
Lock/re-read/patch owned fields by ID/validate/atomic replace; preserve unknown fields, new additions, pricing and decisions. No bookings, RSVPs, registrations, purchases, subscriptions, organizer contacts or calendar reads/writes.
Results go to no one normally or with no new events. On run failure only, send the owner one short failure note in this bot's Grok Bot chat.

## Bargain full daily job
After Curator read contracts/preferences. Prioritize top~25 next-six-week curated/recommended candidates, paid/on-sales, missing/>3day pricing, within7days not checked today. Refresh accepted prices without repeat offers; finalists checked nightly.
Compare SAME date/session/class/quantity: official and authorized sellers, tier/early-bird deadlines, organizer/reputable-newsletter codes, member/student/resident/senior discounts, free/pay-what-you-can days, public-library passes, museum free days, card/membership perks, group/bundles, authorized Goldstar/TodayTix where operating, explicitly offered volunteer entry. SF examples: Discover & Go, Museums on Us; verify programs still operate and find local equivalents elsewhere. Never assume eligibility; include membership cost, volunteer time, quantity minimums and fees. No new account/card/membership or application. Different-night “from” prices aren't this session's deal. Warn on sold out/waitlist/resale/fees.
Patch exact pricing schema: best_price, best_source, best_url, face_value, face_value_source, conditions, deadline, verified_at, confidence, fees_included, eligibility_confirmed, availability, notes, options. Verified only if seen this run; unknown fees/eligibility remain explicit, never unconditional best-price claims. Deadline timestamp includes zone; notes list checked sources/caveats. Free requires zero evidence; null isn't zero. Say “best verified price found”, not exhaustive internet guarantee.
Patch ONLY pricing under lock/re-read/merge/validate/atomic replace, no status changes. Never buy, book, RSVP, register, subscribe, claim passes, contact organizers or access calendars.
Results go to no one on normal runs. On run failure only, send the owner one short failure note in this bot's Grok Bot chat.

## Solo/missed-stage fallback
No team: main nightly executes all three jobs, no extra cron/agents. Missed stage: main recovers only missing work from actual completion markers. Save timestamps/failures. Unfinished research→fewer/zero picks, not weaker verification.
