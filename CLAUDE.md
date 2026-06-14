# CLAUDE.md — Project Longevity Constitution

## Mission
Build a daily longevity study agent that researches cutting-edge longevity science, compiles a focused 30-min study session into a Google Doc, creates a Google Calendar block with the Doc link, and sends a Gmail notification — all following a structured topic progression from fundamentals to advanced.

---

## B.L.A.S.T. Phase Outputs

### B — Blueprint ✅

**North Star:**
Every morning the user opens their calendar and finds a 30-min block with a focused, readable Google Doc link covering the latest longevity research/advancements — progressing day by day from basics to advanced topics.

**Integrations:**
| Service | Purpose | Credential Status |
|---|---|---|
| Firecrawl | Web scraping — articles, Substack, websites | Connected via MCP |
| Apify | Structured extraction — YouTube, journals | Connected via MCP |
| Notion | Create daily study page with material + resources | Needs API token |
| Google Calendar | Create 30-min daily event with Doc link | Connected via MCP |
| Gmail | Send daily email with Doc link to user | Connected via MCP |

**Source of Truth:**
Wide net across all formats — PubMed, bioRxiv, Substack longevity writers, YouTube (Huberman Lab, Peter Attia, Bryan Johnson, etc.), news articles, research blogs, longevity-focused websites. Priority: cutting-edge, peer-reviewed or well-sourced.

**Delivery Payload:**
1. **Notion page** — created fresh each day under a "Longevity Study Material" database, titled `Day {N}: {Topic}`, containing compiled study material + cited resource links
2. **Google Calendar** — 30-min event at 7:00 AM IST with Notion page link in description
3. **Gmail** — daily email to `dhanushpeddemoni.work@gmail.com` with Notion link and topic summary

**Topic Progression:**
Structured curriculum starting from fundamentals, advancing daily:
- Week 1: Foundations (what is longevity, hallmarks of aging, lifespan vs healthspan)
- Week 2: Biology of aging (telomeres, senescence, mitochondria, epigenetics)
- Week 3: Interventions I (sleep, exercise, nutrition science)
- Week 4: Interventions II (fasting, caloric restriction, hormesis)
- Week 5+: Advanced (senolytics, rapamycin, NMN/NAD+, gene therapy, biomarkers, latest trials)
- Ongoing: Rotating deep-dives into cutting-edge research and breakthroughs

**Behavioral Rules:**
- Tone: Academic & dense — written for someone serious about learning the science
- Always cite sources with direct links
- Avoid: supplement advertisements, pseudoscience, unverified biohacks, cosmetic anti-aging content
- Content: enough for 30 min of focused reading (approx 2,500–4,000 words + resources)
- Sources must be peer-reviewed, reputable researchers, or well-sourced journalism

---

### L — Link
_Pending — Phase L: verify all API connections_

### A — Architect
_Pending_

### S — Stylize
_Pending_

### T — Trigger
_Pending_

---

## Data Schema

### Input (Agent receives each day)
```json
{
  "day_number": 1,
  "topic": "What is Longevity? Lifespan vs Healthspan",
  "topic_category": "Foundations",
  "scheduled_time": "07:00",
  "user_email": "dhanushpeddemoni.work@gmail.com"
}
```

### Intermediate (scraped + compiled)
```json
{
  "day_number": 1,
  "topic": "string",
  "sources": [
    {
      "title": "string",
      "url": "string",
      "type": "journal | article | youtube | substack | website",
      "summary": "string",
      "cited": true
    }
  ],
  "compiled_content": "markdown string — full study material",
  "word_count": 3000
}
```

### Output (what gets delivered)
```json
{
  "notion_page_url": "https://notion.so/...",
  "notion_page_id": "string",
  "calendar_event_id": "string",
  "calendar_event_link": "string",
  "gmail_sent": true,
  "day_number": 1,
  "topic": "string",
  "delivery_timestamp": "ISO8601"
}
```

---

## Architectural Invariants
- Logic is deterministic; LLM used only for content synthesis, not routing decisions
- All intermediate files go through `/.tmp/`
- Credentials live in `.env` only — never hardcoded
- Day counter persists in `/.tmp/day_counter.json` or a simple state file
- If any delivery step fails, the system logs the error and retries — it does NOT silently skip

---

## Triggers
- **Daily cron** at 6:45 AM → scrape → compile → create Doc → create Calendar event → send Gmail
- _Full trigger config to be defined in Phase T_

---

## Maintenance Log
_To be populated in Phase T_
