# SOP: Scrape Sources

## Purpose
Search and retrieve high-quality longevity content for the day's topic.

## Tool
Firecrawl MCP (`firecrawl_search`) — primary search tool.

## Process
1. Run 3 searches per topic:
   - `{topic} longevity science research latest`
   - `{topic} peer reviewed study findings`
   - `{topic} site:pubmed.ncbi.nlm.nih.gov OR site:biorxiv.org OR site:peterattiamd.com OR site:hubermanlab.com`
2. Collect up to 5 sources per search (15 total candidates)
3. Filter: remove paywalled, low-quality, supplement-ad pages
4. Target 5–8 final cited sources

## Quality Criteria
- Peer-reviewed journals (PubMed, bioRxiv, Nature, Cell)
- Reputable researchers/practitioners (Attia, Huberman, Sinclair, Levine, de Grey)
- Well-sourced journalism (Vox, The Atlantic, NYT Science)
- Substack by credentialed authors
- NO: supplement store blogs, unverified biohack sites, clickbait

## Output
List of sources with: title, URL, type, key excerpt
