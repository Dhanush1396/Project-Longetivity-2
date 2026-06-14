# Task Plan — Project Longevity

## Project Goal
Build a daily longevity study agent that scrapes/finds resources, prepares study material in a Google Doc, blocks 30 min on Google Calendar with the Doc link, and emails the user daily.

## Phases

### Phase B — Blueprint ✅ COMPLETE
- [x] Discovery Q1: North Star — daily 30-min calendar block with Google Doc study material
- [x] Discovery Q2: Integrations — Firecrawl, Apify, Google Docs, Google Calendar, Gmail
- [x] Discovery Q3: Source of Truth — wide net: journals, YouTube, Substack, articles, websites
- [x] Discovery Q4: Delivery Payload — Doc + Calendar event (7 AM) + Gmail to dhanushpeddemoni.work@gmail.com
- [x] Discovery Q5: Behavioral Rules — academic & dense, cite sources, no pseudoscience
- [x] Data Schema defined in CLAUDE.md

### Phase L — Link [ IN PROGRESS ]
- [ ] Test Google Calendar MCP — create a probe event
- [ ] Test Gmail MCP — send a probe email
- [ ] Test Firecrawl — scrape a longevity article
- [ ] Test Apify — fetch structured data from a source
- [ ] Test Google Docs API — create a test doc (need credentials)
- [ ] Document all results in progress.md

### Phase A — Architect [ PENDING ]
- [ ] SOP: scrape_sources.md — how to search and scrape
- [ ] SOP: compile_material.md — how to build the study doc
- [ ] SOP: create_google_doc.md — how to create and format the Doc
- [ ] SOP: create_calendar_event.md — how to create the event
- [ ] SOP: send_gmail.md — how to send the email
- [ ] SOP: topic_curriculum.md — full topic progression list
- [ ] Navigation layer: main_agent.py
- [ ] Tool scripts in /execution/

### Phase S — Stylize [ PENDING ]
- [ ] Google Doc template finalized
- [ ] Calendar event format finalized
- [ ] Gmail template finalized
- [ ] End-to-end test run

### Phase T — Trigger [ PENDING ]
- [ ] Daily cron job configured (6:45 AM)
- [ ] State file for day counter
- [ ] Self-healing retry logic
- [ ] CLAUDE.md maintenance log complete
