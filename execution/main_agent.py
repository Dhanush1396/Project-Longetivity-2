#!/usr/bin/env python3
"""
Project Longevity — Daily Study Agent
Runs daily via GitHub Actions at 6:45 AM IST.
Reads today's topic → searches → compiles → delivers to Calendar + Gmail.
"""

import json
import os
import sys
import datetime
import subprocess
from pathlib import Path

import anthropic
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ── paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
STATE_FILE = ROOT / "state" / "day_counter.json"
CURRICULUM_FILE = ROOT / "architecture" / "05_thirty_day_curriculum.md"

# ── curriculum (30-day plan) ───────────────────────────────────────────────────
CURRICULUM = [
    {"day": 0,  "topic": "Why Do We Age? Evolutionary & Molecular Theories",          "anchor": "Williams 1957 + Sinclair Cell 2023"},
    {"day": 1,  "topic": "The 12 Hallmarks of Aging — The Master Framework",          "anchor": "López-Otín et al., Cell 2023"},
    {"day": 2,  "topic": "Epigenetic Clocks — Measuring Your Biological Age",         "anchor": "Horvath 2013 + DunedinPACE 2022"},
    {"day": 3,  "topic": "Telomeres & Telomerase — The Hayflick Limit & Beyond",      "anchor": "Blackburn, Greider, Szostak (Nobel 2009)"},
    {"day": 4,  "topic": "Cellular Senescence & the SASP",                            "anchor": "Campisi et al., Nature Reviews 2019"},
    {"day": 5,  "topic": "mTOR: The Central Hub of Aging Biology",                    "anchor": "Harrison et al., Nature 2009"},
    {"day": 6,  "topic": "AMPK & Sirtuins — The Energy Sensors of Longevity",        "anchor": "Guarente + Auwerx labs 2020–2024"},
    {"day": 7,  "topic": "Mitochondrial Dysfunction — The Energy Crisis of Aging",    "anchor": "Wallace 2005 + mitophagy research"},
    {"day": 8,  "topic": "Proteostasis & Autophagy — The Cell's Garbage System",     "anchor": "Ohsumi Nobel 2016 + Rubinsztein lab"},
    {"day": 9,  "topic": "Genomic Instability & DNA Repair in Aging",                "anchor": "Hoeijmakers group + NER pathway research"},
    {"day": 10, "topic": "Sleep Science and Longevity — The Non-Negotiable",          "anchor": "Walker 2017 + Xie et al., Science 2013"},
    {"day": 11, "topic": "VO2 Max, Exercise & All-Cause Mortality — The Data",        "anchor": "Kokkinos et al., NEJM 2022"},
    {"day": 12, "topic": "Strength Training, Muscle Mass & Longevity — The Evidence", "anchor": "Ruiz et al. 2008 + Westcott 2012"},
    {"day": 13, "topic": "Caloric Restriction — Mechanisms & Human Evidence",         "anchor": "CALERIE Trial + NIA studies"},
    {"day": 14, "topic": "Intermittent Fasting — What the Science Actually Shows",    "anchor": "Longo + Mattson 2019, NEJM review"},
    {"day": 15, "topic": "Protein Intake & the mTOR/Longevity Tradeoff",             "anchor": "Levine et al., Cell Metabolism 2014"},
    {"day": 16, "topic": "The Gut Microbiome in Aging — Dysbiosis & Interventions",  "anchor": "Claesson et al., Nature 2012 + 2024 trials"},
    {"day": 17, "topic": "Rapamycin — Deep Dive on the #1 Longevity Drug",           "anchor": "Harrison 2009 + ITP Program results"},
    {"day": 18, "topic": "Metformin & the TAME Trial",                               "anchor": "Barzilai + TAME Trial 2023–2024"},
    {"day": 19, "topic": "Senolytics — Dasatinib + Quercetin, Fisetin & Beyond",     "anchor": "Zhu et al., Nature Medicine 2015 + Mayo trials"},
    {"day": 20, "topic": "NAD+ Biology — NMN, NR & the Mitochondrial Connection",    "anchor": "Yoshino et al., Cell Metabolism 2021"},
    {"day": 21, "topic": "Cardiovascular Risk — ApoB, Lp(a) & Longevity Medicine",  "anchor": "Sniderman + Attia on LDL particle biology"},
    {"day": 22, "topic": "Cancer Through a Longevity Lens — Prevention, Not Treatment","anchor": "Surveillance data + liquid biopsy 2024"},
    {"day": 23, "topic": "The Aging Brain — Alzheimer's, Prevention & Cognitive Reserve","anchor": "Bredesen + FINGER trial"},
    {"day": 24, "topic": "Hormones & Longevity — Testosterone, Estrogen, GH, IGF-1","anchor": "WHI revisited + TRT evidence 2020–2024"},
    {"day": 25, "topic": "Centenarian Studies — What the Longest-Lived Humans Teach Us","anchor": "Sebastiani + New England Centenarian Study"},
    {"day": 26, "topic": "Partial Reprogramming — The Yamanaka Factor Revolution",   "anchor": "Sinclair OSK 2020 + Altos Labs 2022"},
    {"day": 27, "topic": "Senolytics in Humans — Clinical Trial Landscape 2024–2026","anchor": "Unity Biotechnology + Mayo Phase I/II"},
    {"day": 28, "topic": "AI in Longevity — Drug Discovery, Aging Clocks & Personalization","anchor": "AlphaFold + Insilico Medicine"},
    {"day": 29, "topic": "Building Your Personal Longevity Protocol — Evidence-Based","anchor": "Attia 'Outlive' framework + biomarker stacking"},
    {"day": 30, "topic": "The Next 10 Years in Longevity Science — What's Coming",   "anchor": "Altos Labs + Calico + XPRIZE Healthspan"},
]


def load_state() -> dict:
    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_today_entry(state: dict) -> dict:
    day = state["day"]
    # Cycle back after day 30
    idx = day % len(CURRICULUM)
    entry = CURRICULUM[idx].copy()
    entry["day"] = day
    return entry


def firecrawl_search(query: str, api_key: str, limit: int = 5) -> list[dict]:
    url = "https://api.firecrawl.dev/v1/search"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "query": query,
        "limit": limit,
        "scrapeOptions": {"formats": ["markdown"], "onlyMainContent": True},
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    results = data.get("data", {})
    if isinstance(results, dict):
        results = results.get("web", [])
    return results if isinstance(results, list) else []


def gather_sources(topic: str, api_key: str) -> list[dict]:
    print(f"  Searching: '{topic} longevity science research latest'")
    r1 = firecrawl_search(f"{topic} longevity science research latest", api_key)

    print(f"  Searching: '{topic} peer reviewed study findings 2023 2024'")
    r2 = firecrawl_search(f"{topic} peer reviewed study findings 2023 2024", api_key)

    print(f"  Searching: site-specific academic sources")
    r3 = firecrawl_search(
        f"{topic} site:pubmed.ncbi.nlm.nih.gov OR site:cell.com OR site:nature.com OR site:peterattiamd.com",
        api_key,
    )

    seen, sources = set(), []
    for r in [r1, r2, r3]:
        for item in r:
            url = item.get("url", "")
            if url and url not in seen:
                seen.add(url)
                sources.append({
                    "title": item.get("title", ""),
                    "url": url,
                    "excerpt": (item.get("markdown", "") or item.get("description", ""))[:1500],
                })
    return sources[:12]


def compile_material(entry: dict, sources: list[dict], claude_client: anthropic.Anthropic) -> str:
    day = entry["day"]
    topic = entry["topic"]
    anchor = entry["anchor"]

    next_idx = (day + 1) % len(CURRICULUM)
    next_topic = CURRICULUM[next_idx]["topic"]
    next_anchor = CURRICULUM[next_idx]["anchor"]

    sources_text = "\n\n".join(
        f"SOURCE {i+1}: {s['title']}\nURL: {s['url']}\nEXCERPT:\n{s['excerpt']}"
        for i, s in enumerate(sources)
    )

    prompt = f"""You are compiling a premium daily longevity study session for a serious learner.

DAY: {day}
TOPIC: {topic}
ANCHOR PAPER(S): {anchor}
NEXT TOPIC (for preview): Day {day+1} — {next_topic} (anchor: {next_anchor})

SOURCES RETRIEVED:
{sources_text}

INSTRUCTIONS:
Compile a deep, academic-tone HTML study document (~3,500–4,500 words) following this exact structure.
The HTML will be sent as an email body so use inline styles only. Use dark theme: background #0f1117, text #e8e4d9, headings #d4edda, accents #52b788, links #52b788.

REQUIRED STRUCTURE:
1. HEADER — Day N | Topic | Date | Anchor papers box
2. OVERVIEW (~300 words) — What this is, why it matters, key question answered
3. THE SCIENCE (~1200–1500 words) — Core mechanisms, specific studies cited inline with [Author, Year, URL], exact numbers, experimental evidence, molecular pathways
4. CURRENT STATE OF RESEARCH (~700 words) — Where the science stands, active debates, open questions, recent breakthroughs (2023–2025)
5. PRACTICAL IMPLICATIONS (~500 words) — Evidence-based actions, formatted as a 2-column table, plus a "What NOT to do" box
6. KEY TAKEAWAYS — 7 bullet points, crisp and specific
7. CITED RESOURCES — Table of all sources: title hyperlinked, journal/type, one-line description
8. NEXT SESSION PREVIEW — Tomorrow's topic and how it builds on today

TONE RULES:
- Academic and dense — no dumbing down, no hedging
- Every claim must cite a specific paper with author, year, and link inline
- Include specific numbers: percentages, fold-changes, sample sizes, p-values where known
- No supplement recommendations, no pseudoscience
- Inline links throughout the text (not just in the resources section)
- Highlight the 3 most surprising/counterintuitive findings

Return ONLY the complete HTML document. No preamble, no explanation."""

    response = claude_client.messages.create(
        model="claude-opus-4-8",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def get_google_creds() -> Credentials:
    # Don't pass scopes here — they're already encoded in the refresh token.
    # Passing mismatched scopes causes invalid_scope errors.
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    )
    creds.refresh(Request())
    return creds


def create_calendar_event(creds: Credentials, entry: dict, html_content: str) -> str:
    service = build("calendar", "v3", credentials=creds)

    day = entry["day"]
    topic = entry["topic"]

    IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
    now_ist = datetime.datetime.now(IST)
    # If it's already past 7 AM IST, schedule for tomorrow; otherwise today
    today_7am = now_ist.replace(hour=7, minute=0, second=0, microsecond=0)
    event_date = (now_ist + datetime.timedelta(days=1)).date() if now_ist > today_7am else now_ist.date()
    start_ist = datetime.datetime.combine(
        event_date,
        datetime.time(7, 0, 0),
        tzinfo=IST,
    )
    end_ist = start_ist + datetime.timedelta(minutes=30)

    # Build a concise calendar description (no full HTML — use summary)
    cal_desc = f"🔬 LONGEVITY STUDY — DAY {day}: {topic.upper()}\n\nOpen Gmail for the full richly formatted study material.\n\nAnchor: {entry['anchor']}"

    event = {
        "summary": f"🔬 Longevity Study — Day {day}: {topic}",
        "description": cal_desc,
        "start": {"dateTime": start_ist.isoformat(), "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_ist.isoformat(), "timeZone": "Asia/Kolkata"},
        "colorId": "9",  # Blueberry
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 15},
                {"method": "email", "minutes": 15},
            ],
        },
    }

    result = service.events().insert(calendarId="primary", body=event).execute()
    return result["id"]


def create_gmail_draft(creds: Credentials, entry: dict, html_content: str) -> str:
    service = build("gmail", "v1", credentials=creds)

    day = entry["day"]
    topic = entry["topic"]
    date_str = datetime.date.today().strftime("%B %d, %Y")

    subject = f"🔬 Longevity Study | Day {day}: {topic} | {date_str}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["To"] = "dhanushpeddemoni.work@gmail.com"

    plain = f"Day {day}: {topic}\n\nOpen the HTML version to read the full formatted study material.\n\nAnchor: {entry['anchor']}"
    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    draft = service.users().drafts().create(userId="me", body={"message": {"raw": raw}}).execute()
    return draft["id"]


def update_state(state: dict, entry: dict, cal_id: str, draft_id: str):
    state["day"] = entry["day"] + 1
    state["last_run"] = datetime.datetime.utcnow().isoformat() + "Z"
    state["last_topic"] = entry["topic"]
    if "history" not in state:
        state["history"] = []
    state["history"].append({
        "day": entry["day"],
        "topic": entry["topic"],
        "calendar_event_id": cal_id,
        "gmail_draft_id": draft_id,
        "delivered": datetime.datetime.utcnow().isoformat() + "Z",
    })
    save_state(state)


def git_commit_and_push():
    subprocess.run(["git", "config", "user.email", "noreply@anthropic.com"], check=True)
    subprocess.run(["git", "config", "user.name", "Claude"], check=True)
    subprocess.run(["git", "add", str(STATE_FILE)], check=True)
    subprocess.run(
        ["git", "commit", "-m", "chore: update day counter after daily delivery"],
        check=True,
    )
    subprocess.run(
        ["git", "push", "origin", "claude/epic-wright-a4elc9"],
        check=True,
    )


def main():
    print("=== Project Longevity Daily Agent ===")

    # ── validate env ───────────────────────────────────────────────────────────
    required = ["ANTHROPIC_API_KEY", "FIRECRAWL_API_KEY", "GOOGLE_CLIENT_ID",
                "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print(f"ERROR: Missing environment variables: {missing}")
        sys.exit(1)

    # ── load state & pick today's topic ───────────────────────────────────────
    state = load_state()
    entry = get_today_entry(state)
    print(f"Day {entry['day']}: {entry['topic']}")

    # ── search ────────────────────────────────────────────────────────────────
    print("\n[1/4] Searching for sources...")
    sources = gather_sources(entry["topic"], os.environ["FIRECRAWL_API_KEY"])
    print(f"  Found {len(sources)} sources")

    # ── compile ───────────────────────────────────────────────────────────────
    print("\n[2/4] Compiling study material via Claude...")
    claude_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    html_content = compile_material(entry, sources, claude_client)
    print(f"  Generated {len(html_content):,} chars of HTML")

    # ── deliver ───────────────────────────────────────────────────────────────
    print("\n[3/4] Delivering to Google Calendar + Gmail...")
    creds = get_google_creds()

    cal_id, draft_id = None, None
    try:
        cal_id = create_calendar_event(creds, entry, html_content)
        print(f"  ✓ Calendar event: {cal_id}")
    except Exception as e:
        print(f"  ✗ Calendar event failed: {e}")

    try:
        draft_id = create_gmail_draft(creds, entry, html_content)
        print(f"  ✓ Gmail draft: {draft_id}")
    except Exception as e:
        print(f"  ✗ Gmail draft failed: {e}")

    if not cal_id and not draft_id:
        print("ERROR: Both delivery methods failed. Not updating state.")
        sys.exit(1)

    # ── update state ──────────────────────────────────────────────────────────
    print("\n[4/4] Updating state and pushing to GitHub...")
    update_state(state, entry, cal_id or "", draft_id or "")
    git_commit_and_push()

    print(f"\n✓ Day {entry['day']} delivered successfully.")
    print(f"  Topic: {entry['topic']}")
    print(f"  Calendar: {cal_id}")
    print(f"  Gmail draft: {draft_id}")


if __name__ == "__main__":
    main()
