

# DecideIQ: Final Strategic Plan & Execution Roadmap

## Executive Summary

DecideIQ enters a fragmented AI decision-support market where no product combines decision science methodology with multi-model AI reasoning and team workflows. The competitive window is 12–18 months before general AI assistants potentially absorb this functionality. The plan below is a 6-month execution sequence that ships persistence and multi-model reasoning in Week 1, launches publicly on Day 8, activates paid Pro ($19/month) in Month 2, ships Team tier ($49/seat/month) in Month 5, and targets $500K–$700K ARR by Month 12 through a deliberate progression from individual power users to team adoption.

---

## PART 1: COMPETITIVE POSITIONING

DecideIQ occupies the only undefended position in this market: **high methodology rigor + high accessibility**. Traditional AHP tools (Expert Choice, SuperDecisions) have rigor but terrible UX. General AI assistants (ChatGPT, Claude, Perplexity) have accessibility but no persistent framework, no adversarial validation, and no team workflow. Decidedly.ai — the closest pure-play competitor — is early-stage, single-model, and weak on transparency and collaboration.

**DecideIQ's one-line positioning:** "Three AI models argue about your decision so you don't have to — with the methodology to prove it's right."

**The four structural advantages to build and protect:**

| Advantage | Why It's Defensible |
|---|---|
| Multi-model adversarial reasoning | General AI assistants are structurally locked to their own model; they cannot offer this |
| Decision persistence + outcome tracking | Creates compounding data asset and switching costs ChatGPT cannot replicate |
| Transparent AHP/MCDA methodology | Grounds recommendations in published decision science, not "an AI said so" |
| Multi-stakeholder collaboration workflows | Single-user chat interfaces cannot become team decision platforms without architectural overhaul |

**Primary threat to monitor:** OpenAI or Anthropic shipping a built-in "Decision Mode" with persistent frameworks. Estimated timeline: 12–18 months. DecideIQ must have retention-creating features (decision history, outcome tracking, team workflows) deeply embedded before this happens.

---

## PART 2: PRODUCT ARCHITECTURE

### What Ships at Launch (Day 8)

| Component | Specification |
|---|---|
| **Decision persistence** | Every completed decision auto-saved as structured JSON. Decision Library: searchable, filterable by date/category/template. Free tier: 90-day retention (decisions visible but locked after day 91). Pro/Team: permanent. |
| **Multi-model reasoning v1** | GPT-4o + Claude 3.7 Sonnet. Identical structured prompt to each. Agreement display: green (2/2 agree) or amber (divergence) with side-by-side reasoning. Cost: ~$0.01–0.02/decision. |
| **Methodology trace v1** | Collapsible "How we got here" panel: criteria weights visualized, per-option scoring with justification, model disagreement explanation, assumptions listed with override buttons. |
| **Interactive demo decision** | Pre-built "Which project management tool should your team adopt?" (Asana/Monday.com/Notion/Linear). Pre-configured with visible model disagreement. Single slider interaction demonstrates multi-model + transparency + scenario sensitivity in 10 seconds. |
| **4 launch templates** | SaaS vendor selection, hiring candidate comparison, feature prioritization, personal/life decision. Pre-loaded criteria and typical weights. |
| **Deferred account creation** | Decision completes → "Save this decision" prompt → signup. The completed decision is the hostage. |
| **Responsive web** | Desktop-optimized, mobile-functional. No native apps. |
| **Analytics** | Mixpanel free tier. Events: `demo_slider_adjusted`, `decision_started`, `decision_completed`, `signup_prompt_shown`, `account_created`, `return_visit_7d`, `template_selected`. |

### What Ships Months 2–3 (Differentiation Phase)

| Feature | Spec | Monetization Gate |
|---|---|---|
| **Multi-model v2** | Add Gemini 1.5 Pro (3rd model). Adversarial challenge mode: second model prompted to attack first model's reasoning. Confidence calibration: 3/3 agree → high, 2/3 split → moderate with drill-down. | Free: 2 models + basic disagreement. Pro: 3 models + adversarial + confidence scores. |
| **6 industry templates** | SaaS, hiring, real estate, healthcare, finance/investment, product management. Each with domain-specific criteria, typical weights, sample justifications. | All templates free. Custom template *creation* is Pro. |
| **Outcome tracking v1** | Automated prompts at 30/60/90 days: "How did this work out?" Structured 1–5 rating + notes. | Free: single 30-day check-in. Pro: full timeline. |
| **Scenario modeling v2** | Multi-variable adjustment. Saved scenario snapshots ("Conservative" vs. "Growth"). Side-by-side comparison. Tipping point visualization. | Free: single-slider sensitivity. Pro: multi-variable + saved snapshots. |
| **Bias detection** | Flags when criteria weights suggest anchoring, status quo bias, or familiarity bias. Offers to test with adjusted weights. | Pro feature. |
| **Criteria reuse** | "Last time you evaluated SaaS tools, you weighted cost at 35%. Use these again?" | Requires 2+ saved decisions in same category. |

### What Ships Months 4–6 (Monetization Phase)

| Feature | Spec | Tier |
|---|---|---|
| **Collaborative workflows** | Stakeholder invitation via link/email. Independent criteria weighting and scoring per stakeholder. Weighted expertise scoring (CFO's cost input counts 3x). Consensus heatmap. Async input with deadlines/reminders. Discussion threads per criterion. Alignment score. | Team tier. |
| **Admin dashboard** | Decision velocity metrics, team alignment analytics, stakeholder participation rates, outcome tracking aggregate view, compliance/audit trail export. | Team tier. |
| **Shareable decision cards** | Visual branded summary for Twitter/LinkedIn sharing. Shows recommendation, key criteria, model confidence, one-line disagreement highlight. "Run your own decision" CTA with template pre-loaded. | All tiers (viral growth mechanic). |
| **Programmatic SEO pages** | `/compare/saas/asana-vs-monday-vs-notion` format. Pre-built framework + aggregated anonymized insights + interactive preview + CTA. Launch with 50 pages across 6 verticals. | Public (acquisition mechanic). |

---

## PART 3: PRICING

```
FREE ("Decide")          PRO ("Decide Better")       TEAM ("Decide Together")
$0/month                 $19/month ($15 annual)      $49/seat/month ($39 annual)
                                                      3-seat minimum

5 decisions/month         Unlimited                   Unlimited
2 AI models              3 models + adversarial       3 models + adversarial
6 criteria max           Unlimited criteria           Unlimited criteria
90-day history           Permanent history            Permanent history
Basic disagreement       Full methodology trace       Full methodology trace
Single-slider scenarios  Multi-variable + snapshots   Multi-variable + snapshots
View-only sharing        5 collaborators/decision     Unlimited collaborators
1 outcome check-in       Full outcome timeline        Team outcome dashboard
No export                PDF/CSV export               PDF/CSV + audit trail
No custom templates      Custom template creation     Custom templates + admin
—                        —                            Weighted expertise scoring
—                        —                            Consensus visualization
—                        —                            Admin dashboard + analytics
—                        —                            SSO/SAML
```

**Enterprise:** Custom pricing ($99+/seat) for 50+ seats, API access, custom LLM deployment, dedicated CSM, SLA, data residency. Not a launch priority — pursue only after 10+ Team tier customers validate B2B demand.

**Why these specific boundaries:** The free tier is generous enough for genuine habit formation (5 decisions covers most casual users) but constrains power users on model count, criteria depth, and persistence. The Pro gate triggers when a user wants deeper analysis, permanent history, or custom templates — signals of a committed user worth $19/month. The Team gate triggers when a user says "I need my team's input" — the moment individual value becomes organizational value worth $49/seat.

---

## PART 4: GROWTH ENGINES

### Engine 1: Launch Sequence (Week 2)

| Day | Platform | Specific Execution |
|---|---|---|
| Day 8 | **Product Hunt** | Tagline: "3 AIs argue about your decision so you don't have to." 15-second demo GIF: slider interaction → disagreement update → methodology trace. Maker comment: explain multi-model ensemble + AHP methodology. Launch offer: "Founding Member" badge + 6 months Pro free. Target: Top 5 Product of the Day, 500+ signups. |
| Day 9–10 | **Hacker News (Show HN)** | Lead with technical architecture. Invite scrutiny of the methodology. "Here's the math — tell us where we're wrong." Target: 50+ points, 200+ signups. |
| Day 10–12 | **Reddit** (1 post/day, staggered) | r/ProductManagement: feature prioritization template. r/startups: vendor selection template. r/SaaS: SaaS comparison template. Real decision analysis, not promotional. Target: 100+ signups across subreddits. |
| Day 12 | **Twitter/X** | First "Decision Breakdown" thread. Target: 10K+ impressions, 50+ click-throughs. |

### Engine 2: Content (Ongoing from Month 2)

**Weekly "Decision Breakdown" threads** on Twitter/X and LinkedIn. Format: "We ran [interesting real-world decision] through DecideIQ. Here's what 3 AI models disagreed about." Each links to the template used. This is the primary organic acquisition loop — it demonstrates the product's unique capability while generating shareable content.

**LinkedIn-specific angle (Weeks 3–4+):** Target team leads and VPs with professional positioning: "How we used structured decision methodology to choose between 4 marketing automation platforms — and what the AI got wrong." Decision-making content resonates strongly with LinkedIn's audience.

**Resource:** 4–6 hours/week founder time, or one part-time content person at $2,000/month starting Month 2.

### Engine 3: Programmatic SEO (Month 4+)

Launch 50 comparison pages across 6 verticals: `/compare/saas/asana-vs-monday-vs-notion`, `/compare/hiring/in-house-vs-agency-marketing`, `/compare/real-estate/rent-vs-buy-austin`. Each page contains a pre-built decision framework, aggregated anonymized insights from real usage, interactive slider preview, and CTA to customize with your own criteria. Target: ranking for long-tail comparison queries within 3–6 months.

**Critical quality constraint:** Each page must contain genuine unique analytical content with real aggregated data. Thin programmatic pages will be penalized by Google's helpful content systems. The interactive preview and community data are what make these pages defensible.

### Engine 4: Viral Mechanics (Month 4+)

**Shareable decision cards:** Every completed decision generates a branded visual summary (decision, recommendation, key criteria, model confidence, disagreement highlight) designed for Twitter/LinkedIn posting. Each card includes "Run your own decision" CTA with template pre-loaded. This is DecideIQ's "Spotify Wrapped" for decisions.

**Collaborative invitation loop:** Every Team decision that invites external stakeholders (vendors, advisors, board members) exposes new users to DecideIQ. Stakeholders participate without an account, see the full methodology, and receive post-decision signup prompt.

**Referral program (simple):** Free→Free referral: both get 2 bonus decisions that month. Free→Pro referral: referrer gets 1 month Pro free. Pro→Team referral: referrer gets 1 month free per converted seat (cap 3 months).

### Engine 5: Paid Acquisition (Month 3+, Contingency)

**This is the plan's insurance policy against organic growth underperformance.** If by end of Month 2 active users are below 2,000, allocate $1,500–3,000/month to targeted Google Ads on high-intent comparison queries ("best project management tool comparison," "vendor selection framework," "AHP decision tool") and LinkedIn ads targeting product managers, operations leaders, and procurement teams. CPA target: $5–15 for free signup, $50–100 for Pro conversion.

---

## PART 5: EXECUTION ROADMAP

### Week 1 (Days 1–7): Foundation Sprint

| Day | Deliverable | Success Metric |
|---|---|---|
| 1–4 | Decision persistence layer (Supabase Pro + Vercel Pro) | 100% of completed decisions auto-saved; Library loads <2s for 50+ decisions |
| 2–5 | Multi-model reasoning v1 (GPT-4o + Claude 3.7 Sonnet) | Both responses return <8s combined; disagreement detection validated on 50 test cases |
| 2–4 | Interactive demo decision (PM tool comparison) | Slider interaction → re-ranking + disagreement update works flawlessly on desktop and mobile |
| 5 | Analytics infrastructure (Mixpanel) | All 7 critical events firing correctly |
| 6 | Seed 50 beta testers | Recruited from r/ProductManagement, decision-science LinkedIn groups, startup Slack communities. Offer: 6 months Pro free for 3+ decisions + feedback survey. |
| 7 | Pre-launch checklist complete | DNS, SSL, rate limits, demo, signup flow, analytics — all verified end-to-end |

**Week 1 infrastructure cost:** Supabase Pro $25/mo + Vercel Pro $20/mo + API credits $500/mo + Mixpanel $0 = **~$545/month** running cost.

### Week 2 (Days 8–14): Launch

| Day | Action | Target |
|---|---|---|
| 8 | Product Hunt launch | Top 5 POTD, 500+ signups |
| 9–10 | Hacker News Show HN | 50+ points, 200+ signups |
| 10–12 | Reddit (staggered) | 100+ signups across 3 subreddits |
| 12 | First Twitter Decision Breakdown | 10K impressions |
| 13–14 | **First cohort analysis** | Review all funnel metrics (table below) |

**Day 13–14 diagnostic framework:**

| Metric | Stop and Fix | Proceed |
|---|---|---|
| Demo slider interaction rate | <30% of visitors | >50% |
| Decision completion rate | <20% of starters | >40% |
| Signup conversion from completion | <25% | >40% |
| Template usage (vs. blank canvas) | <40% | >60% |
| 7-day return rate | <10% | >20% |

**If any metric hits the "Stop and Fix" column:** Pause all outbound marketing. Diagnose and fix the top 3 friction points. Do not resume growth efforts until metrics cross the "Proceed" threshold. The launch window is ~14 days — wasted traffic doesn't come back.

### Weeks 3–4 (Rest of Month 1): Post-Launch Iteration

| Ship By | Feature |
|---|---|
| Day 18 | Methodology trace v1 (collapsible panel with full breakdown) |
| Day 22 | Scenario modeling v1 (single-slider sensitivity + tipping point indicator) |
| Day 25 | Criteria reuse from past decisions |
| Day 28 | Email-based view-only decision sharing (with DecideIQ branding + CTA) |

**Month 1 targets:** 1,000–2,000 registered accounts. 3,000–5,000 decisions completed. 5+ usable testimonials from beta cohort. Top 3 friction points identified and resolved.

### Month 2 (May 2026): Activate Monetization

**Week 1:** Turn on paid Pro tier at $19/month.
- Founding Members: "Your 6 months free Pro starts now. Lock in $15/month annual rate before [date]."
- Free tier limits enforced: 5 decisions/month, 2-model cap, 6-criteria cap, 90-day history expiration.

**Weeks 2–4:** Ship multi-model v2 (add Gemini, adversarial mode, confidence calibration). Ship 6 industry templates. Begin outcome tracking v1.

**Month 2 targets:** 3,000–4,000 active users. 150–250 Pro subscribers (5–7% conversion). MRR: $2,850–$4,750.