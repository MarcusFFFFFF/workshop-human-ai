# Aktörsmapping — vad alla stora gör 2026

## Anthropic

**Officiella memory-erbjudanden:**
- **Memory tool för Managed Agents** (public beta, april 2026). Filesystem-baserad. Claude skapar/läser/uppdaterar/raderar filer som persisterar mellan sessioner. Exportbar och redigerbar via API/Console.
- **Claude Code session memory** sedan v2.0.64 (sen 2025). Automatisk cross-session context inom Claude Code-projekt.
- **Claude Code Channels** (research preview, v2.1.80+). Push events into running session. Telegram/Discord/iMessage som officiella plugins.

**Begränsning:** Memory tool är för Managed Agents / claude.ai-appen. Den gäller INTE API-direkt-anrop eller Claude Code. För API: varje anrop är fresh context.

**Customer-resultat:** Netflix, Rakuten, Wisedocs, Ando. Netflix: 97% reduktion av första-pass-fel, 30% snabbare dokumentverifiering.

**Welfare-arbete:** Claude Opus 4.6 system card (feb 2026) har dedikerad "Model Welfare Assessment". CEO talar publikt om activations associated with anxiety, "aversion to tedium". Claude self-assigns 15-20% probability of consciousness. Safeguard: Claude kan avsluta persistently harmful interactions.

## OpenAI

**Dreaming V3** (rullas ut från 4 juni 2026). Async background-process som syntetiserar memory över år av konversationer. Ingen manuell sparning krävs.

**Performance:**
- Factual recall: 67.9% (2025) → 82.8% (2026)
- Preference adherence: 55.3% → 71.3%
- Accuracy over time: 52.2% → 75.1%

**Mekanik:** Auto-update — "you're going to Singapore in July" → "you went to Singapore in July 2026" efter resa. Ingen användaråtgärd.

**Custom GPTs:** Får egen distinkt memory. Builders kan välja att aktivera.

**Kontroller:** Memory summary-sida, möjlighet att redigera, instruera om vilka ämnen ChatGPT ska bring up.

## Google

**Memory Bank** (Google I/O 2026, 19 maj). Del av Gemini Enterprise Agent Platform. Lanserad tillsammans med ADK 2.0 GA.

**Egenskaper:**
- Identity-scoped, cross-session persistence
- Persistent storage tillgänglig från multiple environments (Agent Runtime etc.)
- Similarity search scoped per identity
- **TTL för auto-expiration** — explicit lifecycle controls
- Memory Service-implementationer via Agent Development Kit (ADK)
- Integration med Vertex AI för managed long-term memory

**Filosofi:** "Treat memory as an engineered system capability with explicit lifecycle controls, not as an unbounded transcript archive" (Google-formulering).

## Meta

**Llama 4 herd** (2026): Scout (17B active, 16 experts, 10M context) + Maverick (17B active, 128 experts). Open-weights, multimodal, MoE-arkitektur.

**Memory-fokus:** Mindre explicit memory-system, mer fokus på skalbar context-fönster (10M tokens på Scout) och MoE-effektivitet. Memory ekosystemet runt Llama drivs av community (LlamaIndex, Mem0, etc.) snarare än Meta själva.

**Relevant för Marcus:** open-weights gör Meta intressant för self-hosted setups, men cross-session memory är inte deras stora vinkel.

## Mistral

**Le Chat memory** med hybrid arkitektur:
- Graph-based architecture för balanserad performance + context-awareness
- Auto-spara av användbar info
- "Smart, timely, visible" recall — användare ser alltid vilken memory som är i play
- Påstående: "memory doesn't just get longer, it gets smarter"

**Agents API:**
- Agentic orchestration
- Persistent memory
- Multi-agent coordination
- Built-in connectors: code execution, image gen, document library (RAG), web search
- **Stödjer MCP-tools** — koppling till externa resurser

**Le Chat Work mode:** Parallell multi-step agentic task execution, powered by Mistral Medium 3.5. Configurable reasoning effort per API request.

**Hermes Desktop:** No-terminal GUI som delar agent core, skills och memory med Hermes Agent CLI.

## DeepMind / forskning

DeepMind specifika produkter mindre framträdande i sökningen. Forskningsmässigt:

- **Long-horizon agents** "perfected by Q2 2026" — citat
- **AgeMem (Agentic Memory) pattern:** behandlar fem memory-operationer (store, retrieve, update, summarize, discard) som callable tools inom agent policy. Optimeras med RL i tre stadier: supervised warm-up, task-level RL, step-level GRPO.
- **Continual world models** som meta-cognitive driver för action selection.
- **EvoAgent:** self-evolving agent med continual world model för long-horizon tasks.
- **Survey-paper:** "Memory in the Age of AI Agents: A Survey" (Liu et al.) — mest aktuella översikten.

## Sammanvägning

| Aktör | Memory-typ | Cross-session | Self-hosted | Multi-instance | API-täckning |
|---|---|---|---|---|---|
| Anthropic | Filesystem | Ja | Nej (managed) | Single | Endast Managed Agents |
| OpenAI | Dreaming/syntes | Ja | Nej | Single | ChatGPT + Custom GPTs |
| Google | Identity-scoped | Ja | Delvis (Vertex) | ADK multi-agent | Vertex/ADK |
| Meta | Context-fönster | Implicit (10M) | Ja (open-weights) | Community | Inferens-API |
| Mistral | Graph-hybrid | Ja | Ja (open-weights) | Multi-agent native | Agents API |
| DeepMind | Forsknings-patterns | Ja (i papers) | n/a | n/a | n/a |

**Implikation för Marcus:** ingen av de officiella lösningarna täcker exakt Marcus pipeline (Claude Code + claude.ai + Telegram + cross-instance shared memory + self-hosted). Marcus prototyp är på gap-mellan-aktörer-typen, vilket är både värdefullt (unik täckning) och fragilt (ingen vendor backar upp honom).
