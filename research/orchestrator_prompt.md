# AI Orchestrator Research Prompt — Decision Intelligence Tool

## Orchestrator Configuration
- **Category:** Deep Research (Multi-Phase)
- **Mode:** Expert
- **Web Search:** ON
- **Phases:** 4-5
- **Output:** Long (6000+ chars)

---

## PROMPT TO PASTE INTO ORCHESTRATOR:

---

Conduct a comprehensive product research and strategic analysis for a Decision Intelligence Tool called "DecideIQ" that I am building and preparing to launch.

## WHAT WE BUILT

DecideIQ is an AI-powered decision comparison tool. Users describe a decision in natural language ("Should I buy Tesla Model 3 or Mach-E?"), and the system:

1. **Extracts** structured options and criteria from natural language input (GPT-4o-mini)
2. **Validates** the extraction quality before committing to expensive judge calls
3. **Anonymizes and shuffles** options to prevent position bias
4. **Runs 3 independent AI analysts in parallel** (GPT-4o/mini, Claude Sonnet/Haiku, Gemini Flash) — each with a different analytical perspective:
   - General Analyst (balanced assessment)
   - Risk Skeptic (devil's advocate, finds what could go wrong)
   - Pragmatist (focuses on execution feasibility)
5. **Aggregates** scores using rank-point consensus with judge agreement detection
6. **Synthesizes** a coherent recommendation from all judge outputs (separate AI call)
7. **Computes confidence** based on score spread, judge agreement, and judge count

### Architecture
- Python + FastAPI backend, single deploy
- Jinja2 server-rendered frontend (dark theme, Fin.ai-inspired design)
- 6 LLM provider adapters (OpenAI, Anthropic, Google, DeepSeek, xAI, mock)
- Blind judging ported from a proven multi-AI evaluation system
- Settings: depth (quick/standard/deep), focus (balanced/risk/practical), response length, web search toggle, file attachments
- Benchmark system: 20-test evaluation suite with independent quality grading

### Current Benchmark Scores (Round 3, 20 decisions)
- Overall Quality: **7.3/10**
- Winner Accuracy: 7.7 (Strong)
- Reasoning Quality: 7.2 (Good)
- Score Differentiation: 7.0 (Good)
- Strength/Weakness Quality: 7.5 (Good)
- Confidence Calibration: 6.5 (Good) — weakest dimension
- Decisiveness: 8.3 (Strong)

### Category Performance
- Technical decisions: 8.5/10
- Personal decisions: 7.6/10
- Consumer product decisions: 7.2/10
- Business decisions: 7.0/10
- Creative decisions: 6.8/10

### Cost
- $0.002-0.003 per decision (standard mode, cheap models)
- $0.05 per decision (deep mode, flagship models)
- Average latency: 15-25 seconds

## WHO WILL USE THIS

**Primary users:**
1. **Me (the founder)** — for my SaaS and service businesses: freight forwarding sales decisions, operations decisions, vendor selection, pricing strategy, hiring, tech stack choices
2. **Business professionals** — comparing vendors, strategies, pricing plans, tools
3. **Consumers** — comparing products, services, financial options
4. **Freelancers/consultants** — making client recommendations with data backing

**My specific use cases:**
- Freight forwarding: compare carriers, routes, pricing for oversized cargo
- SaaS operations: choose tools, prioritize features, hiring decisions
- Daily business decisions that currently take hours of manual comparison

## WHAT I NEED FROM THIS RESEARCH

### Phase 1: Competition Analysis
Research and analyze ALL direct and indirect competitors in the "AI decision-making" and "option comparison" space. Include:
- What tools exist today for AI-powered decision comparison? (not just AI chatbots — specific decision tools)
- How do they position themselves? What's their value proposition?
- What do they charge? Free tier? Premium pricing?
- What's their tech approach? Single model or multi-model?
- What are their strongest features that we should replicate or improve?
- What are their weakest points we can exploit?
- Are any of them making real money? What's their estimated revenue/traction?
- How do they acquire users? SEO? Product Hunt? Paid ads? Viral loops?

### Phase 2: Product Gaps and Improvements
Based on competition analysis AND our current benchmark data, identify:
- What specific features are we missing that competitors have?
- What features could we add that NO competitor has (our unique advantage)?
- How do we get from 7.3/10 to 8.5/10 quality?
- What should the admin dashboard include for a founder using this daily?
- What analytics/tracking would make this tool more valuable?
- Should we add follow-up questions? Drill-down analysis? "What if" scenarios?
- Should we add a chat interface post-decision for clarifying questions?
- What about decision templates for specific industries (freight, SaaS, etc.)?

### Phase 3: UI/UX and Launch Readiness
- Review our current approach (single-page, tool-first, Fin.ai-inspired dark theme) — is this the right positioning?
- What does the ideal onboarding flow look like?
- How should we handle the first-time user experience?
- What trust signals are most effective for a decision tool?
- What's the minimum viable launch checklist?
- Domain recommendations (decideiq.com? decidebetter.ai? other?)
- Where should we launch first? (Product Hunt, HN, Twitter, Reddit, specific communities)

### Phase 4: Monetization and Growth Strategy
- What's the right pricing model? Freemium with limits? Pro tier? Usage-based?
- What should free users get? What's behind the paywall?
- How do we create viral sharing loops from decision results?
- What's the SEO strategy? Programmatic pages? Blog content?
- How do we build a moat against ChatGPT/Claude doing this directly?
- What's the realistic path to $1k/mo, $10k/mo, $100k/mo?

### Phase 5: Execution Roadmap
Provide a prioritized, actionable roadmap:
- What to do THIS WEEK (immediate impact)
- What to do THIS MONTH (launch readiness)
- What to build in MONTH 2-3 (growth features)
- What to build in MONTH 4-6 (moat and scale)

Be specific. Include tool names, exact features, pricing tiers, marketing channels, content strategies. No generic advice.

---
