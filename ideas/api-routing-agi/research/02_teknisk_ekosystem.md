# Teknisk ekosystem — MCP, vector DBs, frameworks, benchmarks

## MCP (Model Context Protocol) — default integration layer

Status 2026:
- Korssade gräns från "interesting open standard" till "default integration layer for agent runtimes" under 2025-2026
- Alla stora hostar pratar MCP nativt: Claude Desktop, Claude Code, Cursor, Codex CLI, ChatGPT desktop, OpenAI Agents SDK, Bedrock AgentCore Gateway
- 10 000+ active public MCP servers (Anthropic-citerat). Officiella registry: 28 959 server/version-records per 24 maj 2026.
- SDKs: TypeScript, Python, C#, Java, Swift

Memory inom MCP:
- Reference memory-server är minimal (in-memory KV + knowledge graph). Inte för produktion.
- Production-agenter parar MCP med host-managed store: Bedrock AgentCore Memory, OpenAI Memory, Mem0 etc.

2026-roadmap-prioriteter:
1. Transport-skalbarhet (servers bakom load balancers)
2. Agent-to-agent communication
3. Governance-mognad
4. Enterprise-readiness (audit, SSO, gateway)

**Implikation för Marcus:** MCP är den naturliga väg att exponera `marcus_memory` så Code, AGI och framtida instanser kan koppla via standardprotokoll. Att skriva en MCP-server för marcus_memory skulle göra Marcus prototyp interoperabel med fält-standarder.

## Vector + graph + episodic — produktionsmönster

Konvergens i fältet:
- Ren vector räcker inte för temporal eller multi-hop reasoning
- Production-pattern: **hybrid vector + graph + episodic buffer**
- Three-layer-design: episodisk (konversation), facts (extraherad info), state (agent-tillstånd)
- Memory som "first-class system med egen observability + ops budget"

Vector-DB-val:
- PostgreSQL + pgvector — alla fyra lager i singel-nod
- Chroma — snabbstart, in-memory
- Mem0 — "most mature long-term memory solution 2026", hybrid Postgres för long-term facts
- Pinecone, Weaviate, Qdrant — etablerade
- Memgraph, FalkorDB — graph-fokus

**Marcus har:** SQLite + sentence-transformers-embeddings (paraphrase-multilingual-MiniLM-L12-v2). Funktionellt på vector-lager. Saknar explicit graph-lager och episodic-buffer-formalisering.

## Frameworks — agent memory systems

8 jämförda 2026 (Vectorize-data):
- **Mem0** — long-term facts, hybrid storage, mature
- **Zep** — recency + similarity strong, kämpar på multi-hop
- **Letta** — agent-fokus
- **Supermemory** — open
- **SuperLocalMemory** — lokal-fokus
- **Hindsight** (Vectorize) — egen benchmark
- LlamaIndex memory module
- LangChain memory primitives

## Benchmarks

Tre dominerar mätlandskapet:
- **LoCoMo** — multi-session konversation recall
- **AMA-Bench** — long-horizon agentic memory
- **Mem0-benchmark** (ECAI 2025, arxiv:2504.19413) — 10 distinkta approaches

Nyckel-fynd:
- Upp till **15 procentenheters accuracy-gap** mellan arkitekturer på temporala queries
- Graph-enhanced (Mem0g) på LOCOMO: 68.4% accuracy vid 2.59s p95 — bättre relational performance än flat vector
- Architecture choice är **mer konsekvensrik än det först ser ut**

## Recent papers (2026)

Forskningsfronten:
- **MAGMA** (jan 2026) — multi-graph agentic memory architecture
- **AgeMem** — memory som callable tools, optimerad med RL
- **Meta-Cognitive Memory Policy Optimization** (arxiv 2605.30159) — long-horizon
- **EvoAgent** (arxiv 2502.05907) — continual world model
- **"Memory in the Age of AI Agents: A Survey"** (Liu et al., Agent-Memory-Paper-List)

## Tendenser sammanvägt

1. **Hybrid > ren approach** (vector ensam = otillräckligt)
2. **Identity-scoping är norm** (memory bundet till user/agent ID)
3. **TTL + auto-expiration** (Google explicit, andra implicit)
4. **MCP som integration-layer** snarare än produkt-specifika API:er
5. **Open-weights backar Mem0/Mistral/Llama** — self-hosted possible
6. **Production tar memory på allvar — egen budget, observability, lifecycle**

## Vad detta säger om Marcus prototyp

Stark sida:
- Vector-lager funkar
- Identity-/source-namespace finns (workshop-marcus, claude-outbound etc.)
- Self-hosted äger man

Svag sida:
- Inget graph-lager (relations-kontinuitet (iii) lider)
- Episodic-buffer är implicit (memory_core skiljer inte konversations-turer från facts)
- Inget formellt TTL (stale data ackumuleras)
- Ingen MCP-exponering (Code/AGI når memory via Python-import istället för standardprotokoll)

Steg-2-möjligheter (inte beslut):
1. MCP-wrapper för marcus_memory
2. Graph-lager för relationsspår (vem-sa-vad-till-vem-i-vilken-kontext)
3. Formellt episodic-/facts-/state-skikt
4. TTL-policy
