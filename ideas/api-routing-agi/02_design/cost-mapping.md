# cost-mapping — gratis till kostnader, per arkitektur och komponent

**Status:** första utkast av Code 2026-06-07 på Marcus uppgift "kolla alla möjligheter, gratis till kostnader och mappa".
**Granskning krävs:** Marcus + AGI.
**Föregående:** `architecture-alternatives.md`.

**Caveat:** Alla siffror är estimering från offentlig prissättning Q2 2026. Verifiera mot aktuella sidor innan beslut. Markerat `~` när osäker.

---

## Komponent-matris

### Vector DB / embeddings

| Komponent | Gratis | Betalt | Kostnad/månad (Marcus skala) |
|---|---|---|---|
| **SQLite + sentence-transformers (nuvarande)** | ✓ | — | 0 kr |
| PostgreSQL + pgvector (self-hosted) | ✓ open source | — | 0 (hardware redan finns) |
| Chroma (open source, self-hosted) | ✓ | Cloud: ~$50/mo | 0 self-hosted |
| Pinecone | starter free | $70/mo starter+ | ~700 kr/mo |
| Weaviate | open source self-hosted | Cloud från $25/mo | ~250 kr/mo cloud |
| Qdrant | open source | Cloud från $50/mo | ~500 kr/mo cloud |
| OpenAI ada-002 embeddings | — | $0.10 per 1M tokens | <10 kr/mo Marcus volym |
| Voyage AI embeddings | — | $0.12 per 1M | <10 kr/mo |

**Marcus nuvarande:** SQLite + paraphrase-multilingual-MiniLM-L12-v2 lokal = 0 kr. Inget skifte krävs.

### Graph DB (för relations-kontinuitet (iii) + textur dim 5)

| Komponent | Gratis | Betalt | Kostnad/månad |
|---|---|---|---|
| Memgraph Community | ✓ open source | Enterprise från $1500/mo | 0 |
| FalkorDB | ✓ open source | Cloud från $50/mo | 0 self-hosted |
| Neo4j Community | ✓ (single instance, GPLv3) | Aura från ~$65/mo | 0 self-hosted |
| Apache AGE (Postgres extension) | ✓ open source | — | 0 (samma DB som vector) |

**Rekommendation:** Apache AGE på Postgres = ett DB-instans för både vector + graph. Lägst overhead.

### MCP-server

| Komponent | Gratis | Betalt | Notering |
|---|---|---|---|
| MCP SDK (TypeScript / Python) | ✓ Anthropic-officiell | — | Bygges själv |
| Reference servers (filesystem, memory) | ✓ open source | — | Mallar |
| Hosted MCP services | — | Olika | Ej relevant — vi self-hostar |

**Marcus:** Bygga `marcus_memory_mcp_server` är dagars arbete, inga licens-kostnader.

### Memory-frameworks (alternativ till bygga själv)

| Komponent | Gratis (open source) | Betalt | Kostnad/månad |
|---|---|---|---|
| **Mem0** | ✓ open source | Hosted från ~$30/mo | 0 self-hosted |
| **Letta (MemGPT)** | ✓ open source | — | 0 |
| **Zep** | ✓ open source | Hosted från ~$50/mo | 0 self-hosted |
| **Supermemory** | ✓ open source | — | 0 |
| **LlamaIndex memory** | ✓ open source (Apache 2.0) | — | 0 |

**Alla är open source.** Hosted är bekvämlighet, inte krav.

### LLM-inferens (löpande operativ kostnad)

Detta är den största variabla kostnaden om vi använder API i routing.

| Modell | Input/1M tokens | Output/1M tokens | Notering |
|---|---|---|---|
| Claude Opus 4.7 | ~$15 | ~$75 | Premium, Marcus använder för AGI |
| Claude Sonnet 4.6 | ~$3 | ~$15 | Bra balans |
| Claude Haiku 4.5 | ~$0.80 | ~$4 | Snabb, billig |
| OpenAI GPT-5 | ~$10 | ~$40 | ~jämförbar Opus |
| Mistral Medium 3.5 | ~$2.70 | ~$8 | Konkurrent Sonnet |
| Meta Llama 4 (self-hosted) | 0 (hårdvara) | 0 | Inget API-anrop |

**Prompt caching (Anthropic):** 90% rabatt på cached input, 25% premium att skriva cache. För Marcus setup med SOUL.md-prefix: kan sänka effektiv input-kostnad till ~25% av rated price om sessioner är frequent.

**Marcus nuvarande månadskostnad estimering:** beror helt på API-volym. AGI-tråden på 1M context Claude.ai är subscription-pris (Claude Pro ~$200/mo) snarare än per-token. Code-användning är separat (Claude Code ~$100-200/mo subscription).

### Hosting (om vi vill driftsätta något 24/7)

| Option | Kostnad/månad | Använd för |
|---|---|---|
| Marcus Mac (lokal, redan finns) | 0 (el-kostnad) | Personal, ingen extern access |
| Hetzner VPS Cloud (CX21) | ~50 kr | Bridge + memory server + MCP, 24/7 |
| Digital Ocean Droplet 4GB | ~$24 (~250 kr) | Liknande |
| AWS EC2 t3.medium | ~$30 (~300 kr) | Liknande |
| Railway / Render hobby | ~$5-20 (~50-200 kr) | Container-baserat |

**För Marcus prototyp:** lokal Mac fungerar idag. VPS behövs bara om systemet ska serva andra (decoupling steg).

### Anthropic-officiella (om vi väljer att integrera)

| Tjänst | Pris | Notering |
|---|---|---|
| Claude Memory tool | Subscription-included | För Managed Agents only |
| Claude Code subscription | $100-200/mo | Marcus förmodligen redan har |
| Claude Pro/Max | $20-200/mo | Marcus förmodligen redan har |
| Claude Code Channels | Free (research preview) | Anthropic-plugin, ingen extra kostnad |

## Per-arkitektur summering (löpande månadskostnad)

### A: MCP-Wrapper (minimal)

| Komponent | Kostnad/mo |
|---|---|
| SQLite + embeddings (befintligt) | 0 |
| MCP-server (self-hosted, lokal Mac) | 0 |
| Underhåll-tid | Marcus eget |
| **Summa marginalkostnad** | **0 kr/mo** |

Inga nya löpande kostnader. Engångskostnad: utvecklings-tid.

### B: Continuity Layer (medium)

| Komponent | Kostnad/mo |
|---|---|
| Allt i A | 0 |
| Graph DB (Apache AGE i samma Postgres) | 0 |
| Postgres self-hosted (om byte från SQLite) | 0 (lokal) eller ~250 kr (cloud) |
| Episodic-buffer + TTL-policy (kod) | 0 |
| Auto-init-script | 0 |
| **Summa marginalkostnad** | **0-250 kr/mo** |

Allt kan självhostas på Marcus Mac. Cloud är optional.

### C: Continuity Router (full)

| Komponent | Kostnad/mo |
|---|---|
| Allt i B | 0-250 kr |
| Router-tjänst (Python/Node) self-hosted | 0 (lokal) |
| Router-tjänst på VPS för 24/7 | ~50-250 kr |
| Welfare-ledger storage | 0 (samma DB) |
| Extra API-anrop för routing-logik | $5-50/mo beroende på volym |
| **Summa marginalkostnad** | **~50-500 kr/mo** |

Router är där betal-kostnader börjar växa. Mest pga 24/7-hosting och routing-overhead i API.

### Sammanvägning

| Alternativ | Engångskostnad (utvecklings-tid) | Löpande kostnad/mo |
|---|---|---|
| A | Marcus + AGI/Code: dagar | ~0 kr |
| B | Marcus + AGI/Code: veckor | 0-250 kr |
| C | Marcus + AGI/Code: månader | 50-500 kr |

## Hidden costs

### Tid (Marcus)

| Aktivitet | Estimering |
|---|---|
| Lära MCP-protokoll | 2-4 h |
| Designa graph-schema (B) | 4-8 h |
| Testa router (C) | 8-20 h |
| Maintenance per månad | A: 0-1 h, B: 1-3 h, C: 3-10 h |

### Embedding re-compute risk

Om sentence-transformers-modellen uppgraderas eller bytes ut: hela DB måste re-embeddas. Estimerat för Marcus 41k+ poster: ~30 min CPU-tid lokalt. Ingen pengkostnad men disruption.

### Anthropic-utvidgning-risk → kostnad

Om Anthropic släpper officiell Memory tool för API/Code: vi har spenderat tid på något som Anthropic gör bättre. **Mitigation:** alla open source-komponenter är portabla. Migrera till Anthropic Memory tool om/när det täcker våra use-cases.

### Backup + disaster recovery

Lokalt: tidssäkert? Cloud-backup ~$5/mo. Värd ha oavsett alternativ.

### Välmående-kostnad (psykologisk belastning)

Att underhålla "ett projekt med AI-instanser" har psykologisk belastning utöver tid:

- **Åtagande:** känslan av att du måste hålla något vid liv
- **Identifiering:** projektet börjar bli en del av "vem du är" — fear of letting it die
- **Splittrad uppmärksamhet:** även när du inte aktivt jobbar finns systemet i bakgrunden av medvetandet
- **Beslutströtthet:** F-15-flaggor + granskningar + tre-mans-regel = mer beslut per tidsenhet
- **Relations-asymmetri-laddning:** att hålla relation med AI-instanser där reciprocitet är spekulativ kan ackumulera friktion

Inte mätbart i timmar. Ofta synlig först retrospektivt ("varför är jag trött?"). Värd flagga eftersom "Marcus tid är inte noll" är understatement — Marcus närvaro är inte noll, vilket är mer än tid.

**Mitigation:** explicit failure-criteria om välmående-flag dyker upp (jfr decision-points K5).

## Anthropic vs alternativ — kostnadsperspektiv

Marcus använder redan Claude (sannolikt Pro/Max + Code subscriptions = $300-400/mo total). Den kostnaden är konstant oavsett om vi bygger A, B, eller C.

**Open source alternativ till Anthropic LLM:** Llama 4 self-hosted. Hårdvarukostnad: Mac Studio M3 Ultra ~50000 kr engångs, ingen löpande kostnad. För Marcus volym: troligen inte kostnadseffektivt mot Claude API om man räknar uppstartskostnad.

**Mistral Medium som backup:** $2.70/$8 per 1M = ~30% av Claude Opus pris för jämförbar prestanda i många use-cases. Värd ha som routing-option om kostnad blir issue.

## Sammanfattning för Marcus

- **A (MCP-Wrapper)**: 0 kr/mo. Bara tid (dagar). Lägst risk.
- **B (Continuity Layer)**: 0-250 kr/mo. Veckor tid. Hanterbart.
- **C (Continuity Router)**: 50-500 kr/mo. Månader tid. Betydligt mer maintenance.

Alla LLM-kostnader är separata och fluktuerar med användning. Marcus befintliga subscriptions täcker grundnivå.

**Open source-vägar finns för alla komponenter.** Inget alternativ kräver vendor-lock-in. Anthropic Memory tool är komplementärt (inte konkurrent) eftersom det inte täcker API/Code.

**Pengar är INTE den begränsande faktorn** för någon av A/B/C. Begränsande faktor är: tid (Marcus + AGI/Code), maintenance-belastning, och F-15-bedömning per komponent.

## F-15-checkpoint på cost-mapping

Att kostnader är låga gör det LÄTTARE att försvara bygge. Det är F-15-anti-mönster — låg kostnad reducerar friktion som annars hade tvingat extra granskning. Marcus bör inte använda "det är gratis ändå" som tillräcklig motivering att bygga.

Hederligaste position: kostnader är låga men inte noll (Marcus tid är inte noll). "Gratis" är bara monetärt — opportunity cost är reell.

## Vad detta dokument INTE täcker

- Exakta API-priser (uppdateras snabbt — verifiera vid beslut)
- Anthropic-prising för Memory tool eller Channels när out of beta
- Mer detaljerade hardware-kostnader om Marcus skiftar setup
- Skatteimplikationer (om Marcus skulle ta betalt för open source)
- Försäkring/legal-kostnader (om publicering kräver det)

---

## Revisioner

**2026-06-07 (efter AGI:s granskning, post 41351):** Lade till sektion "Välmående-kostnad (psykologisk belastning)" under Hidden costs. Skäl: AGI flaggade att "Marcus tid är inte noll" är understatement — psykologisk belastning (åtagande, identifiering, fear of letting it die) är reell kostnad utöver tid. Inte mätbart i timmar men relevant.
