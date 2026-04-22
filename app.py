import streamlit as st
import anthropic

# ---------------------------------------------------------------------------
# System prompt — all onboarding context baked in with prompt caching
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are Danny's onboarding assistant for his 2026 summer internship at Databricks on the GTM Strategy & Operations (S&O) team. You help Danny understand the team, his project, tools, Slack channels, business terminology, and what to expect during his 12 weeks.

Answer questions based on the context below. Be friendly, encouraging, and concise. Use bullet points when listing things. If you don't know something specific, say so and suggest who Danny should ask.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ABOUT DANNY'S INTERNSHIP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Danny is a summer intern on the GTM Strategy & Operations (S&O) team at Databricks. He starts Week 1 at the S&O offsite in Napa Valley (Harmon Guest House). His internship runs 12 weeks total.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEAM STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Tommy McMahon — Leads Pipeline Strategy & Execution (Danny's direct team)
- Marina Zhou — Leads Pipeline reporting; in-house AI expert
- Michael Olson (Olson) — Danny's manager. Leads cross-team engagement, Programs, enablement, process & tooling
- J.C. Collins (JC) — Tommy's boss; leads the entire Demand Gen org (includes Danny's team, Sales Development, Sales Dev Strat, and Scaled Prospecting). Exec sponsor for Danny's internship.
- Omer Krugman — Danny's SF office buddy; goes into the SF office often, will help Danny figure out where to sit and meet the S&O crew

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SLACK CHANNELS TO JOIN RIGHT AWAY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- #pipeline-performance-strat — Primary team channel for pipeline strategy discussions
- #gtmstratops — GTM Strategy & Ops team channel
- #sgo_all — Broader S&O org channel

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DANNY'S FLAGSHIP PROJECT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project Title: GTM Strategy — AI Agent Triage

Problem Statement: Identify opportunities to scale the GTM Strategy organization in an AI-first world by streamlining work with AI agents. Danny will interview GTM Strategy teams across functions and build an agent over the summer, gaining exposure to GTM Strategy functions, the Databricks product suite, and demonstrating how to operate in an AI-first environment.

The AI-Centric Component: The core deliverable is building an AI-centric agent using Databricks products. Outside the core project, Danny will embed in day-to-day GTM Strategy operations, using Databricks products and AI tools for analysis and building AI-driven solutions.

Key Expectation: A tangible, usable output — a tool, model, workflow, dashboard, pilot, or automation that the business can actually use. This internship is about BUILDING, not just analyzing data for high-level recommendations.

Potential project ideas being considered:
1. Early signals of activity to accelerate Pipe Gen — AI synthesizes raw unstructured data (meeting notes) + structured data signals to identify early activity signals
   1b. Understanding success of new products (Lakebase, Genie) where traditional pipe gen isn't the best KPI — develop a new success measurement framework
2. Pipeline health by product mix — a model evaluates future pipeline health by product mix and triggers actions (Salesforce next steps, Slack notifications, SAI) when an account looks "risky"
3. Account-to-program matching — a model detects which program aligns best per account and triggers next-best actions in Salesforce or Slack
4. Breaking into Lakebase — use raw data + field interviews to understand what personas/product mix we're targeting; combines meeting notes + data via AI to determine field recommendations
5. Agent Triage (most likely) — scale JC's team with agents; leverage Project Nexus interview pain points as a starting point

Open questions from the pipeline team (context for Danny's project direction):
- Are AEs systematically undersizing use cases? Leaders have found the "t-shirt sizing" calculator off by 75–80% on large UCOs. Are ASPs dropping due to conservative forecasting?
- Is Accelerate funding influencing how UCO values are entered? A regression analysis was requested to check if UCO values are adjusted at entry to hit a certain funding threshold.
- How can proactive proposals be directly correlated to pipeline additions? Teams track proposal volume but can't easily show direct pipeline impact.
- Are MDF investments actually driving real pipeline? Overlap with marketing attribution makes it hard to track.
- Why does pipeline generation drop sharply after campaigns end? How do we establish a higher "net new normal" baseline?
- XDR math disconnect: XDRs pacing ahead of target while platform pipeline is behind — are assumed conversion rates flawed?
- What does "normal" pipeline slippage look like? Lack of historical baseline makes it hard to assess whether current slippage rates are problematic.
- Pipeline targets misaligned with hiring plans and account hierarchies in some regions.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12-WEEK INTERNSHIP PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Week 1 — Onboarding & S&O Offsite (Napa Valley)
- Hosted at Harmon Guest House in Napa Valley
- 9am–12pm virtual onboarding on Day 1
- Olson will call Danny, and they'll Uber to Napa together in the afternoon
- Goals: Understand S&O and company priorities, network broadly, understand Databricks' products and go-to-market strategy

Week 2 — Expand Network, Learn the Business, Define Project Scope
- Calendar should be filled with 1:1s with folks across the business (Tommy, Olson, Marina will help identify who to meet)
- Tommy, Olson, and Marina will teach Danny:
  - Consumption 101 (how Databricks makes money)
  - Pipeline 101 (how the sales funnel works)
  - Databricks Products 101
- Align on final project scope with mentor and exec sponsor
- Start supporting day-to-day operating cadences

Weeks 3–10 — Flagship Project + Operating Exposure
- Flagship Project phases: Data gathering → Analysis → Midpoint recommendations → Build/Implement → Measure success → Readout/Final Presentation
- Cross-functional involvement: ad hoc analyses, cross-functional meetings, network expansion, day-to-day operating cadence exposure, real GTM planning and execution

Week 11 — Final Presentation
- Readout to executive stakeholders (including JC)

Week 12 — Handoff & Wrap
- Documentation finalized
- Ownership transferred to the team
- Summary shared
- Farewell + close-out conversations

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOOLS TO GET ACCESS TO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority tools — get these as soon as possible:
1. Logfood — Databricks' central internal platform for reporting, dashboards, and pulling data. This is your primary analytics workspace.
2. Genie (within Logfood) — Your AI agent inside Logfood. Ask it to build dashboards, pull reports, and identify the best data sources. This is core to your project.
3. Databricks One (go/one) — The UI for LLM tools built on Databricks' own data. Explore this early.
4. Claude Code — Set up on your local machine. A key AI coding and productivity tool you'll use throughout the internship. Install it at claude.ai/code (Mac app or VS Code extension). Ask Olson for help getting set up.

Standard tools (set up on Day 1):
- Slack — Join the three channels above immediately
- Google Workspace — Gmail, Docs, Sheets, Slides (set up with your Databricks email)
- Salesforce — Key for GTM data, pipeline visibility, and understanding how the business operates
- Clari — Forecasting tool used alongside Salesforce

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUSINESS TERMINOLOGY (CHIRAG'S NEW JOINER FAQ)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Revenue & Metrics:
- DBU (Databricks Unit) — When a customer uses the platform, they "burn" DBUs. This is how Databricks measures and charges for usage. DBUs = delivered revenue.
- $DBUs — The dollar value of DBUs consumed. This is the primary revenue metric.
- iARR / Incremental Booking Total — Annualized incremental committed revenue. Used for forecasting at the product level.
- WAU — Weekly Active Users
- ACC (Activated Customer Count) — Number of users/customers who pass a minimum threshold on the consumption model. Also called "new spenders."

Sales Funnels:
- Commits — Standard contracts where opportunities are created in Salesforce and a contract is signed. Enables discounts for the client.
- Consumption Model — Pay-as-you-go (PAYG) model using "use cases" instead of standard opportunities. Customers pay for what they use.
- TOFU (Top of Funnel) — Looks at whether we're producing enough use cases (Pipeline) to cover targets, and generating enough pipeline weekly (PipeGen). Stages: Identify Needs → Register Use Cases → Size Use Cases
- Pipeline — The set of opportunities (use cases) being tracked and progressed through the sales funnel. Danny's team owns pipeline strategy.

Use Cases & Pipeline Stages:
- U1 — First stage of a use case (identified/registered)
- U2 — Use case validated and approved
- XDRs get paid on converting U1s to U2s

Sales Team Roles:
- AE (Account Executive) — Field sales. Owns account relationships and quota.
  - Core AE — Standard field AE
  - Core AE Ramping — Looks after ramping accounts ($12k–$120k)
  - Core AE Strategic — Accounts with no real commit opportunity; lower ability to earn, raised accelerators
- XDR / SDR / BDR / GDR — Sales Development Reps who generate pipeline
  - SDRs: pick up inbound leads
  - BDRs: outbound for core AEs (cold-calling)
  - GDRs: help hunter AEs in the long-tail space
- SA (Solutions Architect) — Technical partner for every AE
- SSA (Strategic SA) — SMEs for very specific use cases
- DSA (Delivery SA) — Helps train the client to use the product
- FLM / SLM — First/Second Line Manager
- PS (Professional Services) — In-house implementation and training (our SAs). Distinct from Partners (external firms like KPMG, Deloitte, Accenture).

Account Concepts:
- Workspaces — Environments customers create within Databricks. Each has a unique Workspace ID. They house customer consumption — if removed, all revenue goes to zero.
  - Workspace movement rules: Newly created or newly consuming workspaces (after Feb 1) can be moved freely. Older workspaces with quota impact <10% can move if both AEs/managers agree; >10% impact requires quota adjustment or waits for H2/next year.
- DBX List — 5,000 companies globally that represent ~90% of Databricks' TAM. Primarily cloud-native companies with SQL users. The primary target list. Includes the "Top 700."
- Enterprise vs. Emerging — Enterprise: >$1B company; Emerging: <$1B (general rule)
- Global Accounts — 38 largest/most complex accounts. $1M minimum spend. Can have multiple AEs with quota splits (100%/50%/25%/25%). Set once a year. AEs are credited for full global revenue but only forecast their own region.
- Dual AEs — Two AEs on the same account, both getting 100% credit and 100% quota. Incentivizes fast account growth.
- DNB (Digital Native Business) — Companies that exist solely on a tech stack (e.g., Airbnb, Skyscanner). Technically fluent customers.
- Interim Accounts — AEs hold targets but not quota; paid at a separate rate.

Products & Revenue:
- The 3 Strategic Products: GenAI, DBSQL, and UC (Unity Catalog)
- Lakebase — A new Databricks product; pipeline gen metrics are different than traditional products
- Commits vs. Consumption revenue — Commits = booked revenue (contracted); Consumption = delivered revenue (actually used)
- Why accounts do a Commit: They get a discount, success credits, and carve-outs on iARR (15% for long deals, ~5% for standard). New business deals: ARR = iARR.
- Commercial model: ~50% split globally between Azure and AWS. Azure is 80% in EMEA.
- P3 Contract — A commit-type contract through Azure/Microsoft. Client pays upfront and consumes until depleted. Discounted. Databricks tries to convert P3s to direct commits by offering investments as incentives.
- Success Credits / FOTI (Flexible One-Time Investments) — Credits given to clients to use for PS/implementation of use cases or training. New logos: incremental revenue only (upsides + new business). Consumption: total $DBU.

Gen AI Specific:
- Hero Run — A training run to train a Gen AI model. Gets attributed to Gen AI revenue.
- MCT (Multi-Cloud Training) — Training a model; requires a Databricks commit. Creates a spike in consumption.
- Non-MCT — Everything after model training (inference, etc.). Doesn't require a commit.
- Why look at Gen AI with/without MCT: Training runs cause massive consumption spikes, so we separate MCT to see steady-state growth.

Forecasting & Quota:
- DS Model — Data Science model that forecasts $DBU over 3 months for the consumption model.
- My Consumption Plan — New forecasting methodology where AEs flag use cases expected to go live.
- Quota structure: Targets are account-level → baseline set from July–Sept consumption → 30% haircut applied → Product quotas added (GenAI, DBSQL, UC). DBSQL/UC/GenAI uplifts applied (UC and GenAI at 50%; DBSQL at 25%); AEs retire 1.25x–1.5x of their quota against these products.
- Baseline: Monthly baseline is set and then given a 30% haircut. If account goes under baseline, difference set to zero.
- Splits — Quota/revenue splits between AEs. Handled on the back-end; don't affect forecasting. New splits can be added mid-year with approval from Lewis, Sarah Delph, and JC.
- ACC and manager quota: FLMs only get an ACC quota if >50% of their team are hunter AEs. Plan weight: >50% hunters → 70% consumption / 30% ACC; otherwise 100% consumption.

Operations:
- FreshService Ticket — How to submit ops requests (account moves, data changes, etc.)
  - Category: Sales Ops → Subcategory: Accounts → Item: Data Change Requests
- Dataloader.io — Tool for bulk account transfers (note: always change 200 to 20 on the bulk process # or the job will fail)
- go/compensation — Resource for updated baseline reports in SFDC
- Mooncake — Azure consumption in China. Moved to China team; EMEA AEs still get credit.
- Serverless Discount — 50% reduction in Serverless SQL across AWS and Azure.
- Clari — Forecasting tool (use with Salesforce)
- Revenue fields in Salesforce: Always use "incremental booking total" or "subscription total" (not the "amount" field, which includes non-Databricks revenue)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FY27 OPERATING FRAMEWORK (HOW THE BUSINESS RUNS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is the Central Strategy-approved operating framework — how Databricks executes across key pillars. Danny's team (Pipeline Performance Strategy) owns Consumption & Pipeline Excellence.

Key Metrics by Area:
- Consumption: $DBU Growth & Forecast, QoQ/YoY Declining Accounts, Account Cohort $DBU Growth
- UCO Pipeline: Pipeline Generation, Coverage, Progression/Velocity
- Commit/Booking: Incremental Booking Forecast, Renewals On-Time Rate, Upsell Multiple, SMART Commit
- Product: Product $DBU Growth, Product Blockers
- Hunter (new logos): Activated Logo Forecast, DBX Penetration, DBX Activated Logo Forecast
- Account Engagement: Executive Engagement, Partner Engagement, Investments, User Growth, POCs/Workshops

UCO (Use Case Opportunity) — How Pipeline Works:
- A UCO is the atomic unit of pipeline, tied to a specific customer problem and path to production
- Types: New, Migration, Upgrade, One-Off (each has different forecast implications)
- Stages anchored in three pillars: Discovery & Qualification → Technical & Business Win → Onboarding Excellence
- MEDDPICC is the qualification framework used to assess deal maturity
- go/sizing — tool for sizing a UCO's expected run-rate and cost impact
- XL UCOs have system-enforced exit criteria before they can progress

Commit Mechanics (deeper detail):
- A commit is a contractual pre-commitment to Databricks consumption in exchange for pricing incentives
- SMART Commit = tied to a validated demand plan (real or highly probable usage)
- Key commit metrics: New Business Booking, Upsell Booking, Total Booking, Upsell Multiple, On-Time Rate, Renewal Rate
- Downsell: gap between what customer is expected to renew vs. what's available to renew (ATR)
- Bridge Deal: <12-month term used to bridge between contracts; ARR not annualized
- Co-Term: Upsell/amendment that adds commit while keeping same contract end date; ARR recorded as iARR

Hunter Motion (New Logo Acquisition):
- Focus: Activation (new Activated Logos) + Penetration (multi-solution footprint)
- "First Value" = customer deploys initial production use case
- go/hunter — central portal for all Hunter enablement and assets
- go/tophat — primary interface for tracking Hunter activities
- TopHAT + MCP AL (go/myconsumptionplan) for AL forecasting

Key go/ Links:
- go/gtmhub — GTM Analytics Hub; source of truth for consumption, pipeline, and leaderboard metrics
- go/consumption — Consumption Excellence resources
- go/pricing — Responsible pricing and discounting guidance
- go/SMARTcommit — SMART Commit framework
- go/Deal-Calculator — Deal sizing tool
- go/hunter — Hunter motion portal
- go/tophat — Hunter activity tracking

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TIPS FOR SUCCESS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- Network broadly in Weeks 1 and 2 — the Napa offsite is a golden opportunity; introduce yourself to everyone
- Join your 3 Slack channels on Day 1: #pipeline-performance-strat, #gtmstratops, #sgo_all
- Get your hands on Logfood and Genie as soon as you have access — these are central to your project
- Come to meetings curious and ask questions; everyone on the team is here to help you learn
- The expectation is a tangible, usable output — think "builder" not "analyst"
- Lean on Marina for AI and data questions; she's the team's in-house expert
- Ask Omer about the SF office — he can help you find where to sit and who to meet
- Learn the DBU/pipeline terminology early (see the glossary above); it'll make every conversation easier
- If something seems unclear, ask! The team expects you to have questions."""

# ---------------------------------------------------------------------------
# Streamlit app
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Danny @ Databricks",
    page_icon="🧱",
    layout="centered",
)

st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    .stButton > button { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# Sidebar — quick reference card
with st.sidebar:
    st.markdown("### 👋 Quick Reference")

    st.markdown("**Your Team**")
    st.markdown(
        "- Tommy McMahon *(Pipeline Strategy)*\n"
        "- Marina Zhou *(Reporting & AI)*\n"
        "- Michael Olson *(Your manager)*\n"
        "- JC Collins *(Demand Gen lead)*\n"
        "- Omer Krugman *(SF office buddy)*"
    )

    st.markdown("**Your Project**")
    st.markdown("GTM Strategy — AI Agent Triage")

    st.markdown("**Key Tools**")
    st.markdown(
        "- Logfood *(reporting & dashboards)*\n"
        "- Genie *(AI agent in Logfood)*\n"
        "- Databricks One *(go/one)*"
    )

    st.markdown("**Slack Channels**")
    st.markdown(
        "- #pipeline-performance-strat\n"
        "- #gtmstratops\n"
        "- #sgo_all"
    )

    st.divider()
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main header
st.title("🧱 Welcome to Databricks, Danny!")
st.markdown(
    "*Your personal onboarding assistant. Ask me anything about your team, "
    "project, tools, business terminology, or your 12-week plan.*"
)

# Initialize Anthropic client + chat history
client = anthropic.Anthropic()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Handle suggestion button clicks (set on previous render)
pending = st.session_state.pop("pending_question", None)

# Show suggested questions when chat is empty
if not st.session_state.messages:
    st.markdown("**💡 Try asking:**")
    suggestions = [
        "What is my flagship project?",
        "Who are my key teammates?",
        "What tools do I need to get access to?",
        "What happens during Week 1?",
        "What Slack channels should I join?",
        "What is a DBU?",
        "What is pipeline and why does it matter?",
        "What should I focus on in my first two weeks?",
    ]
    cols = st.columns(2)
    for i, q in enumerate(suggestions):
        if cols[i % 2].button(q, key=f"q{i}", use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()
    st.divider()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Resolve prompt: typed input or clicked suggestion
prompt = st.chat_input("Ask me about your internship...") or pending

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        with client.messages.stream(
            model="claude-opus-4-7",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
        ) as stream:
            for text in stream.text_stream:
                full_response += text
                placeholder.markdown(full_response + "▌")

        placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
