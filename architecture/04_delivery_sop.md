# SOP: Delivery

## Purpose
Deliver the compiled study material via Google Calendar event and Gmail draft.

## Step 1 — Google Calendar Event
- Title: `🔬 Longevity Study — Day {N}: {Topic}`
- Start: 7:00 AM IST (Asia/Kolkata)
- End: 7:30 AM IST
- Color: Blueberry (9)
- Description: Full HTML study material (overview + key sections + resources)
- Reminder: 15 min popup + email

## Step 2 — Gmail Draft
- To: dhanushpeddemoni.work@gmail.com
- Subject: `🔬 Longevity Study | Day {N}: {Topic} | {Date}`
- Body: Full richly formatted HTML (complete study material)
- Draft lands in Drafts — user can send to self or read directly

## Step 3 — State Update
- Increment day_counter in state/day_counter.json
- Log delivery timestamp and topic

## Error Handling
- If Calendar event creation fails: log error, still send Gmail draft
- If Gmail draft fails: log error, Calendar event is the fallback
- Never silently skip both — alert user
