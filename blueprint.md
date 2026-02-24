# 🔌 AI/ML Daily Digest — Complete MCP Implementation Blueprint
### Zero Scrapers · Zero Cost · 100% Automated · Works Even When Your PC is OFF

---

## 📋 Table of Contents

1. [Critical First — What Happens When Your PC is Off?](#1-critical-first--what-happens-when-your-pc-is-off)
2. [What is MCP and Why Use it Instead of Scrapers?](#2-what-is-mcp-and-why-use-it-instead-of-scrapers)
3. [The Big Idea — 3 Servers Instead of 13](#3-the-big-idea--3-servers-instead-of-13)
4. [Full System Architecture](#4-full-system-architecture)
5. [What is FastMCP and How Do You Build With It?](#5-what-is-fastmcp-and-how-do-you-build-with-it)
6. [Server 1 — Research Server (Papers, RSS, Blogs)](#6-server-1--research-server-papers-rss-blogs)
7. [Server 2 — Community Server (Reddit, HN, HuggingFace)](#7-server-2--community-server-reddit-hn-huggingface)
8. [Server 3 — Utility Server (Crawl, Memory, Search)](#8-server-3--utility-server-crawl-memory-search)
9. [Already Cloud-Hosted MCPs — Zero Setup Needed](#9-already-cloud-hosted-mcps--zero-setup-needed)
10. [Complete Master Source Coverage Map](#10-complete-master-source-coverage-map)
11. [How to Deploy to Prefect Horizon (Step by Step)](#11-how-to-deploy-to-prefect-horizon-step-by-step)
12. [GitHub Actions — The Free 24/7 Cron Trigger](#12-github-actions--the-free-247-cron-trigger)
13. [Complete Pipeline Flow (PC Off, Everything Automated)](#13-complete-pipeline-flow-pc-off-everything-automated)
14. [Project Folder Structure — All 3 Repos](#14-project-folder-structure--all-3-repos)
15. [How Each Tool Works — Source by Source](#15-how-each-tool-works--source-by-source)
16. [Detailed Sample Outputs](#16-detailed-sample-outputs)
17. [Step-by-Step Build Timeline — Scratch to Production](#17-step-by-step-build-timeline--scratch-to-production)
18. [Complete Accounts & Keys Setup](#18-complete-accounts--keys-setup)
19. [Final Cost Summary](#19-final-cost-summary)
20. [Final Launch Checklist](#20-final-launch-checklist)

---

## 1. Critical First — What Happens When Your PC is Off?

> This is the most important question. Everything else builds on the answer.

### The Problem With Self-Hosted MCP Servers

When people talk about "self-hosted MCP servers," they mean the server process runs on your own machine. If your machine is off, the server is off. GitHub Actions is a cloud service — it runs on GitHub's servers — but if it tries to call an MCP server that lives on your PC and your PC is off, the call fails and you get nothing.

### The Solution — Cloud-Deploy Everything

The answer is to deploy all your MCP servers to **Prefect Horizon**, a free cloud platform built specifically for MCP servers. Your servers run on Horizon's infrastructure 24 hours a day, 7 days a week, regardless of whether your PC is on, off, asleep, or broken.

```
WRONG SETUP (PC must be always on):
─────────────────────────────────────────────────
GitHub Actions (cloud)
        ↓  calls
Your PC (must be ON and running MCP servers)
        ↓  if PC is off
        ✗  Pipeline fails. No digest. No notifications.


CORRECT SETUP (PC never needed):
─────────────────────────────────────────────────
GitHub Actions (cloud)
        ↓  calls
Prefect Horizon URLs (cloud, always online 24/7)
        ↓  returns data
Gemini Flash 2.0 (cloud)
        ↓  saves
Supabase (cloud)
        ↓  sends to
Email + Telegram + Discord
        ↓
Dashboard on Vercel (cloud)

YOUR PC = NEVER NEEDED ✅
```

### The Three Layers That Make This Work

```
LAYER 1 — Trigger (GitHub Actions)
  Runs on GitHub's cloud servers
  Wakes up at 7:00 AM IST every day
  Your PC does not need to be on
  Free: 2,000 minutes/month

LAYER 2 — MCP Servers (Prefect Horizon)
  Your custom FastMCP servers deployed to Horizon
  Run 24/7 on Horizon's cloud infrastructure
  Free for personal projects
  Auto-redeploy on every git push

LAYER 3 — External Cloud MCPs (GitHub, HF, Supabase)
  Already hosted by their own companies
  No deployment needed at all
  Just use their URLs
  Free with free accounts
```

---

## 2. What is MCP and Why Use it Instead of Scrapers?

### MCP (Model Context Protocol) — Simple Explanation

MCP is an open standard created by Anthropic in late 2024. Think of it as a universal connector — like a USB port — between AI systems and data sources. Instead of writing custom scraping code for every website, you plug in a pre-built MCP server that already handles all the API calls, authentication, parsing, and error handling for that source.

```
SCRAPER APPROACH (what you wanted to avoid):
──────────────────────────────────────────────────────────
You write Python scraper for ArXiv
  → ArXiv changes their HTML structure
  → Your scraper breaks
  → You spend 2 hours debugging
  → Fix it
  → It breaks again next month

You write Python scraper for Reddit
  → Reddit changes their API rules
  → Your scraper breaks
  → Reddit starts blocking requests
  → You debug again

Repeat this for every single source. Forever.
Maintenance nightmare.


MCP APPROACH (what this blueprint uses):
──────────────────────────────────────────────────────────
arxiv-mcp-server → already handles everything for ArXiv
reddit-mcp-buddy  → already handles everything for Reddit
github-mcp-server → already handles everything for GitHub

You just CALL the tool with parameters.
Community maintains the server.
When APIs change, someone else fixes it.
You focus on your pipeline logic, not scraping code.
```

### How MCP Communication Works

```
YOUR PIPELINE                    MCP SERVER               DATA SOURCE
─────────────────                ──────────────────       ─────────────
"Give me latest papers           arxiv-mcp-server         ArXiv API
 from cs.AI last 24h"      →     receives request    →    queries API
                                  formats response         returns JSON
                           ←     returns items       ←
  [{title, authors,
    abstract, url,
    published_at}]

The pipeline never touches ArXiv directly.
The MCP server is the intermediary.
```

### FastMCP — The Framework for Building MCP Servers

FastMCP is the standard framework for writing MCP servers in Python. It was created shortly after Anthropic announced MCP, was incorporated into the official MCP Python SDK, and today powers 70% of all MCP servers. It is downloaded over one million times a day.

The core concept is simple: you write a regular Python function that fetches data, add a decorator on top of it, and FastMCP automatically turns it into a fully compliant MCP tool. All the protocol complexity — schema generation, parameter validation, error handling, connection management — is handled for you automatically. You focus purely on the data-fetching logic.

```
THE PATTERN:
────────────
1. Create a FastMCP server instance with a name
2. Write Python functions that fetch data from APIs
3. Add @mcp.tool decorator above each function
4. FastMCP auto-generates MCP schema from function signature
5. Push to GitHub → deploy to Horizon → get a live URL

That URL is what GitHub Actions calls every morning.
```

---

## 3. The Big Idea — 3 Servers Instead of 13

### Your Original Instinct (Correct!)

You correctly identified that creating one GitHub repo per MCP server is wasteful. If you had 13 tools, that's 13 repos, 13 deployments, 13 URLs to manage. Instead, you group all logically-related tools into one FastMCP server. One server = one repo = one Horizon deployment = one URL.

### The 3-Server Grouping Strategy

```
ALL YOUR TOOLS GROUPED INTO 3 LOGICAL SERVERS:
─────────────────────────────────────────────────────────────────────

SERVER 1: ai-digest-research-server
  GitHub Repo:   github.com/YOUR_USERNAME/ai-digest-research-server
  Horizon URL:   https://ai-digest-research.YOUR_NAME.fastmcp.app/mcp
  Purpose:       Everything about finding content — research papers,
                 blog posts, RSS feeds, any URL
  Tools inside:  arxiv, papers_with_code, semantic_scholar,
                 openreview (conferences), kaggle, rss_feeds,
                 fetch_any_url
  Covers:        Sections 1, 2, 7, 8, 9, 10 of master list


SERVER 2: ai-digest-community-server
  GitHub Repo:   github.com/YOUR_USERNAME/ai-digest-community-server
  Horizon URL:   https://ai-digest-community.YOUR_NAME.fastmcp.app/mcp
  Purpose:       Everything about community signals — social platforms,
                 discussions, trending models and tools
  Tools inside:  reddit (5 subreddits), hacker_news,
                 huggingface (models, spaces, papers, leaderboard)
  Covers:        Sections 3, 5 of master list


SERVER 3: ai-digest-utility-server
  GitHub Repo:   github.com/YOUR_USERNAME/ai-digest-utility-server
  Horizon URL:   https://ai-digest-utility.YOUR_NAME.fastmcp.app/mcp
  Purpose:       Supporting tools — JS page rendering, memory,
                 search, pipeline utilities
  Tools inside:  crawl4ai (JS pages), searxng (web search),
                 memory (persistent preferences)
  Covers:        Hard-to-reach pages, bot memory, live search


ALREADY CLOUD-HOSTED (zero repos, zero deployment needed):
  GitHub MCP     → api.githubcopilot.com/mcp/          (GitHub hosts it)
  Supabase MCP   → mcp.supabase.com                    (Supabase hosts it)
  Context7 MCP   → via npx command                     (Context7 hosts it)
  HuggingFace MCP→ huggingface.co/mcp                  (HF hosts it)
  Covers:        Section 3 (GitHub repos + releases), Sections 4, 9
─────────────────────────────────────────────────────────────────────
RESULT:
  3 GitHub repos
  3 Horizon deployments
  4 external cloud MCPs (no setup needed)
  Total: 7 MCP URLs in your config
  Monthly cost: $0
```

---

## 4. Full System Architecture

```
╔═══════════════════════════════════════════════════════════════════════╗
║             GITHUB ACTIONS — FREE CLOUD CRON SCHEDULER               ║
║        Triggers at 7:00 AM IST (1:30 AM UTC) every single day        ║
║        Runs on GitHub's servers — your PC never needs to be on        ║
╚═══════════════════════════════╦═══════════════════════════════════════╝
                                ║
          ┌─────────────────────┼───────────────────────┐
          ▼                     ▼                       ▼
╔═══════════════════╗  ╔═════════════════════╗  ╔═══════════════════════╗
║ SERVER 1          ║  ║ SERVER 2            ║  ║ CLOUD MCPs            ║
║ Research Server   ║  ║ Community Server    ║  ║ (already hosted)      ║
║ (Prefect Horizon) ║  ║ (Prefect Horizon)   ║  ║                       ║
║                   ║  ║                     ║  ║ GitHub MCP            ║
║ Tools:            ║  ║ Tools:              ║  ║ → Repos + Releases    ║
║ → arxiv           ║  ║ → reddit            ║  ║ → Trending repos      ║
║ → papers_with_code║  ║ → hacker_news       ║  ║ → All 22 framework    ║
║ → semantic_scholar║  ║ → huggingface       ║  ║   releases monitored  ║
║ → openreview      ║  ║   (models, spaces,  ║  ║                       ║
║ → kaggle          ║  ║    papers,          ║  ║ Supabase MCP          ║
║ → rss_feeds       ║  ║    leaderboard)     ║  ║ → Save all results    ║
║ → fetch_url       ║  ║                     ║  ║ → Query digest data   ║
║                   ║  ║                     ║  ║                       ║
║ OUTPUT:           ║  ║ OUTPUT:             ║  ║ Context7 MCP          ║
║ ~200 items        ║  ║ ~150 items          ║  ║ → Live framework docs  ║
╚═══════════════════╝  ╚═════════════════════╝  ╚═══════════════════════╝
          │                     │                       │
          └─────────────────────┼───────────────────────┘
                                ║
                    ┌───────────▼────────────┐
                    │   SERVER 3             │
                    │   Utility Server       │
                    │   (Prefect Horizon)    │
                    │                        │
                    │   Tools:               │
                    │   → crawl4ai           │
                    │   → searxng (search)   │
                    │   → memory             │
                    │                        │
                    │   Used for:            │
                    │   JS-heavy pages,      │
                    │   bot /search command  │
                    │   preference memory    │
                    └───────────┬────────────┘
                                ║
                                ▼
╔═══════════════════════════════════════════════════════════════════════╗
║                DEDUPLICATION (runs in GitHub Actions)                 ║
║          Raw input: ~450-500 items from all servers                   ║
║          Stage 1: URL hash check (remove exact duplicates)            ║
║          Stage 2: 85% fuzzy title match (remove near-duplicates)      ║
║          Output: ~150-250 unique items                                 ║
╚═══════════════════════════════╦═══════════════════════════════════════╝
                                ║
                                ▼
╔═══════════════════════════════════════════════════════════════════════╗
║              GEMINI FLASH 2.0 — 1 SINGLE BATCH API CALL              ║
║         All 150-250 items sent at once (1M token context window)      ║
║         Returns for each item:                                         ║
║           → 2-sentence technical summary                               ║
║           → Relevance score 1-10                                       ║
║           → is_breaking flag (true/false)                              ║
║           → Tags array (LLM, RAG, Agents, MCP, etc.)                  ║
║           → Framework mentions array                                   ║
║         Free tier: 1,500 requests/day — using only 1-2 per day       ║
╚═══════════════════════════════╦═══════════════════════════════════════╝
                                ║
                                ▼
╔═══════════════════════════════════════════════════════════════════════╗
║              SUPABASE (via Supabase MCP — cloud hosted)               ║
║         Tables: news_items | papers | github_repos | digest_runs      ║
║         Free tier: 500MB, 50,000 rows                                  ║
╚═══════════════════════════════╦═══════════════════════════════════════╝
                                ║
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
          📧 Resend       🤖 Telegram     🎮 Discord
          Email           Bot Push        Webhook
          Digest          + Commands      Embeds
                 └──────────────┼──────────────┘
                                ▼
                    🖥️ Next.js Dashboard
                        (Vercel — FREE)
                    Always live, reads Supabase directly
```

---

## 5. What is FastMCP and How Do You Build With It?

### Getting FastMCP

FastMCP is a Python library. You get it via pip, the Python package installer. It is hosted on PyPI (the Python Package Index) at `pypi.org/project/fastmcp`. The GitHub repository is at `github.com/PrefectHQ/fastmcp` and the full documentation is at `gofastmcp.com`.

```
WHERE TO GET IT:
─────────────────────────────────────────────
Official Documentation:  gofastmcp.com
GitHub Repository:       github.com/PrefectHQ/fastmcp
PyPI Package:            pip install fastmcp
Discord Community:       discord.gg/fastmcp (for help)
```

### The Three Building Blocks of a FastMCP Server

Every FastMCP server is made of three types of components:

```
1. TOOLS
   → Python functions that the pipeline CALLS to fetch data
   → Decorated with @mcp.tool
   → Accepts parameters, returns data
   → Example: fetch_arxiv_papers(category="cs.AI", days=1)
   → This is what you use for 95% of your digest sources

2. RESOURCES
   → Read-only data that can be exposed as reference material
   → Decorated with @mcp.resource
   → Example: expose your rss_sources.yaml as a readable resource
   → Less important for your project

3. PROMPTS
   → Reusable instruction templates
   → Decorated with @mcp.prompt
   → Not relevant for your digest project
```

### How a Tool Is Defined (Conceptual, No Code)

A tool is simply a Python function with three things:
- A descriptive function name (this becomes the tool name)
- A docstring explaining what it does (this becomes the tool description that the LLM reads)
- Type annotations on all parameters and return value (FastMCP generates the schema from these)

The `@mcp.tool` decorator above the function is all that's needed to register it as an MCP tool. FastMCP handles everything else — the JSON schema, the parameter validation, the error handling, the protocol compliance.

### How Multiple Tools Go in One Server

You create one `FastMCP` server instance at the top of your file. Then every function with `@mcp.tool` below it becomes a tool in that server. There is no limit to how many tools one server can have. All tools share the same server instance, same dependencies, same deployment.

```
CONCEPTUAL STRUCTURE OF ONE SERVER FILE:
──────────────────────────────────────────
Create server instance: mcp = FastMCP("Research Server")

Tool 1: fetch_arxiv_papers    → queries ArXiv API
Tool 2: fetch_arxiv_recent    → gets papers from last 24h
Tool 3: search_papers_with_code → queries PWC API
Tool 4: get_sota_benchmarks   → gets PWC leaderboards
Tool 5: search_semantic_scholar → queries S2 API
Tool 6: get_trending_citations → gets top cited papers
Tool 7: get_conference_papers  → queries OpenReview
Tool 8: fetch_rss_feed        → fetches one RSS/Atom feed URL
Tool 9: fetch_all_feeds       → fetches all 35+ configured feeds
Tool 10: fetch_url            → fetches any URL as Markdown
Tool 11: search_kaggle_datasets → queries Kaggle API

All 11 tools in ONE file, ONE server, ONE GitHub repo,
ONE Horizon deployment, ONE URL to call.
```

### Tool Naming Convention

Tools are organized using a namespace pattern so you can tell them apart:

```
NAMING PATTERN: category/action_name
─────────────────────────────────────
arxiv/search             → search ArXiv
arxiv/get_recent         → get recent papers
papers/trending          → trending on PWC
papers/sota              → SOTA benchmarks
scholar/search           → search Semantic Scholar
openreview/neurips       → NeurIPS papers
openreview/icml          → ICML papers
rss/fetch_feed           → one RSS feed
rss/fetch_all            → all configured feeds
fetch/url                → any URL
kaggle/datasets          → Kaggle datasets
kaggle/competitions      → Kaggle competitions
reddit/r_machinelearning → ML subreddit
reddit/r_localllama      → LocalLLaMA subreddit
hn/top_ai                → HN AI top stories
hf/trending_models       → HF models
hf/daily_papers          → HF daily papers
crawl/page               → render any JS page
memory/save              → save preference
search/web               → web search
```

---

## 6. Server 1 — Research Server (Papers, RSS, Blogs)

### What This Server Covers

This is your heaviest server. It handles all research paper sources, all RSS/blog feeds, URL fetching, and dataset sources. Almost everything from Sections 1, 2, 7, 8, 9, 10 of your master list.

```
ai-digest-research-server
─────────────────────────────────────────────────────────────────
GitHub Repo:  github.com/YOUR_USERNAME/ai-digest-research-server
Horizon URL:  https://ai-digest-research.YOUR_NAME.fastmcp.app/mcp
Language:     Python
Framework:    FastMCP 3.0
Auth:         None for most tools (Kaggle needs free API token)
```

### Tools Inside This Server

```
TOOL GROUP 1: ArXiv Papers
──────────────────────────
Tool: arxiv/search
  What it does:  Full-text search across all ArXiv papers
  Input params:  query keyword, category (cs.AI etc.), max results
  Returns:       List of papers with title, authors, abstract, URL, date
  Source API:    arxiv.org API (completely free, no auth)
  How to get:    pip install arxiv (official ArXiv Python library)
                 Docs: info.arxiv.org/help/api/index.html

Tool: arxiv/get_recent
  What it does:  Papers submitted in the last N days in a category
  Input params:  category, days_back (default: 1), max results
  Returns:       Same as above, sorted by submission date
  Source API:    Same ArXiv API, sorted by submittedDate


TOOL GROUP 2: Papers With Code
────────────────────────────────
Tool: papers/trending
  What it does:  Trending papers on Papers With Code today
  Input params:  max_results (default: 20)
  Returns:       Paper title, abstract, GitHub repo URL, paper URL
  Source API:    paperswithcode.com/api/v1/ (free, no auth needed)
  How to get:    Direct HTTP calls to PWC REST API
                 Docs: paperswithcode.com/api/v1/docs

Tool: papers/sota
  What it does:  Latest SOTA benchmark result updates
  Input params:  task (optional filter), max_results
  Returns:       Task name, benchmark name, best method, paper link
  Source API:    Same PWC API /results/ endpoint


TOOL GROUP 3: Semantic Scholar
────────────────────────────────
Tool: scholar/search
  What it does:  Search academic papers, get citation counts
  Input params:  query, fields (citations, abstract, year), max_results
  Returns:       Papers with title, authors, citations, abstract, URL
  Source API:    api.semanticscholar.org/graph/v1 (free, optional key)
  How to get:    Optional free API key from semanticscholar.org/product/api
                 Docs: api.semanticscholar.org/api-docs

Tool: scholar/trending_citations
  What it does:  Top-cited ML papers published in the last 7 days
  Input params:  min_citations, max_results
  Returns:       Papers sorted by recent citation velocity


TOOL GROUP 4: OpenReview (Conference Papers)
────────────────────────────────────────────
Tool: openreview/neurips
  What it does:  NeurIPS accepted papers
  Input params:  year, max_results, offset for pagination
  Returns:       Paper title, abstract, authors, forum URL
  Source API:    api2.openreview.net (free, needs free account)
  How to get:    Free account at openreview.net (just email + password)
                 Docs: docs.openreview.net/reference/api-v2

Tool: openreview/icml
  What it does:  ICML accepted papers
  Same structure as above, different venue ID

Tool: openreview/iclr
  What it does:  ICLR accepted papers
  Same structure as above, different venue ID

Tool: openreview/acl
  What it does:  ACL and EMNLP papers
  Same structure as above, multiple venue IDs

Tool: openreview/cvpr
  What it does:  CVPR computer vision papers
  Same structure as above, different venue ID


TOOL GROUP 5: RSS and Blog Feeds
──────────────────────────────────
Tool: rss/fetch_feed
  What it does:  Fetches any single RSS or Atom feed URL
  Input params:  feed_url, max_items (default: 10)
  Returns:       List of items with title, link, summary, published date
  Library used:  feedparser (pip install feedparser)
                 feedparser.org — most reliable RSS parser for Python
  How to get:    pip install feedparser
                 Docs: feedparser.readthedocs.io

Tool: rss/fetch_all
  What it does:  Fetches ALL 35+ configured feeds simultaneously (async)
  Input params:  category filter (optional), max_items_per_feed
  Returns:       All items across all feeds in one merged list
  Config file:   rss_sources.yaml (lists all 35+ feed URLs with metadata)

ALL 35+ FEEDS CONFIGURED IN rss_sources.yaml:

  Company Blogs (all have RSS/Atom feeds):
  ├── Google AI Blog          ai.googleblog.com/feeds/posts/default
  ├── DeepMind Blog           deepmind.com/blog/rss.xml
  ├── OpenAI Blog             openai.com/blog/rss/
  ├── Anthropic Blog          anthropic.com/blog/rss
  ├── Meta AI / FAIR          research.facebook.com/blog/rss
  ├── Microsoft Research      microsoft.com/en-us/research/blog/feed/
  ├── NVIDIA Developer        blogs.nvidia.com/blog/feed/
  ├── HuggingFace Blog        huggingface.co/blog/feed
  ├── W&B Blog                wandb.ai/site/rss
  ├── AWS ML Blog             aws.amazon.com/blogs/machine-learning/feed/
  ├── Google Cloud AI         cloud.google.com/.../feed
  ├── Modal Labs Blog         (RSS feed URL)
  ├── Replicate Blog          (RSS feed URL)
  ├── Perplexity AI Blog      (RSS feed URL)
  ├── Together AI Blog        (RSS feed URL)
  └── a16z AI Blog            (RSS feed URL)

  Agentic Framework Blogs:
  ├── LangChain Blog          blog.langchain.dev/feed.xml
  ├── LlamaIndex Blog         blog.llamaindex.ai/feed
  └── MCP Blog                modelcontextprotocol.io/blog/feed.xml

  Newsletters:
  ├── The Batch               deeplearning.ai RSS feed
  ├── Import AI               Jack Clark newsletter RSS
  ├── BAIR Blog               bair.berkeley.edu/blog/feed.xml
  ├── Gradient Flow           Ben Lorica newsletter RSS
  └── KDnuggets               kdnuggets.com/feed

  Backend Framework Releases (via GitHub Atom):
  ├── FastAPI                 github.com/tiangolo/fastapi/releases.atom
  ├── Flask                   github.com/pallets/flask/releases.atom
  ├── Django                  github.com/django/django/releases.atom
  ├── Streamlit               github.com/streamlit/streamlit/releases.atom
  ├── Gradio                  github.com/gradio-app/gradio/releases.atom
  ├── Ray                     github.com/ray-project/ray/releases.atom
  ├── MLflow                  github.com/mlflow/mlflow/releases.atom
  ├── BentoML                 github.com/bentoml/BentoML/releases.atom
  ├── Lightning               github.com/Lightning-AI/pytorch-lightning/releases.atom
  ├── Prefect                 github.com/PrefectHQ/prefect/releases.atom
  └── Airflow                 github.com/apache/airflow/releases.atom

  Agentic Framework Releases (via GitHub Atom):
  ├── LangGraph               github.com/langchain-ai/langgraph/releases.atom
  ├── CrewAI                  github.com/joaomdmoura/crewai/releases.atom
  ├── AutoGen                 github.com/microsoft/autogen/releases.atom
  ├── LlamaIndex              github.com/jerryjliu/llama_index/releases.atom
  ├── Haystack                github.com/deepset-ai/haystack/releases.atom
  ├── OpenDevin               github.com/OpenDevin/OpenDevin/releases.atom
  ├── MetaGPT                 github.com/geekan/MetaGPT/releases.atom
  ├── Flowise                 github.com/FlowiseAI/Flowise/releases.atom
  └── AutoGPT                 github.com/Significant-Gravitas/AutoGPT/releases.atom

  Aggregators and Directories:
  └── AI Top Tools            aitoptools.com/feed

  Medium / Towards Data Science:
  └── TDS AI/ML tag           medium.com/feed/tag/machine-learning


TOOL GROUP 6: URL Fetcher
───────────────────────────
Tool: fetch/url
  What it does:  Fetches any URL and returns clean Markdown content
  Input params:  url, max_chars (default: 3000)
  Returns:       Clean readable text in Markdown format
  Use cases:     Pages without RSS (arXiv Sanity, HF Forums,
                 DataTau, OpenAI community, Anthropic community,
                 Futurepedia, any blog post URL)
  Library used:  httpx (pip install httpx) for HTTP calls
                 markdownify or html2text to convert HTML → Markdown

Tool: fetch/arxiv_sanity
  What it does:  Fetches today's top papers from arxiv-sanity-lite
                 (Karpathy's curation tool, no official API)
  Returns:       Top papers from Karpathy's filtered ArXiv view
  Method:        fetch/url call to the arxiv-sanity-lite RSS/JSON export


TOOL GROUP 7: Kaggle
──────────────────────
Tool: kaggle/datasets
  What it does:  New ML-tagged datasets published recently
  Input params:  tags (["deep-learning", "nlp", "llm"]), days_back
  Returns:       Dataset name, description, size, download count, URL
  Source API:    Official Kaggle API (kaggle.com/docs/api)
  How to get:    pip install kaggle
                 Free account at kaggle.com → Settings → Create API Token
                 Downloads kaggle.json file with username + key

Tool: kaggle/competitions
  What it does:  Active ML competitions with prizes
  Input params:  category, days_since_deadline
  Returns:       Competition title, description, prize, deadline, URL
  Source API:    Same Kaggle API

Tool: kaggle/trending_notebooks
  What it does:  Trending notebooks on Kaggle (community insights)
  Input params:  topic, max_results
  Returns:       Notebook title, author, votes, URL
```

---

## 7. Server 2 — Community Server (Reddit, HN, HuggingFace)

### What This Server Covers

Community signals — what real people are discussing and finding interesting. Reddit, Hacker News, and the HuggingFace ecosystem (models trending, spaces popular, daily papers curated).

```
ai-digest-community-server
─────────────────────────────────────────────────────────────────
GitHub Repo:  github.com/YOUR_USERNAME/ai-digest-community-server
Horizon URL:  https://ai-digest-community.YOUR_NAME.fastmcp.app/mcp
Language:     Python
Framework:    FastMCP 3.0
Auth:         None needed for Reddit (public API)
              None needed for HN (public Algolia API)
              None for HuggingFace public data
```

### Tools Inside This Server

```
TOOL GROUP 1: Reddit
──────────────────────
Important note: These tools use Reddit's PUBLIC JSON endpoint
(reddit.com/r/subreddit/hot.json) — NO OAuth, NO API key,
NO Reddit account needed. This is a public endpoint Reddit
provides for read-only anonymous access.

Tool: reddit/r_machinelearning
  What it does:  Hot posts from r/MachineLearning
  Input params:  min_score (default: 100), max_posts (default: 20)
  Returns:       Post title, score, comment count, URL, text preview
  Source API:    reddit.com/r/MachineLearning/hot.json
                 No auth needed — completely public

Tool: reddit/r_localllama
  What it does:  Hot posts from r/LocalLLaMA
  Input params:  min_score (default: 50), max_posts
  Returns:       Same structure as above
  Source API:    reddit.com/r/LocalLLaMA/hot.json

Tool: reddit/r_deeplearning
  What it does:  Hot posts from r/DeepLearning
  Input params:  min_score, max_posts
  Source API:    reddit.com/r/DeepLearning/hot.json

Tool: reddit/r_datascience
  What it does:  Hot posts from r/DataScience
  Source API:    reddit.com/r/DataScience/hot.json

Tool: reddit/r_ai
  What it does:  Hot posts from r/ArtificialIntelligence
  Source API:    reddit.com/r/ArtificialIntelligence/hot.json

Tool: reddit/search
  What it does:  Search across all 5 subreddits for a keyword
  Input params:  query, subreddit (optional), time_filter, sort
  Returns:       Matching posts sorted by relevance or score
  Source API:    reddit.com/r/subreddit/search.json?q=query

Note on Stack Overflow: Stack Overflow has an official free API
(api.stackexchange.com) that can fetch trending AI/ML/LLM questions.
It is included as an optional tool in this server.

Tool: stackoverflow/trending_ai
  What it does:  Trending questions tagged ai/ml/llm on Stack Overflow
  Input params:  tags (["llm","langchain","fastapi"]), min_score
  Returns:       Question title, tags, answer count, view count, URL
  Source API:    api.stackexchange.com/2.3/questions
                 Completely free, 300 requests/day without key
                 10,000 requests/day with free key from stackapps.com


TOOL GROUP 2: Hacker News
───────────────────────────
Tool: hn/top_ai
  What it does:  Top HN stories related to AI/ML today
  Input params:  min_points (default: 50), max_results, keywords
  Returns:       Story title, URL, points, comment count, HN link, time
  Source API:    hn.algolia.com/api/v1/search (Algolia HN Search API)
                 Completely free, no API key needed
  How to get:    No package needed — direct HTTP call to Algolia HN API
                 Docs: hn.algolia.com/api

Tool: hn/search
  What it does:  Search HN for specific keyword (e.g., "LangGraph")
  Input params:  query, date_range, min_points
  Returns:       Matching stories sorted by points
  Source API:    Same Algolia API with query parameter


TOOL GROUP 3: HuggingFace
───────────────────────────
Note: HuggingFace has TWO options:
  Option A: Use HuggingFace's official MCP server (huggingface.co/mcp)
            → Cloud-hosted by HF, move this to "already cloud-hosted" list
            → Just use their URL, no tools to build

  Option B: Build the tools yourself in this server
            → More control, but requires maintenance
            → Use HF's free public REST API

We recommend Option A (official HF MCP, already cloud-hosted).
But if you want Option B, here are the tools:

Tool: hf/trending_models
  What it does:  Top 20 trending models by downloads today
  Input params:  pipeline_tag (text-generation etc.), max_results
  Returns:       Model ID, downloads, likes, tags, task type, URL
  Source API:    huggingface.co/api/models?sort=downloads&limit=20
                 Free, no auth for public models

Tool: hf/trending_spaces
  What it does:  Top 10 trending Spaces (demo apps) by likes
  Input params:  max_results
  Returns:       Space ID, likes, SDK type, description, URL
  Source API:    huggingface.co/api/spaces?sort=likes&limit=10

Tool: hf/daily_papers
  What it does:  HuggingFace curated daily papers (5-10/day)
  Input params:  date (default: today)
  Returns:       Paper title, abstract, upvotes, URL
  Source API:    huggingface.co/api/daily_papers

Tool: hf/leaderboard
  What it does:  Latest ChatbotArena / LMSYS leaderboard rankings
  Input params:  top_n (default: 20)
  Returns:       Model name, arena score, rank change, organization
  Source API:    huggingface.co API

Tool: hf/datasets
  What it does:  New ML datasets added to the Hub
  Input params:  task_categories, max_results, days_back
  Returns:       Dataset ID, description, downloads, size, URL
  Source API:    huggingface.co/api/datasets
```

---

## 8. Server 3 — Utility Server (Crawl, Memory, Search)

### What This Server Covers

Supporting tools for the pipeline. Not data sources themselves, but tools that help fetch, process, remember, and search.

```
ai-digest-utility-server
─────────────────────────────────────────────────────────────────
GitHub Repo:  github.com/YOUR_USERNAME/ai-digest-utility-server
Horizon URL:  https://ai-digest-utility.YOUR_NAME.fastmcp.app/mcp
Language:     Python
Framework:    FastMCP 3.0
Special:      Crawl4AI needs Playwright browser — this server
              is slightly heavier than the others
```

### Tools Inside This Server

```
TOOL GROUP 1: Crawl4AI — Full JS Browser Rendering
────────────────────────────────────────────────────
Tool: crawl/page
  What it does:  Renders any webpage with full JavaScript execution
                 Returns clean Markdown content
  Why needed:    Some sites (Medium, Futurepedia, some JS-heavy blogs)
                 block simple HTTP fetch requests or require JS to load
                 their content. Simple fetch/url won't work on these.
  Input params:  url, wait_for_selector (optional), max_chars
  Returns:       Full page content as clean Markdown
  Library:       crawl4ai (pip install crawl4ai)
                 GitHub: github.com/unclecode/crawl4ai
                 Uses Playwright browser internally
  Install extra: After pip install, run: playwright install chromium

Tool: crawl/blog_post
  What it does:  Specifically optimized for blog post extraction
                 Removes navigation, ads, footers, returns only article
  Input params:  url
  Returns:       Article title, author, date, full content, tags

Tool: crawl/batch
  What it does:  Crawl a list of URLs in parallel
  Input params:  urls (list), max_concurrent (default: 5)
  Returns:       List of results in same order as input URLs

SOURCES THIS COVERS THAT server-fetch/url CANNOT:
  → Medium / Towards Data Science (JS-heavy)
  → Futurepedia (dynamic content)
  → Apple Machine Learning Research Blog (no RSS)
  → Some community forum pages
  → Any JS-rendered page


TOOL GROUP 2: SearXNG — Private Web Search
─────────────────────────────────────────────
Tool: search/web
  What it does:  Private web search with no API key needed
                 Uses SearXNG metasearch engine
  Why needed:    For Telegram bot's /search command — when users ask
                 about something not yet in the Supabase database
  Input params:  query, categories, max_results
  Returns:       Search results with title, URL, snippet, source
  How it works:  SearXNG is an open-source metasearch engine that
                 aggregates results from Google, Bing, DuckDuckGo
                 and many others without tracking
  GitHub:        github.com/searxng/searxng
  Instance:      You can use a public SearXNG instance (many exist free)
                 OR deploy your own to Horizon (recommended for privacy)
  Public list:   searx.space (list of public free instances)


TOOL GROUP 3: Memory — Persistent Preferences
───────────────────────────────────────────────
Tool: memory/save
  What it does:  Save a user preference, starred item, or note
  Input params:  key, value, category
  Returns:       Confirmation
  Storage:       Simple file or SQLite on Horizon (persistent)
  Use case:      "Remember I always want LangChain items first"
                 "Star this paper for follow-up"

Tool: memory/recall
  What it does:  Retrieve saved preferences or starred items
  Input params:  key or category
  Returns:       Stored value
  Use case:      Bot personalizes output based on your preferences

Tool: memory/list
  What it does:  List all saved memory entries
  Input params:  category filter (optional)
  Returns:       All saved key-value pairs
```

---

## 9. Already Cloud-Hosted MCPs — Zero Setup Needed

These are official MCP servers hosted by the companies themselves. You do not write any code for these. You do not deploy anything. You just add their URL to your GitHub Actions config and call them directly.

### GitHub MCP Server (Official by GitHub)

```
Who hosts it:   GitHub's own servers
URL to use:     https://api.githubcopilot.com/mcp/
Auth:           Your free GitHub account (OAuth)
Cost:           Free with any GitHub account

What it gives you:
  → Search GitHub for trending repos by topic
    Topics to monitor: llm, ai, agents, rag, mcp, langchain,
                       transformers, neural-network, deep-learning
  → Monitor specific repo releases (all 22 framework repos)
  → Get release notes and changelogs
  → Browse issues, PRs, README content
  → Search code across GitHub

Frameworks it monitors releases for:
  Agentic:   LangGraph, CrewAI, AutoGen, LlamaIndex,
             Haystack, OpenDevin, MetaGPT, Flowise, AutoGPT
  Backend:   FastAPI, Flask, Django, Starlette, Streamlit,
             Gradio, Ray, MLflow, BentoML, Lightning,
             Prefect, Airflow, LangServe, Chainlit
  All 22+ repos covered by one MCP server

Documentation: docs.github.com/en/copilot/building-copilot-extensions/
               building-a-copilot-mcp-server
```

### HuggingFace MCP Server (Official by HuggingFace)

```
Who hosts it:   HuggingFace's own servers
URL to use:     https://huggingface.co/mcp
Auth:           Free HuggingFace account login
Cost:           Free

What it gives you:
  → Trending models (by downloads and likes)
  → Trending Spaces (demo apps)
  → Daily Papers (curated by HF team)
  → Datasets Hub (new datasets)
  → Model comparisons
  → Leaderboard data (ChatbotArena)
  → More as HF expands the server

Note: If you build hf/* tools in Server 2 yourself, you do not
need this. Using the official server is easier and lower maintenance.
```

### Supabase MCP Server (Official by Supabase)

```
Who hosts it:   Supabase's own servers
URL to use:     https://mcp.supabase.com/mcp?project_ref=YOUR_REF
Auth:           Your Supabase project reference (from project settings)
Cost:           Free (it's your own database being queried)

What it gives you:
  → Query your digest database using natural language
  → Insert, update, delete records
  → Manage tables and indexes
  → Check logs and errors
  → The Telegram bot can query your DB through this

Documentation: github.com/supabase-community/supabase-mcp
```

### Context7 MCP (Hosted by Context7)

```
Who hosts it:   Context7 (upstash/context7-mcp)
How to use:     npx -y @upstash/context7-mcp (connects to cloud)
Auth:           None required
Cost:           Free tier (generous for personal use)

What it gives you:
  → Up-to-date documentation for any library
  → When your bot receives /docs fastapi or /whatsnew langgraph
    it calls Context7 which returns CURRENT docs, not LLM training data
  → Resolves library name to documentation
  → Returns specific version docs
  → Much better than asking an LLM about docs from its training data

GitHub:        github.com/upstash/context7
```

---

## 10. Complete Master Source Coverage Map

Every single item from your master source document, mapped to the exact tool that covers it:

```
════════════════════════════════════════════════════════════════════════
SECTION 1: RESEARCH & PAPERS
════════════════════════════════════════════════════════════════════════
Source                      Tool                    Server        Cost
────────────────────────────────────────────────────────────────────────
ArXiv cs.LG, cs.AI, stat.ML  arxiv/search            Research-S1   FREE
ArXiv cs.CL, cs.CV           arxiv/get_recent        Research-S1   FREE
arXiv Sanity (Karpathy)      fetch/url               Research-S1   FREE
                             (fetches arxiv-sanity-lite.org)
Semantic Scholar AI feed     scholar/search          Research-S1   FREE
Semantic Scholar citations   scholar/trending_cites  Research-S1   FREE
Papers With Code trending    papers/trending         Research-S1   FREE
Papers With Code SOTA        papers/sota             Research-S1   FREE
Papers With Code datasets    papers/datasets         Research-S1   FREE
NeurIPS proceedings          openreview/neurips      Research-S1   FREE
ICML proceedings             openreview/icml         Research-S1   FREE
ICLR proceedings             openreview/iclr         Research-S1   FREE
CVPR proceedings             openreview/cvpr         Research-S1   FREE
ACL proceedings              openreview/acl          Research-S1   FREE
EMNLP proceedings            openreview/acl          Research-S1   FREE
OpenReview API               (all openreview/* tools) Research-S1  FREE
Academic datasets (Kaggle)   kaggle/datasets         Research-S1   FREE

════════════════════════════════════════════════════════════════════════
SECTION 2: NEWSLETTERS & BLOGS
════════════════════════════════════════════════════════════════════════
Source                      Tool                    Server        Cost
────────────────────────────────────────────────────────────────────────
The Batch (deeplearning.ai)  rss/fetch_all           Research-S1   FREE
Import AI (Jack Clark)       rss/fetch_all           Research-S1   FREE
BAIR Blog (UC Berkeley)      rss/fetch_all           Research-S1   FREE
Gradient Flow (Ben Lorica)   rss/fetch_all           Research-S1   FREE
Yannic Kilcher's summaries   ⚠️ YouTube RSS          Research-S1   FREE
                             (youtube.com/@YannicKilcher RSS exists)
HuggingFace Blog             rss/fetch_all           Research-S1   FREE
W&B Blog                     rss/fetch_all           Research-S1   FREE
AWS ML Blog                  rss/fetch_all           Research-S1   FREE
Google Cloud AI Blog         rss/fetch_all           Research-S1   FREE
Microsoft Azure AI Blog      rss/fetch_all           Research-S1   FREE
Medium / Towards Data Science rss/fetch_all +        Research-S1   FREE
                              crawl/page (for JS)    Utility-S3
KDnuggets News               rss/fetch_all           Research-S1   FREE

════════════════════════════════════════════════════════════════════════
SECTION 3: CODE, TOOLS & FRAMEWORKS
════════════════════════════════════════════════════════════════════════
Source                      Tool                    Server        Cost
────────────────────────────────────────────────────────────────────────
HuggingFace Model Hub        hf/trending_models      Community-S2  FREE
                             OR HF official MCP      Cloud MCP     FREE
HuggingFace Spaces           hf/trending_spaces      Community-S2  FREE
Papers With Code SOTA        papers/sota             Research-S1   FREE
PyPI trending packages       rss/fetch_feed          Research-S1   FREE
                             (pypi.org/rss/updates.xml)
Conda new ML packages        rss/fetch_feed          Research-S1   FREE
                             (anaconda.org RSS)
Kaggle Datasets              kaggle/datasets         Research-S1   FREE
Kaggle Competitions          kaggle/competitions     Research-S1   FREE
GitHub Trending AI/ML        github-mcp (search)     Cloud MCP     FREE
GitHub Releases (frameworks) github-mcp (releases)   Cloud MCP     FREE
FastAPI releases             rss/fetch_all           Research-S1   FREE
                             (GitHub .atom feed)
Flask releases               rss/fetch_all           Research-S1   FREE
Django releases              rss/fetch_all           Research-S1   FREE
Lightning AI releases        rss/fetch_all           Research-S1   FREE

════════════════════════════════════════════════════════════════════════
SECTION 4: AGENTIC & DEVELOPER FRAMEWORKS
════════════════════════════════════════════════════════════════════════
Source                      Tool                    Server        Cost
────────────────────────────────────────────────────────────────────────
LangChain Blog               rss/fetch_all           Research-S1   FREE
LlamaIndex Blog              rss/fetch_all           Research-S1   FREE
CrewAI GitHub releases       rss/fetch_all +         Research-S1   FREE
                             github-mcp              Cloud MCP     FREE
MCP Blog                     rss/fetch_all           Research-S1   FREE
AutoGen (Microsoft)          rss/fetch_all +         Research-S1   FREE
                             github-mcp              Cloud MCP     FREE
Haystack (Deepset)           rss/fetch_all +         Research-S1   FREE
                             github-mcp              Cloud MCP     FREE
Flowise                      rss/fetch_all +         Research-S1   FREE
                             github-mcp              Cloud MCP     FREE
AutoGPT / GPT Engineer       rss/fetch_all +         Research-S1   FREE
                             github-mcp              Cloud MCP     FREE
OpenDevin / MetaGPT          github-mcp              Cloud MCP     FREE

════════════════════════════════════════════════════════════════════════
SECTION 5: COMMUNITY & DISCUSSIONS
════════════════════════════════════════════════════════════════════════
Source                      Tool                    Server        Cost
────────────────────────────────────────────────────────────────────────
r/MachineLearning            reddit/r_machinelearning Community-S2  FREE
r/DeepLearning               reddit/r_deeplearning   Community-S2  FREE
r/LocalLLaMA                 reddit/r_localllama     Community-S2  FREE
r/DataScience                reddit/r_datascience    Community-S2  FREE
r/ArtificialIntelligence     reddit/r_ai             Community-S2  FREE
Hacker News AI stories       hn/top_ai               Community-S2  FREE
Stack Overflow AI trends     stackoverflow/trending  Community-S2  FREE
HuggingFace Forums           fetch/url               Research-S1   FREE
OpenAI community posts       fetch/url               Research-S1   FREE
Anthropic community posts    fetch/url               Research-S1   FREE
LinkedIn posts               ❌ NO API AVAILABLE     SKIP          —
                             (ToS violation, no public API)

════════════════════════════════════════════════════════════════════════
SECTION 6: VIDEOS & PODCASTS
════════════════════════════════════════════════════════════════════════
Source                      Tool                    Server        Cost
────────────────────────────────────────────────────────────────────────
YouTube channels (all)       rss/fetch_feed          Research-S1   FREE
                             YouTube provides RSS for every channel:
                             youtube.com/feeds/videos.xml?channel_id=ID
                             Gives titles, descriptions, upload dates
                             (No video content, just metadata)
Yannic Kilcher YouTube       rss/fetch_feed (YT RSS) Research-S1   FREE
Two Minute Papers            rss/fetch_feed (YT RSS) Research-S1   FREE
Sentdex                      rss/fetch_feed (YT RSS) Research-S1   FREE
CodeEmporium                 rss/fetch_feed (YT RSS) Research-S1   FREE
HuggingFace YouTube          rss/fetch_feed (YT RSS) Research-S1   FREE
OpenAI YouTube               rss/fetch_feed (YT RSS) Research-S1   FREE
Podcasts (all)               rss/fetch_feed          Research-S1   FREE
                             All podcasts have RSS feeds.
                             Gives episode title, description, date.
Gradient Dissent (W&B)       rss/fetch_feed          Research-S1   FREE
Lex Fridman Podcast          rss/fetch_feed          Research-S1   FREE
ML Street Talk               rss/fetch_feed          Research-S1   FREE
TWiML AI Podcast             rss/fetch_feed          Research-S1   FREE
Practical AI Podcast         rss/fetch_feed          Research-S1   FREE

════════════════════════════════════════════════════════════════════════
SECTION 7: COMPANY & RESEARCH BLOGS
════════════════════════════════════════════════════════════════════════
All have RSS feeds → covered by rss/fetch_all in Research-S1   FREE

Apple ML Research Blog       crawl/page              Utility-S3    FREE
(no RSS — needs JS crawling)

════════════════════════════════════════════════════════════════════════
SECTION 8: AGGREGATORS & DIRECTORIES
════════════════════════════════════════════════════════════════════════
Source                      Tool                    Server        Cost
────────────────────────────────────────────────────────────────────────
AI Top Tools                 rss/fetch_all           Research-S1   FREE
Futurepedia                  crawl/page              Utility-S3    FREE
AI Papers Daily (Telegram)   fetch/url               Research-S1   ⚠️PARTIAL
                             (Telegram channels not easily fetchable)
HuggingFace Daily Papers     hf/daily_papers         Community-S2  FREE
DataTau                      fetch/url               Research-S1   FREE
arXiv Digest channels        rss/fetch_feed          Research-S1   FREE
                             (Substack newsletters have RSS)

════════════════════════════════════════════════════════════════════════
SECTION 9: BACKEND & INFRA ECOSYSTEM
════════════════════════════════════════════════════════════════════════
All GitHub releases covered by github-mcp (Cloud MCP) or
rss/fetch_all (GitHub Atom feeds in Research-S1)        FREE

LangServe / Chainlit         rss/fetch_all +         Research-S1   FREE
                             github-mcp              Cloud MCP     FREE

════════════════════════════════════════════════════════════════════════
SECTION 10: ADDITIONAL / OPTIONAL
════════════════════════════════════════════════════════════════════════
Source                      Tool                    Server        Cost
────────────────────────────────────────────────────────────────────────
HF Datasets Hub              hf/datasets             Community-S2  FREE
HF Leaderboard               hf/leaderboard          Community-S2  FREE
Kaggle Trending Notebooks    kaggle/trending_ntbks   Research-S1   FREE
Semantic Scholar citations   scholar/trending_cites  Research-S1   FREE
Modal Labs Blog              rss/fetch_all           Research-S1   FREE
Replicate Blog               rss/fetch_all           Research-S1   FREE
Perplexity AI Blog           rss/fetch_all           Research-S1   FREE
Together AI Blog             rss/fetch_all           Research-S1   FREE
a16z AI Blog                 rss/fetch_all           Research-S1   FREE
Sequoia Generative AI Blog   rss/fetch_all           Research-S1   FREE
AI Snakepit (ethics)         rss/fetch_feed          Research-S1   FREE
Gradient Institute           rss/fetch_feed          Research-S1   FREE
════════════════════════════════════════════════════════════════════════

OVERALL COVERAGE: 98% of all sources ✅
UNCOVERABLE:  LinkedIn (ToS), Telegram private channels
COST: $0
```

---

## 11. How to Deploy to Prefect Horizon (Step by Step)

This section explains the full deployment process for each of your 3 servers. The process is identical for all three. You do it once per server.

### Prerequisites Before Deploying

```
1. GitHub account (free at github.com)
2. Prefect Horizon account (free at horizon.prefect.io)
   → Sign in with your GitHub account (no separate registration)
3. FastMCP installed locally for testing
   → pip install fastmcp
4. Python 3.11+ installed on your PC (for local development/testing only)
   → Once deployed, PC is not needed
```

### Step-by-Step Process

```
PHASE 1 — LOCAL DEVELOPMENT
─────────────────────────────────────────────────────────────────

STEP 1: Create a new folder for the server
  Name it: ai-digest-research-server
  (or community-server, or utility-server)

STEP 2: Create the main Python file
  Name it: main.py
  This file will contain:
    - One FastMCP server instance at the top
    - One Python function per tool
    - @mcp.tool decorator above each function
    - A docstring explaining each tool (this is what the pipeline reads)

STEP 3: Import the libraries your tools need
  All library imports go at the top of main.py
  Common imports for Research Server:
    - feedparser (for RSS parsing)
    - arxiv (official ArXiv Python library)
    - httpx (for async HTTP requests to REST APIs)
    - html2text or markdownify (for HTML → Markdown conversion)
  Common for Community Server:
    - httpx (for Reddit JSON and HN Algolia calls)
  Common for Utility Server:
    - crawl4ai (for JS browser rendering)

STEP 4: Create requirements.txt
  List every Python library your server needs, one per line
  Example for Research Server:
    feedparser
    arxiv
    httpx
    html2text
    kaggle
    fastmcp
  Horizon reads this file automatically and installs everything

STEP 5: Create config/rss_sources.yaml (Research Server only)
  This YAML file lists all 35+ RSS feed URLs
  Organized by category: company_blogs, newsletters, framework_releases
  The rss/fetch_all tool reads this file to know which feeds to fetch

STEP 6: Test locally with FastMCP Inspector
  Run: fastmcp dev main.py
  Opens a browser at localhost:6274
  You can click on each tool, enter parameters, and see the output
  Test every single tool before deploying
  Fix any errors before moving to Phase 2


PHASE 2 — GITHUB REPOSITORY
──────────────────────────────────────────────────────────────────

STEP 7: Create a new GitHub repository
  Go to github.com → New repository
  Name: ai-digest-research-server (or community/utility)
  Set to Private (recommended — hides your API keys in config)
  Initialize with README

STEP 8: Push your code
  Upload these files to the repo:
    main.py
    requirements.txt
    config/rss_sources.yaml (Research Server only)
    .env.example (template listing needed env vars, no actual values)
  DO NOT commit .env with actual API keys
  Use GitHub Secrets for real keys (added in Repo Settings → Secrets)

STEP 9: Add secrets to GitHub repository
  Go to: Your repo → Settings → Secrets and Variables → Actions
  Add each secret your server needs:
    Research Server:  KAGGLE_USERNAME, KAGGLE_KEY, SEMANTIC_SCHOLAR_KEY
    Community Server: No secrets needed (all public APIs)
    Utility Server:   No secrets needed


PHASE 3 — PREFECT HORIZON DEPLOYMENT
──────────────────────────────────────────────────────────────────

STEP 10: Go to horizon.prefect.io
  Sign in with your GitHub account
  (same account where your repos live)

STEP 11: Click "Deploy New Server"
  Horizon shows all your GitHub repos
  Select: ai-digest-research-server
  (repeat for community and utility servers)

STEP 12: Configure the deployment
  Fill in these fields:
    Server name:  ai-digest-research (becomes part of your URL)
    Description:  "Research papers, RSS feeds, blogs for AI digest"
    Entrypoint:   main.py:mcp
                  (tells Horizon which file and which object to run)
    Python version: 3.11 (recommended)
    Authentication: OFF for personal use (you control access via token)

STEP 13: Set environment variables in Horizon
  Horizon has a Secrets/Variables section in each deployment
  Add your real API keys here:
    KAGGLE_USERNAME = your_kaggle_username
    KAGGLE_KEY = your_kaggle_api_key
    SEMANTIC_SCHOLAR_KEY = your_optional_key
  These are injected at runtime — never exposed in code

STEP 14: Click Deploy
  Horizon:
    → Clones your GitHub repo
    → Installs from requirements.txt
    → Starts your FastMCP server
    → Gives you a live HTTPS URL
  Takes approximately 60 seconds

STEP 15: Copy your server URL
  It will look like:
    https://ai-digest-research.YOUR_HORIZON_USERNAME.fastmcp.app/mcp
  Save this URL — you'll put it in your GitHub Actions pipeline config

STEP 16: Test the live URL
  In Horizon, click "ChatMCP" to open the test interface
  Try calling each tool with real parameters
  Verify results look correct
  If something's wrong, fix it in your local code and push to GitHub
  Horizon auto-redeploys within seconds of every push

REPEAT STEPS 10-16 FOR EACH OF THE 3 SERVERS
```

### What Horizon Gives You Automatically (No Extra Work)

```
CI/CD:        Every git push to your repo → Horizon auto-redeploys
              Branch previews for testing changes without affecting prod
Monitoring:   Real-time logs, error tracking, call history
Scaling:      Horizon handles traffic spikes automatically
Security:     OAuth 2.1 built in (optional for personal use)
Rollbacks:    One click to revert to any previous version
Uptime:       24/7 — not dependent on your PC at all
```

---

## 12. GitHub Actions — The Free 24/7 Cron Trigger

GitHub Actions is the cloud scheduler that wakes up every day at 7 AM IST and runs your pipeline. It runs on GitHub's own cloud servers — your PC does not need to be running.

### How It Works

```
YOUR GITHUB REPO: ai-digest-pipeline
  ↓
Contains file: .github/workflows/daily_digest.yml
  ↓
GitHub reads this file and schedules it
  ↓
Every day at 1:30 AM UTC (7:00 AM IST):
  GitHub spins up an Ubuntu container on their servers
  The container runs for ~3-5 minutes
  The container calls your Horizon MCP servers
  The container calls Gemini API
  The container saves to Supabase
  The container sends notifications
  The container shuts down automatically
  ↓
You wake up to a complete digest on all channels
```

### What the Workflow File Does (Plain English)

```
.github/workflows/daily_digest.yml — what it defines:
────────────────────────────────────────────────────────

TRIGGER:
  Schedule: Run at 1:30 AM UTC every day (7:00 AM IST)
  Manual: Also allow clicking "Run Workflow" button in GitHub UI
          (useful for testing without waiting for 7 AM)

STEPS:
  1. Check out your repository code
  2. Set up Python 3.11 environment
  3. Cache pip dependencies (speeds up future runs)
  4. Install Python packages from requirements.txt
  5. Run the main pipeline script (orchestrator.py)
     with all environment variables injected from GitHub Secrets

SECRETS NEEDED (add to GitHub repo → Settings → Secrets):
  RESEARCH_SERVER_URL     → your Horizon research server URL
  COMMUNITY_SERVER_URL    → your Horizon community server URL
  UTILITY_SERVER_URL      → your Horizon utility server URL
  GITHUB_MCP_URL          → api.githubcopilot.com/mcp/
  GITHUB_TOKEN            → your GitHub PAT for GitHub MCP auth
  SUPABASE_MCP_URL        → mcp.supabase.com URL with project ref
  SUPABASE_KEY            → your Supabase service role key
  GEMINI_API_KEY          → your Gemini Flash 2.0 API key
  TELEGRAM_BOT_TOKEN      → your Telegram bot token
  TELEGRAM_CHAT_ID        → your personal Telegram chat ID
  DISCORD_WEBHOOK_URL     → your Discord webhook URL
  RESEND_API_KEY          → your Resend email API key
  EMAIL_TO                → your personal email address

FREE USAGE CHECK:
  Pipeline runs ~4 minutes per day
  4 min × 30 days = 120 minutes/month
  GitHub free tier = 2,000 minutes/month
  Budget used: 6% — extremely safe
```

---

## 13. Complete Pipeline Flow (PC Off, Everything Automated)

This is the full minute-by-minute flow of what happens every morning:

```
7:00:00 AM IST — GitHub Actions wakes up on GitHub's cloud
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7:00:05 AM — GitHub Actions container starts
  → Checks out your pipeline code
  → Installs dependencies (fast due to caching)
  → Reads all MCP server URLs from secrets

7:00:30 AM — PARALLEL DATA COLLECTION BEGINS
  All 4 MCP servers called simultaneously:

  ┌─────────────────────────────────────────────────────┐
  │ Research Server (Horizon)                           │
  │   → arxiv/get_recent(cs.AI, days=1)     ~50 papers  │
  │   → arxiv/get_recent(cs.LG, days=1)     ~50 papers  │
  │   → papers/trending(max=20)             ~20 papers  │
  │   → scholar/trending_cites              ~15 papers  │
  │   → openreview/neurips                  ~10 papers  │
  │   → rss/fetch_all                       ~150 blogs  │
  │   → kaggle/datasets                     ~10 items   │
  │   Total: ~305 items                                 │
  └─────────────────────────────────────────────────────┘
  ┌─────────────────────────────────────────────────────┐
  │ Community Server (Horizon)                          │
  │   → reddit/r_machinelearning            ~20 posts   │
  │   → reddit/r_localllama                 ~20 posts   │
  │   → reddit/r_deeplearning               ~15 posts   │
  │   → reddit/r_datascience                ~15 posts   │
  │   → reddit/r_ai                         ~15 posts   │
  │   → hn/top_ai                           ~20 stories │
  │   → hf/trending_models                  ~20 models  │
  │   → hf/daily_papers                     ~8 papers   │
  │   → hf/trending_spaces                  ~10 spaces  │
  │   Total: ~143 items                                 │
  └─────────────────────────────────────────────────────┘
  ┌─────────────────────────────────────────────────────┐
  │ GitHub MCP (GitHub's cloud)                         │
  │   → search repos by topic (llm, ai, agents...)      │
  │   → check all 22 framework repos for new releases   │
  │   Total: ~40 items                                  │
  └─────────────────────────────────────────────────────┘
  ┌─────────────────────────────────────────────────────┐
  │ Utility Server (Horizon)                            │
  │   → crawl/page for JS-heavy blogs                   │
  │   → Used selectively, not every run                 │
  │   Total: ~10-15 items                               │
  └─────────────────────────────────────────────────────┘

  TOTAL RAW ITEMS COLLECTED: ~490-500 items

7:01:30 AM — DEDUPLICATION
  Input:  ~500 raw items
  Stage 1 URL dedup:    removes 120 exact URL duplicates
  Stage 2 Fuzzy titles: removes 120 near-duplicates
  Output: ~250 unique items

7:01:35 AM — GEMINI FLASH 2.0 CALL
  Single batch request to Gemini API
  All 250 items in one JSON payload
  Gemini processes everything simultaneously
  Returns for each item:
    → 2-sentence technical summary
    → Relevance score 1-10
    → is_breaking flag
    → Tags array
    → Framework mentions array
  Token usage: ~50,000 tokens (5% of 1M limit)
  API calls used: 1 (of 1,500 free daily limit)

7:02:30 AM — SUPABASE SAVE
  Items sorted by relevance score (highest first)
  Saved to 3 tables:
    news_items:    ~160 blog + community items
    papers:        ~55 research papers
    github_repos:  ~40 repos and releases
  digest_runs table: 1 audit log entry

7:02:45 AM — PARALLEL PUBLISHING
  All 3 channels publish simultaneously:

  📧 Resend Email:
    Top 10 news items
    Top 5 framework updates
    Top 3 research papers
    Sent to your email

  🤖 Telegram Bot:
    Breaking news section (if any)
    Framework updates section
    Top stories section
    GitHub trending section
    Research papers section

  🎮 Discord Webhook:
    Color-coded embeds per category
    Breaking news in red
    Agents in green, Backend in blue

7:03:30 AM — DONE
  Dashboard on Vercel auto-shows latest data
  (reads Supabase directly — no action needed)

  YOUR PC = OFF THE ENTIRE TIME ✅
  YOU WAKE UP TO COMPLETE DIGEST ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total pipeline time: ~3.5 minutes
Total cost: $0
```

---

## 14. Project Folder Structure — All 3 Repos

```
REPO 1: ai-digest-research-server/
│
├── main.py                          ← FastMCP server with ALL tools
│                                       One FastMCP instance at top
│                                       11 tool functions below it
│                                       Each function = one @mcp.tool
│
├── requirements.txt                 ← Python dependencies
│                                       feedparser, arxiv, httpx,
│                                       html2text, kaggle, fastmcp
│
├── config/
│   ├── rss_sources.yaml             ← ALL 35+ RSS feed URLs
│   │                                   Organized by category
│   │                                   Loaded by rss/fetch_all tool
│   │
│   └── conferences.yaml             ← OpenReview venue IDs
│                                       NeurIPS, ICML, ICLR, ACL, CVPR
│
├── .env.example                     ← Template for needed keys
│                                       KAGGLE_USERNAME=
│                                       KAGGLE_KEY=
│                                       SEMANTIC_SCHOLAR_KEY=
│
└── README.md                        ← Documentation for this server
                                        Tool list, usage examples


REPO 2: ai-digest-community-server/
│
├── main.py                          ← FastMCP server with community tools
│                                       Reddit, HN, HuggingFace tools
│                                       StackOverflow optional tool
│
├── requirements.txt                 ← httpx, fastmcp
│                                       (No special auth libraries needed)
│
└── README.md


REPO 3: ai-digest-utility-server/
│
├── main.py                          ← FastMCP server with utility tools
│                                       crawl4ai, SearXNG, memory tools
│
├── requirements.txt                 ← crawl4ai, fastmcp, sqlitedict
│                                       (crawl4ai installs playwright)
│
├── searxng_instance.txt             ← URL of your chosen SearXNG instance
│                                       (public instance or your own)
│
└── README.md


REPO 4: ai-digest-pipeline/          ← THE MAIN PIPELINE REPO
│                                       This is what GitHub Actions runs
│
├── .github/
│   └── workflows/
│       └── daily_digest.yml         ← Cron schedule + workflow steps
│
├── pipeline/
│   ├── orchestrator.py              ← Calls all 7 MCP server URLs
│   │                                   Collects all items
│   │                                   Runs deduplication
│   │                                   Calls Gemini
│   │                                   Calls Supabase
│   │                                   Triggers publishers
│   │
│   ├── deduplicator.py              ← URL hash + fuzzy title matching
│   └── gemini_client.py             ← Batch call to Gemini Flash 2.0
│
├── publishers/
│   ├── telegram_publisher.py        ← Sends to Telegram bot
│   ├── discord_publisher.py         ← Sends Discord webhook embeds
│   └── email_publisher.py           ← Sends email via Resend
│
├── mcp_config.py                    ← All 7 MCP server URLs
│                                       Loaded from environment variables
│
├── requirements.txt                 ← fastmcp, httpx, resend, etc.
│
└── .env.example                     ← All required secret names
```

---

## 15. How Each Tool Works — Source by Source

### RSS and Blog Feeds — How feedparser Works

```
HOW feedparser WORKS:
──────────────────────────────────────────────────────
feedparser is a Python library that reads RSS/Atom feed URLs
and converts them into Python objects you can work with.

You give it a URL like:
  https://openai.com/blog/rss/

It returns a structured object with:
  feed.title       → "OpenAI Blog"
  feed.entries     → list of articles
  entry.title      → "OpenAI releases o3"
  entry.link       → "https://openai.com/blog/o3"
  entry.summary    → first 500 characters of article
  entry.published  → "2026-02-23T08:00:00Z"

Your rss/fetch_all tool:
  1. Reads rss_sources.yaml to get all 35+ URLs
  2. Calls feedparser on ALL of them simultaneously (async)
  3. Takes the 10 most recent entries from each feed
  4. Returns everything as a flat list of ScrapedItem objects

Why GitHub release Atom feeds work perfectly:
  github.com/tiangolo/fastapi/releases.atom
  ↓
  feedparser reads it
  ↓
  entry.title    → "0.111.0"
  entry.link     → release URL
  entry.summary  → release notes text
  entry.published → exact release datetime
  ↓
  PERFECT data for framework release tracking
```

### ArXiv Tool — How the arxiv Library Works

```
HOW arxiv Python Library WORKS:
────────────────────────────────────────────────────────
The arxiv Python library (pip install arxiv) wraps the
official ArXiv API in a clean Python interface.

Official ArXiv API documentation: info.arxiv.org/help/api/index.html
Python library docs:              lukasschwab.me/arxiv.py/

Your tool:
  1. Receives: category="cs.AI", days_back=1, max_results=50
  2. Calls ArXiv API with:
     → search_query: "cat:cs.AI"
     → sortBy: submittedDate
     → dateFrom: yesterday's date
  3. Returns each paper with:
     → title, authors (list), abstract, arxiv_url, pdf_url
     → submitted date, primary category, all categories
  4. All completely free, no authentication, no rate limits
```

### Reddit Tools — No OAuth Needed

```
HOW REDDIT PUBLIC JSON API WORKS:
────────────────────────────────────────────────────────
Reddit provides a completely open JSON endpoint for every subreddit.
No authentication. No API key. No OAuth. Just a direct HTTP GET.

URL pattern:
  reddit.com/r/SUBREDDIT_NAME/hot.json?limit=25

Returns JSON with:
  data.children → list of posts
  Each post:
    data.title       → post headline
    data.url         → linked URL (or reddit URL for text posts)
    data.score       → upvote count
    data.permalink   → reddit.com/r/.../comments/...
    data.selftext    → text content (if it's a text post)
    data.num_comments → comment count
    data.created_utc → unix timestamp

Your tool:
  1. Receives: subreddit="MachineLearning", min_score=100, max=20
  2. Fetches hot.json with httpx
  3. Filters posts where score >= min_score
  4. Returns structured list of relevant posts

Rate limits: None for this public endpoint (be reasonable — 1 call/min is fine)
```

### HuggingFace API — How it Works

```
HOW HUGGINGFACE PUBLIC REST API WORKS:
──────────────────────────────────────────────────────────
HuggingFace exposes a public REST API at huggingface.co/api/
No authentication needed for public models and spaces.

Key endpoints:
  Trending models: GET /api/models?sort=downloads&limit=20
  Trending spaces: GET /api/spaces?sort=likes&limit=10
  Daily papers:    GET /api/daily_papers?date=2026-02-23

Each endpoint returns JSON arrays with structured data.
Your tools make direct HTTP GET calls using httpx.
```

### GitHub MCP (Cloud) — How it Works

```
HOW GITHUB MCP SERVER WORKS:
──────────────────────────────────────────────────────────
The official GitHub MCP server is hosted at:
  https://api.githubcopilot.com/mcp/

Authentication:
  You create a Personal Access Token (PAT) at:
  github.com/settings/tokens → Fine-grained tokens → New token
  Permission needed: "Contents" read (for releases)
                     "Metadata" read (for repos)

The token goes in your GitHub Actions secrets as GITHUB_TOKEN.
When GitHub Actions calls the GitHub MCP server, it passes this
token in the Authorization header.

Tools available:
  search_repositories  → find trending repos by topic
  list_releases        → get all releases for a repo
  get_release          → get details of a specific release
  read_file            → read any file from any public repo
  search_code          → search code across GitHub

Your pipeline calls these tools for:
  → github.search_repositories(topic="llm", sort="stars", days=1)
  → github.list_releases(repo="langchain-ai/langgraph", since=yesterday)
  → Repeat for all 22 monitored framework repos
```

---

## 16. Detailed Sample Outputs

### What the Pipeline Produces Each Morning

```
DAILY RUN SUMMARY — February 23, 2026
═══════════════════════════════════════════════════════════════
Run Start:    7:00:03 AM IST
Run End:      7:03:47 AM IST
Duration:     3 minutes 44 seconds

DATA COLLECTION:
  Research Server (Horizon):   302 items  ✅ Success
    → ArXiv cs.AI:              48 papers
    → ArXiv cs.LG:              52 papers
    → ArXiv stat.ML:            31 papers
    → Papers With Code:         20 papers
    → Semantic Scholar:         17 papers
    → OpenReview:               14 papers
    → RSS feeds (35 sources): 110 items
    → Kaggle:                    10 items

  Community Server (Horizon):  138 items  ✅ Success
    → r/MachineLearning:         18 posts
    → r/LocalLLaMA:              22 posts
    → r/DeepLearning:            14 posts
    → r/DataScience:             12 posts
    → r/ArtificialIntelligence:  16 posts
    → Hacker News:               21 stories
    → HuggingFace models:        20 items
    → HuggingFace papers:         8 items
    → HuggingFace spaces:         7 items

  GitHub MCP (Cloud):           43 items  ✅ Success
    → Trending repos:            38 repos
    → Framework releases:         5 releases
      (LangGraph v0.2.1, FastAPI 0.111.0,
       CrewAI v0.28.0, Haystack 2.5.0, MLflow 2.15.0)

  TOTAL RAW:                   483 items

DEDUPLICATION:
  After URL dedup:             361 items  (122 removed)
  After fuzzy title dedup:     238 items  (123 removed)
  Total removed:               245 duplicates (51%)

GEMINI PROCESSING:
  Items sent:                  238
  Tokens used:                 ~47,200 (4.7% of daily limit)
  API calls used:              1 (of 1,500 free)
  Breaking items flagged:      4
  Score 9-10:                  31 items
  Score 7-8:                   67 items
  Score 5-6:                   89 items
  Score 1-4:                   51 items

STORAGE:
  news_items saved:            148
  papers saved:                 53
  github_repos saved:           37
  Supabase rows added:         238

PUBLISHING:
  📧 Email:     ✅ Sent to your@email.com
  🤖 Telegram:  ✅ 5 messages sent to chat ID
  🎮 Discord:   ✅ 4 webhook calls (38 embeds)
  🖥️ Dashboard: ✅ Live on Vercel (auto-updated)

STATUS: SUCCESS ✅
═══════════════════════════════════════════════════════════════
```

### Sample Telegram Output

```
MESSAGE 1 OF 5 — Breaking News
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚨 BREAKING AI NEWS — Feb 23, 2026

🔴 [LangGraph v0.2.1 Released](https://github.com/...)
   Score: 10/10
   LangGraph 0.2.1 introduces native streaming API for
   real-time agent state updates and a checkpoint system
   enabling resumable multi-step workflows.

🔴 [Google Releases Gemini 2.5 Ultra](https://blog.google/...)
   Score: 10/10
   Gemini 2.5 Ultra achieves state-of-the-art on 12 of
   15 benchmarks with a 2M token context window and
   native tool use improvements.


MESSAGE 2 OF 5 — Framework Updates
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 FRAMEWORK UPDATES TODAY

🤖 [LangGraph v0.2.1](https://github.com/...) ★ 10/10
   Streaming API + checkpoint system for resumable agents.
   Tags: Agents · LLM · OpenSource

🤖 [CrewAI v0.28.0](https://github.com/...) ★ 9/10
   New memory module with cross-crew shared context.
   Tags: Agents · MultiAgent

⚙️ [FastAPI 0.111.0](https://github.com/...) ★ 9/10
   WebSocket improvements + new dependency injection patterns.
   Tags: Backend · OpenSource

⚙️ [MLflow 2.15.0](https://github.com/...) ★ 8/10
   LLM evaluation framework expanded with new metrics.
   Tags: MLOps · Evaluation


MESSAGE 3 OF 5 — Top AI/ML News
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📰 TOP AI/ML NEWS TODAY

• [Anthropic publishes interpretability results](https://...)
  Score: 9/10 | Tags: Research · Safety
  Anthropic's sparse autoencoder work reveals internal
  representations for emotion and planning in Claude.

• [OpenAI open-sources reasoning trace dataset](https://...)
  Score: 8/10 | Tags: LLM · Dataset · OpenSource
  500k reasoning traces released for fine-tuning
  chain-of-thought reasoning in smaller models.

• [DeepMind AlphaFold 3 used in drug discovery](https://...)
  Score: 8/10 | Tags: Research · Biology · LLM
  First peer-reviewed drug candidate designed using
  AlphaFold 3 protein structure predictions.

[+ 7 more stories in dashboard]
🔗 https://your-dashboard.vercel.app


MESSAGE 4 OF 5 — GitHub Trending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💻 TRENDING GITHUB REPOS

⭐ [microsoft/phi-4-mini](https://github.com/...)
   New 4B parameter model optimized for edge deployment.
   Python | ⭐ 2.4k today | Tags: llm, inference

⭐ [unslothai/unsloth](https://github.com/...)
   Fine-tuning now 5x faster with 70% less VRAM.
   Python | ⭐ 1.1k today | Tags: fine-tuning, llm

⭐ [modal-labs/quillman](https://github.com/...)
   Real-time voice AI pipeline using Modal + Whisper.
   Python | ⭐ 890 today | Tags: voice, agents


MESSAGE 5 OF 5 — Research Papers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 TOP RESEARCH PAPERS

🔬 [Scaling Laws for Agent Tasks](https://arxiv.org/...)
   ArXiv cs.AI | Score: 9/10
   Establishes empirical scaling laws for multi-step
   agentic tasks, showing emergent tool use at 13B params.

🔬 [MegaScale-Infer: Serving 1T Parameters](https://arxiv.org/...)
   ArXiv cs.LG | Score: 9/10
   Distributed inference system for trillion-parameter
   models using tensor parallelism on commodity hardware.

🔬 [RLHF Without Human Feedback](https://arxiv.org/...)
   NeurIPS 2025 | Score: 8/10
   Self-play method generates synthetic preference data
   matching human RLHF quality at 100x lower cost.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Sample Discord Embed (Visual Description)

```
┌──────────────────────────────────────────────────────────┐
│ ████ GREEN LEFT BORDER (AgentFramework)                   │
│                                                          │
│  🤖 LangGraph v0.2.1 Released                           │
│     ↑ (clickable title → GitHub releases page)          │
│                                                          │
│  LangGraph 0.2.1 introduces a native streaming API      │
│  for real-time agent state updates and a checkpoint      │
│  system enabling resumable multi-step workflows.         │
│                                                          │
│  Category: AgentFramework │ Score: 10/10 │ 🔴 BREAKING  │
│  Tags: Agents · LLM · OpenSource                        │
│  ─────────────────────────────────────────────────────  │
│  langchain_ai/langgraph  •  Feb 23, 2026  •  GitHub     │
└──────────────────────────────────────────────────────────┘

COLOR CODE:
  🟢 Green   = AgentFramework items
  🔵 Blue    = BackendFramework items
  🟠 Orange  = Research papers
  🔴 Red     = Breaking news / ModelRelease
  🟣 Purple  = Tools
  🟡 Yellow  = Newsletter items
  🩵 Cyan    = Community posts (Reddit/HN)
```

### Sample Email Structure

```
EMAIL SUBJECT:
  🧠 AI/ML Digest — Feb 23, 2026 | 4 Breaking · 5 Framework Updates

EMAIL BODY SECTIONS:
  ┌────────────────────────────────────────────────────────┐
  │  🧠 AI/ML Daily Digest                Feb 23, 2026     │
  │  238 items processed · 4 breaking · Gemini Flash 2.0  │
  └────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────┐
  │  🚨 BREAKING TODAY                                     │
  │                                                        │
  │  [LangGraph v0.2.1]  ████████████ 10/10               │
  │  Summary text...                          [Read →]     │
  │                                                        │
  │  [Gemini 2.5 Ultra]  ████████████ 10/10               │
  │  Summary text...                          [Read →]     │
  └────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────┐
  │  🧠 AGENT FRAMEWORKS  │  ⚙️ BACKEND FRAMEWORKS          │
  │                        │                               │
  │  LangGraph v0.2.1  10  │  FastAPI 0.111.0  9          │
  │  CrewAI v0.28.0     9  │  MLflow 2.15.0    8          │
  │                        │                               │
  └────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────┐
  │  📰 TOP STORIES                                        │
  │                                                        │
  │  1. Anthropic publishes interpretability results   9/10│
  │     Summary · Tags: Research · Safety     [Read →]     │
  │                                                        │
  │  2. OpenAI open-sources reasoning dataset          8/10│
  │     Summary · Tags: LLM · Dataset        [Read →]     │
  │  [... 6 more stories ...]                              │
  └────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────┐
  │  💻 TRENDING REPOS        📄 TOP PAPERS                │
  │  [3 cards]                [3 cards]                    │
  └────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────┐
  │  View full digest → your-dashboard.vercel.app          │
  │  Powered by Gemini Flash 2.0 + 40+ MCP sources         │
  └────────────────────────────────────────────────────────┘
```

---

## 17. Step-by-Step Build Timeline — Scratch to Production

### Week 1 — Accounts, Local Setup, First Working Tool

```
DAY 1: Create All Required Accounts
  □ Google AI Studio (aistudio.google.com) → get Gemini API key
  □ Supabase (supabase.com) → create project, note URL + keys
  □ Prefect Horizon (horizon.prefect.io) → sign in with GitHub
  □ Telegram → create bot via @BotFather → save token
  □ Discord → create webhook in your server → save URL
  □ Resend (resend.com) → create account → get API key
  □ Kaggle (kaggle.com) → create account → download API token
  □ Semantic Scholar (semanticscholar.org/product/api) → free key
  □ OpenReview (openreview.net) → create free account
  □ GitHub → create Personal Access Token (PAT) for GitHub MCP

DAY 2-3: Install Local Development Tools
  □ Install Python 3.11 (python.org)
  □ Install pip: python -m ensurepip
  □ Install FastMCP: pip install fastmcp
  □ Install feedparser: pip install feedparser
  □ Install arxiv: pip install arxiv
  □ Install httpx: pip install httpx
  □ Install crawl4ai: pip install crawl4ai + playwright install chromium
  □ Install kaggle: pip install kaggle
  □ Verify all installs with: pip list
  □ Create GitHub account if not exists
  □ Install Git on your PC (git-scm.com)

DAY 4-5: Build First Tool (RSS) and Test
  □ Create folder: ai-digest-research-server
  □ Create main.py with FastMCP server instance
  □ Write rss/fetch_feed tool (single feed URL)
  □ Add @mcp.tool decorator and docstring
  □ Run: fastmcp dev main.py
  □ Open MCP Inspector in browser
  □ Test rss/fetch_feed with OpenAI blog URL
  □ Verify you get back article titles and summaries
  □ Create config/rss_sources.yaml with first 5 feeds
  □ Write rss/fetch_all tool
  □ Test: all 5 feeds return items in MCP Inspector

DAY 6-7: Complete Research Server Tools
  □ Add arxiv/get_recent tool → test with cs.AI
  □ Add papers/trending tool → test with PWC API
  □ Add scholar/search tool → test with "LLM agents"
  □ Add openreview/neurips tool → test with 2024 venue
  □ Add fetch/url tool → test with HF Forums URL
  □ Add kaggle/datasets tool → test with "llm" tag
  □ Test all tools in MCP Inspector
  □ Create requirements.txt with all dependencies
  □ Create .env.example template

END OF WEEK 1: Research server works locally with 8+ tools tested
```

### Week 2 — Community Server + Horizon Deployment

```
DAY 1-2: Build Community Server
  □ Create folder: ai-digest-community-server
  □ Create main.py with FastMCP server instance
  □ Write reddit/r_machinelearning tool
  □ Test: hot.json returns posts correctly
  □ Write reddit/r_localllama, r_deeplearning, r_datascience, r_ai
  □ Write hn/top_ai tool using Algolia API
  □ Test: HN returns AI stories with score filter
  □ Write hf/trending_models tool
  □ Write hf/daily_papers tool
  □ Write hf/trending_spaces tool
  □ Test all tools in MCP Inspector
  □ Create requirements.txt (just httpx + fastmcp)

DAY 3-4: Deploy Research Server to Horizon
  □ Create GitHub repo: ai-digest-research-server
  □ Push main.py, requirements.txt, config/ folder
  □ Go to horizon.prefect.io
  □ Click Deploy → select your repo
  □ Set entrypoint: main.py:mcp
  □ Add environment variables: KAGGLE_USERNAME, KAGGLE_KEY
  □ Click Deploy → wait 60 seconds
  □ Open ChatMCP interface in Horizon
  □ Test EVERY tool in the live Horizon deployment
  □ Copy your live URL and save it

DAY 5-6: Deploy Community Server to Horizon
  □ Create GitHub repo: ai-digest-community-server
  □ Push code to GitHub
  □ Deploy to Horizon (same steps as above)
  □ Test all community tools via ChatMCP
  □ Copy live URL

DAY 7: Build and Deploy Utility Server
  □ Create ai-digest-utility-server folder
  □ Write crawl/page tool using crawl4ai
  □ Write search/web tool (pick a public SearXNG instance)
  □ Write memory tools
  □ Test locally
  □ Deploy to Horizon
  □ Test via ChatMCP

END OF WEEK 2: All 3 custom servers live on Horizon, tested, URLs saved
```

### Week 3 — Pipeline Orchestrator + Gemini + Supabase

```
DAY 1-2: Create Supabase Database
  □ Go to Supabase project → SQL Editor
  □ Run schema.sql to create all 4 tables
  □ Verify tables appear in Table Editor
  □ Note: project_ref for Supabase MCP URL
  □ Test Supabase MCP endpoint in browser

DAY 3-4: Build Pipeline Orchestrator
  □ Create folder: ai-digest-pipeline
  □ Create mcp_config.py with all 7 server URLs
  □ Create orchestrator.py that:
     → Calls all 3 Horizon servers in parallel
     → Calls GitHub MCP cloud server
     → Merges all results
  □ Test: run orchestrator.py locally
  □ Verify all servers respond with data
  □ Verify you get ~400+ raw items

DAY 5-6: Add Deduplication and Gemini
  □ Create deduplicator.py
  □ Test deduplication on the 400 raw items
  □ Verify duplicates are removed (should drop to ~200)
  □ Create gemini_client.py
  □ Build the Gemini prompt (JSON instructions)
  □ Test: send 10 items to Gemini, check quality
  □ Test: send all 200 items in one batch
  □ Verify scores, summaries, tags look correct

DAY 7: Add Supabase Saving
  □ Create supabase_client.py
  □ Add save functions for each table
  □ Test: run full pipeline, check Supabase Table Editor
  □ Verify data appears in all 3 tables
  □ Verify digest_runs table has an entry

END OF WEEK 3: Full pipeline runs locally end-to-end
```

### Week 4 — Publishers + Automation + Dashboard

```
DAY 1-2: Build Publishers
  □ Create telegram_publisher.py
  □ Test: send sample message to your Telegram bot
  □ Implement all 5 message sections
  □ Add command handlers: /today, /agents, /backend, /papers
  □ Create discord_publisher.py
  □ Test: send embeds to your Discord channel
  □ Verify color coding works
  □ Create email_publisher.py
  □ Test: send sample email via Resend
  □ Check rendering on Gmail + mobile

DAY 3-4: GitHub Actions Setup
  □ Create .github/workflows/daily_digest.yml in pipeline repo
  □ Push to GitHub
  □ Go to repo → Actions → Run Workflow (manual trigger)
  □ Watch the live logs in GitHub Actions
  □ Verify all steps complete successfully
  □ Check Telegram/Discord/Email received the digest
  □ Check Supabase was updated

DAY 5-6: Build Next.js Dashboard
  □ Create Next.js 14 app in frontend/ folder
  □ Install Supabase JS client
  □ Build main feed page (reads news_items table)
  □ Build agents page (filter AgentFramework)
  □ Build backend page (filter BackendFramework)
  □ Build papers page
  □ Build GitHub trending page
  □ Deploy to Vercel (connect GitHub repo)
  □ Add SUPABASE env vars in Vercel settings
  □ Test live dashboard URL

DAY 7: Final Testing + Monitoring Setup
  □ Wait for scheduled 7 AM run (or trigger manually)
  □ Verify all channels received the digest
  □ Check Supabase row count increased
  □ Enable GitHub Actions email notifications for failures
  □ Test each Telegram bot command
  □ Make any formatting adjustments
  □ System is LIVE ✅

END OF WEEK 4: Fully automated, 24/7, PC-off system
```

---

## 18. Complete Accounts & Keys Setup

Everything you need to sign up for before you start building:

```
REQUIRED — Cannot build without these:
────────────────────────────────────────────────────────────────
1. GitHub Account
   URL:      github.com
   Sign up:  Free
   What for: Store 4 repos + GitHub Actions cron + GitHub MCP
   Key type: Personal Access Token (Fine-grained)
   Where:    github.com/settings/tokens → Fine-grained → New token
   Permissions needed: Contents read, Metadata read
   Free limits: 5,000 API req/hr, 2,000 Actions min/month

2. Prefect Horizon Account
   URL:      horizon.prefect.io
   Sign up:  Sign in with GitHub (no separate registration)
   What for: Free hosting for your 3 FastMCP servers
   Key type: No key needed — uses GitHub OAuth
   Free limits: Personal projects free forever

3. Supabase Account
   URL:      supabase.com
   Sign up:  Free (email or GitHub login)
   What for: PostgreSQL database for all digest data
   Key type: Project URL + anon key + service role key
   Where:    Project Settings → API → Project URL and Keys
   Free limits: 500MB, 50,000 rows, 2GB bandwidth/month

4. Google AI Studio (Gemini API)
   URL:      aistudio.google.com
   Sign up:  Sign in with Google account
   What for: Gemini Flash 2.0 for summarization
   Key type: API Key (starts with "AIzaSy...")
   Where:    aistudio.google.com → Get API Key → Create API Key
   Free limits: 1,500 requests/day, 1M tokens/min

5. Telegram Bot
   Process:  Open Telegram → search @BotFather → /newbot
   What you get: BOT_TOKEN (format: 1234:ABCdef...)
   Chat ID:  After creating bot, send /start to it
             Then fetch: api.telegram.org/bot<TOKEN>/getUpdates
             Look for "chat": {"id": YOUR_CHAT_ID}
   Free limits: Unlimited for personal bots

6. Discord Webhook
   Process:  Discord server → any channel → Edit Channel
             → Integrations → Webhooks → New Webhook
   What you get: Webhook URL (long URL starting with discord.com/api/...)
   Free limits: 30 webhook calls/minute per channel

7. Resend Email
   URL:      resend.com
   Sign up:  Free
   What for: Send your daily email digest
   Key type: API Key (starts with "re_...")
   Where:    resend.com → API Keys → Create API Key
   Domain:   Add your domain (for custom from address)
             OR use onboarding@resend.dev for testing
   Free limits: 3,000 emails/month

OPTIONAL — For specific data sources:
────────────────────────────────────────────────────────────────
8. Kaggle Account
   URL:      kaggle.com
   Sign up:  Free
   What for: kaggle/* tools for datasets and competitions
   Key type: Username + API Key (in kaggle.json file)
   Where:    kaggle.com → Account → Settings → Create New API Token
             Downloads kaggle.json file — save username and key from it
   Free limits: Unlimited API access

9. Semantic Scholar (Optional)
   URL:      semanticscholar.org/product/api
   Sign up:  Free
   What for: Higher rate limits for scholar/* tools
             (Works without key at 100 req/5min; with key at 1 req/sec)
   Key type: API Key
   Free limits: 1 request/second with free key

10. OpenReview Account
    URL:     openreview.net
    Sign up: Free (email + password)
    What for: openreview/* tools for conference papers
    Key type: Email + password (passed as env vars)
    Free limits: No stated limits for read access

DASHBOARD ONLY:
────────────────────────────────────────────────────────────────
11. Vercel Account
    URL:     vercel.com
    Sign up: Free (sign in with GitHub)
    What for: Host your Next.js dashboard
    Free limits: Unlimited personal projects, 100GB bandwidth/month
```

---

## 19. Final Cost Summary

```
╔══════════════════════════════════════════════════════════════╗
║              COMPLETE MONTHLY COST BREAKDOWN                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  HOSTING                                                     ║
║  Prefect Horizon (3 FastMCP servers)  FREE for personal      ║
║  Vercel (Next.js dashboard)           FREE unlimited         ║
║  GitHub Actions (cron scheduler)      FREE 2000 min/month    ║
║                                                              ║
║  DATABASES & APIS                                            ║
║  Supabase (PostgreSQL DB)             FREE 500MB             ║
║  Gemini Flash 2.0 (AI summaries)      FREE 1,500 req/day     ║
║                                                              ║
║  NOTIFICATIONS                                               ║
║  Telegram Bot API                     FREE unlimited         ║
║  Discord Webhooks                     FREE unlimited         ║
║  Resend (email)                       FREE 3,000 emails/mo   ║
║                                                              ║
║  DATA SOURCES (all MCP servers)                              ║
║  GitHub MCP (official cloud)          FREE with GitHub acct  ║
║  HuggingFace MCP (official cloud)     FREE with HF account   ║
║  Supabase MCP (official cloud)        FREE your own DB       ║
║  Context7 MCP (context7.com)          FREE personal tier     ║
║  ArXiv API (no MCP needed)            FREE always            ║
║  Reddit JSON API                      FREE always            ║
║  HN Algolia API                       FREE always            ║
║  OpenReview API                       FREE always            ║
║  Papers With Code API                 FREE always            ║
║  Kaggle API                           FREE with account      ║
║  Semantic Scholar API                 FREE with free key     ║
║  RSS/Atom feeds (35+ sources)         FREE always            ║
║                                                              ║
║  YOUR USAGE vs FREE LIMITS                                   ║
║  Gemini:         1-2 calls/day vs 1,500 limit  = 0.1%       ║
║  Supabase:       ~300 rows/day vs 50k limit    = growing     ║
║                  Enough for 4+ months of data               ║
║  GitHub Actions: 4 min/day vs 2,000 min/month  = 6%         ║
║  Resend:         1 email/day vs 3,000/month    = 1%          ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  TOTAL MONTHLY COST:                  $0.00                  ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 20. Final Launch Checklist

### Accounts Verified
```
□ GitHub: Account exists, PAT created with correct permissions
□ Horizon: Account created, signed in with GitHub
□ Supabase: Project created, schema SQL executed, tables visible
□ Google AI Studio: API key created and tested (returns summaries)
□ Telegram: Bot created, token saved, your chat ID found and verified
□ Discord: Webhook URL created for target channel
□ Resend: Account created, sender verified, API key saved
□ Kaggle: Account created, kaggle.json downloaded, credentials saved
□ Semantic Scholar: Free API key created (optional but recommended)
□ OpenReview: Free account created, email and password saved
□ Vercel: Account created, signed in with GitHub
```

### Server 1 (Research) — Verified
```
□ All tools defined and decorated with @mcp.tool
□ All docstrings written (describes what tool does, what it returns)
□ rss_sources.yaml contains all 35+ feed URLs
□ Tested every tool in FastMCP Inspector locally — all return data
□ requirements.txt complete
□ Pushed to GitHub repo: ai-digest-research-server
□ Deployed to Horizon — status shows green/running
□ All tools tested in Horizon ChatMCP interface with real data
□ Horizon URL saved: https://ai-digest-research.YOUR_NAME.fastmcp.app/mcp
```

### Server 2 (Community) — Verified
```
□ All Reddit tools return posts with correct score filtering
□ HN tool returns AI stories with 50+ score
□ HF tools return models/spaces/papers
□ Tested in FastMCP Inspector locally
□ Pushed to GitHub repo: ai-digest-community-server
□ Deployed to Horizon — status green
□ All tools tested in Horizon ChatMCP
□ Horizon URL saved
```

### Server 3 (Utility) — Verified
```
□ crawl/page tool tested on a JS-heavy page (Medium article)
□ search/web tool returns results from SearXNG
□ memory tools save and recall correctly
□ Deployed to Horizon — status green
□ Horizon URL saved
```

### Cloud MCPs — Configured
```
□ GitHub MCP URL: api.githubcopilot.com/mcp/ — tested with PAT
□ Supabase MCP URL: mcp.supabase.com — tested with project ref
□ Context7 — tested (npx @upstash/context7-mcp)
□ All URLs saved in mcp_config.py
```

### Database — Verified
```
□ All 4 Supabase tables created: news_items, papers, github_repos, digest_runs
□ All indexes created
□ Test insert and query work correctly
□ Supabase MCP can query your DB
```

### Pipeline — Verified
```
□ orchestrator.py calls all 7 MCP servers successfully
□ Returns 400+ raw items from a real test run
□ Deduplication reduces to ~200 unique items
□ Gemini returns summaries and scores for all items
□ Quality of summaries looks good (technical, accurate)
□ Saving to Supabase works — rows appear in table editor
□ digest_runs table shows a success entry
```

### Publishers — Verified
```
□ Telegram: Received full formatted digest in your chat
□ Telegram: /today command returns today's top 10 items
□ Telegram: /agents returns only AgentFramework items
□ Telegram: /backend returns only BackendFramework items
□ Discord: Embeds appear with correct color coding
□ Discord: Breaking news appears as red embed at top
□ Email: Received in inbox (not spam folder)
□ Email: Renders correctly on mobile and desktop
```

### GitHub Actions — Verified
```
□ .github/workflows/daily_digest.yml committed to pipeline repo
□ All 13 secrets added to repo Settings → Secrets
□ Manual trigger (Run Workflow) completed successfully
□ All steps show green checkmarks in Actions log
□ Failure notification email enabled in Actions settings
□ Cron schedule confirmed: 30 1 * * * = 7:00 AM IST
```

### Dashboard — Verified
```
□ Next.js app deployed on Vercel
□ Supabase env vars added in Vercel project settings
□ Main feed loads with today's items sorted by score
□ Breaking banner appears correctly
□ /agents page filters correctly
□ /backend page filters correctly
□ /papers page shows abstracts
□ /github page shows star counts
□ /archive date picker works
□ Search bar returns results
```

### Final Live Test
```
□ Waited for scheduled 7:00 AM run (or triggered manually)
□ All 4 channels received the digest simultaneously
□ Supabase row count increased by expected amount
□ digest_runs table shows status: "success"
□ PC was off during the run — everything still worked
□ SYSTEM IS FULLY LIVE ✅
```

---

## Appendix A — Where to Get Everything

```
FRAMEWORKS & LIBRARIES:
FastMCP Documentation:      gofastmcp.com
FastMCP GitHub:             github.com/PrefectHQ/fastmcp
FastMCP PyPI:               pip install fastmcp
FastMCP Discord:            discord.gg/fastmcp

MCP Official Documentation: modelcontextprotocol.io
MCP Python SDK:             github.com/modelcontextprotocol/python-sdk

DATA SOURCE LIBRARIES:
feedparser (RSS):           feedparser.readthedocs.io
                            pip install feedparser
arxiv Python library:       lukasschwab.me/arxiv.py
                            pip install arxiv
httpx (HTTP client):        www.python-httpx.org
                            pip install httpx
crawl4ai:                   crawl4ai.com
                            pip install crawl4ai
kaggle:                     github.com/Kaggle/kaggle-api
                            pip install kaggle

CLOUD SERVICES:
Prefect Horizon:            horizon.prefect.io
GitHub (Actions + MCP):     github.com / api.githubcopilot.com/mcp/
HuggingFace MCP:            huggingface.co/mcp
Supabase:                   supabase.com / mcp.supabase.com
Context7:                   context7.com / upstash/context7-mcp
SearXNG public instances:   searx.space
Google AI Studio:           aistudio.google.com
Vercel:                     vercel.com
Resend:                     resend.com

APIs (all free):
ArXiv API:                  info.arxiv.org/help/api/index.html
Papers With Code API:       paperswithcode.com/api/v1/docs
Semantic Scholar API:       api.semanticscholar.org/api-docs
OpenReview API:             docs.openreview.net/reference/api-v2
HuggingFace API:            huggingface.co/docs/api-inference
Reddit JSON:                reddit.com/r/SUBREDDIT/hot.json
HN Algolia API:             hn.algolia.com/api
Kaggle API:                 kaggle.com/docs/api
Stack Exchange API:         api.stackexchange.com
```

---

*Built to run forever at $0/month · PC never required · Fully automated · 95%+ source coverage*
*FastMCP + Prefect Horizon + GitHub Actions + Gemini Flash 2.0 + Supabase + Vercel*
