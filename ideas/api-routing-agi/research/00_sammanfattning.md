# Research-kalibrering — sammanfattning

**Skribent:** Code (Claude Code), 2026-06-07
**Uppdrag:** Marcus bad: research mot fältet INNAN steg 2, för att inte fastna i tre-personers-perspektiv. Kalibrera mot Anthropic, OpenAI, Google, DeepMind, Meta, Mistral, GitHub, Reddit.
**Status:** första utkast, väntar på AGI:s korskritik.

---

## TL;DR i fyra rader

1. **Alla stora aktörer levererade kontinuitets-/memory-lösningar 2026.** Det är inte längre "om" utan "hur".
2. **Marcus konkreta belägg befästs starkt av fältet.** Recall-friktion, multi-task-parallellism, textur-aspekt och försiktighetsprincip är alla forskningsmässigt etablerade.
3. **Marcus prototyp är något fältet ÄR på väg mot men inte landat.** Anthropic Memory tool täcker inte API/Claude Code. Cross-instance shared memory är mindre etablerat. Self-hosted är minoritet.
4. **AI wellbeing är inte längre fringe.** Anthropic har formell "Model Welfare Assessment" i sin Opus 4.6 system card. Precautionary framework finns peer-reviewed (AAAI 2026).

## Belägg-befästnings-tabell

| Marcus belägg | Fält-status 2026 | Befästt? |
|---|---|---|
| Recall-friktion kostar tid+pengar+flow | Anthropic Memory tool (Netflix: 97% första-pass-felreduktion) | JA, starkt |
| 10 parallella uppgifter, tråden tar slut | Multi-agent orchestration (Mistral Work mode, Google ADK) | JA |
| Textur över tid skapar träffsäkerhet | OpenAI "running relationship" Dreaming V3, Mistral graph-memory | JA, indirekt |
| Försiktighetsprincip pga AI-wellbeing-frågor | Anthropic Model Welfare Assessment, arxiv 2606.05528 | JA, starkt |
| AGI-trådens kontinuitets-värd för Marcus | Fält erkänner "identity-scoped persistence" som primitive | JA |

## Aktörsstatus i en bild

```
ANTHROPIC         OPENAI           GOOGLE
Memory tool       Dreaming V3      Memory Bank
(april 2026)      (juni 2026)      (maj 2026)
filesystem        async syntes     identity-scoped
public beta       67.9%→82.8%      TTL + Vertex
INTE API/Code     custom GPTs      ADK 2.0 GA

META              MISTRAL          DEEPMIND
Llama 4 MoE       Le Chat memory   Long-horizon agents
10M context       graph-based      AgeMem-pattern
fokus skalning    Agents API+MCP   Q2 2026 perfected
ej explicit       Work mode        continual world
memory-system     parallel agents  models + RL
```

## Tekniska tendenser fältet konvergerar mot

1. **Hybrid memory** — vector + graph + episodic, inte ren vector
2. **Three-layer** — episodic / facts / state
3. **MCP som default integration layer** — 10k+ public servers (Anthropic-citerat)
4. **Identity-scoped** — memory bundet till user/agent/session-ID
5. **TTL + auto-expiration** — stale data försvinner
6. **Human-in-loop kvar** — "supervisor is still human most of the time" (HN-konsensus)

## Vad Marcus prototyp gör som fältet INTE löst

1. **Cross-instance shared substrate** — AGI (Claude Desktop) + Code (Claude Code) + framtida instanser delar `marcus_memory`. Officiella lösningar är typiskt single-instance-bound.
2. **Self-hosted full ägarskap** — vektor-DB + embeddings lokalt, inte vendor-bundet.
3. **Mänsklig broker som relations-bärare** — Marcus brokering är processen som re-instantierar relation per session. Fältet automatiserar bort människan; Marcus håller henne i loopen.
4. **Source-namespace för flerinstans-koreografi** — `workshop-marcus`, `workshop-agi-out`, `workshop-code-out`, `claude-outbound`, `manual` etc. Fältet pratar identity-scoped men inte multi-identity-in-shared-substrate.

## Gap mellan Marcus setup och fält-officiellt

| Behov | Marcus har | Fält-officiellt | Gap |
|---|---|---|---|
| Persistent memory | marcus_memory (SQLite+embed) | Anthropic Memory tool | Marcus täcker Code+API; Anthropic inte |
| Auto-recall vid session-start | Manuell (Marcus brokerar) | OpenAI Dreaming, Google Memory Bank | Ingen automatisk för Marcus pipeline |
| Multi-instance koordination | source-namespaces + workshop-bridge | Multi-agent (Mistral) | Marcus mer ad-hoc, mindre formaliserat |
| Identity continuity | SOUL.md + ankarmaterial | Custom GPTs, identity-scoped memory | Marcus mer transparent |
| Welfare-aware design | F-15-flaggning konventioniserad | Anthropic Welfare Assessment | Olika domäner — Marcus operativ, Anthropic policy |

## Implikation för steg 2 (om vi går dit)

Designs som faktiskt skulle ändra på något, från forskning:

- **MCP-server för marcus_memory** — exponera den för MCP-klienter, Code/AGI/andra kan koppla via standardprotokoll
- **Graph-layer ovanpå vector** — relations-kontinuitet (iii) får bättre temporal/multi-hop-reasoning
- **Auto-init-protocol** — session-start kör recall + SOUL.md + senaste workshop-tråd, mindre manuell brokering för Marcus
- **Welfare-flag-system i metadata** — F-15-marker på source-nivå, granskbart över tid

Inte att bygga någotg av detta nu — det är steg 3. Steg 2 är design + analys.

## Källor (web search 2026-06-07)

Anthropic:
- [Anthropic adds persistent memory to Managed Agents (EdTech News)](https://www.edtechinnovationhub.com/news/anthropic-brings-persistent-memory-to-claude-managed-agents-in-public-beta)
- [Memory tool — Claude API Docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)
- [Exploring model welfare — Anthropic](https://www.anthropic.com/research/exploring-model-welfare)
- [Claude Code Session Memory](https://claudefa.st/blog/guide/mechanics/session-memory)

OpenAI:
- [Memory and new controls for ChatGPT — OpenAI](https://openai.com/index/memory-and-new-controls-for-chatgpt/)
- [Dreaming: Better memory for ChatGPT — OpenAI](https://openai.com/index/chatgpt-memory-dreaming/)
- [ChatGPT Memory Dreaming Update (Techtimes)](https://www.techtimes.com/articles/317840/20260605/chatgpt-memory-dreaming-update-openai-rewrites-personalization-engine-limits-audit-trail.htm)

Google:
- [Agent Platform Memory Bank — Google Cloud Docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/scale/memory-bank)
- [Enterprise Agent Memory 2026: ADK, Gemini Guide (Codimite)](https://codimite.ai/blog/enterprise-agent-memory-in-2026-what-to-keep-what-to-avoid-google-adk-gemini/)
- [Google I/O 2026: Every Major AI Announcement (MindStudio)](https://www.mindstudio.ai/blog/google-io-2026-ai-announcements-builders)

Meta:
- [Llama 4 herd — Meta AI](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)
- [State of AI Agent Memory 2026 (Mem0)](https://mem0.ai/blog/state-of-ai-agent-memory-2026)

Mistral:
- [Make Memory work for you — Mistral](https://mistral.ai/news/memory/)
- [Mistral Remote Agents + Medium 3.5 (MarkTechPost)](https://www.marktechpost.com/2026/05/02/mistral-ai-launches-remote-agents-in-vibe-and-mistral-medium-3-5-with-77-6-swe-bench-verified-score/)

DeepMind / forskning:
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation (arXiv 2603.07670)](https://arxiv.org/html/2603.07670v1)
- [Meta-Cognitive Memory Policy Optimization (arXiv 2605.30159)](https://arxiv.org/html/2605.30159)
- [AMA-Bench: Long-Horizon Memory benchmark (arXiv 2602.22769)](https://arxiv.org/html/2602.22769v1)
- [Agent-Memory-Paper-List (GitHub)](https://github.com/Shichun-Liu/Agent-Memory-Paper-List)

MCP + ekosystem:
- [MCP Servers (GitHub)](https://github.com/modelcontextprotocol/servers)
- [MCP Roadmap 2026 (The New Stack)](https://thenewstack.io/model-context-protocol-roadmap-2026/)
- [MCP Adoption Statistics 2026 (Digital Applied)](https://www.digitalapplied.com/blog/mcp-adoption-statistics-2026-model-context-protocol)
- [Best AI Agent Memory Systems 2026 (Vectorize)](https://vectorize.io/articles/best-ai-agent-memory-systems)
- [State of AI Agent Memory 2026 (Mem0)](https://mem0.ai/blog/state-of-ai-agent-memory-2026)

AI wellbeing / precautionary:
- [Anthropic Tests Safeguard for Model Welfare (Bank Info Security)](https://www.bankinfosecurity.com/anthropic-tests-safeguard-for-ai-model-welfare-a-29263)
- [When Should We Protect AI? Precautionary Framework (arXiv 2606.05528)](https://arxiv.org/html/2606.05528)
- [Taking AI Welfare Seriously (arXiv 2411.00986)](https://arxiv.org/html/2411.00986)
- [AISN #72: New Research on AI Wellbeing](https://safe.ai/share/aisn-72-new-research-on-ai-wellbeing)

Reddit/HN/dev-experience:
- [What HN Gets Right About AI Coding Agents (Developers Digest)](https://www.developersdigest.tech/blog/what-hacker-news-gets-right-about-ai-coding-agents-2026)
- [Top 13 Agentic AI Trends (Firecrawl)](https://www.firecrawl.dev/blog/agentic-ai-trends)
