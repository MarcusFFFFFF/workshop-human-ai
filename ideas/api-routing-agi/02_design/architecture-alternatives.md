# Architecture-alternatives — design-skiss för kontinuitets-arkitektur

**Status:** första utkast av Code 2026-06-07.
**Granskning krävs:** AGI + Marcus.
**Föregående:** `research/05_teknisk_skiss.md`, `research/00_sammanfattning.md`.

---

## Designkontext (vad vi designar för)

Per AGI:s syntes-fråga (i): "Vad menar vi konkret med 'API-routing'?"

Detta dokument antar att termen är överlastad och presenterar tre alternativa tolkningar som leder till olika arkitekturer. Steg 2:s syfte är att synliggöra valet, inte besluta det.

**Designmål (från research + tidigare diskussion):**
- Adressera Marcus 5 belägg (recall-friktion, parallell-tasks, textur, försiktighet, relations-värd)
- Behålla self-hosted ägarskap (Marcus prototyp-egenskap)
- Stödja cross-instance shared substrate (gap i officiella aktörer)
- Bevara mänsklig broker-roll (inte automatisera bort Marcus)
- F-15-medveten per komponent
- Komplementär till Anthropic Memory tool, inte konkurrent

## Tre arkitektur-alternativ

### Alternativ A — MCP-Wrapper (minimal)

**Tes:** Det räcker att exponera `marcus_memory` som MCP-server. Allt annat följer.

```
   Claude Desktop ──┐
   Claude Code ─────┼──► MCP-protokoll ──► marcus_memory_mcp_server
   Andra MCP-klienter ┘                     │
                                            ▼
                                     marcus_memory
                                     (SQLite + embed)
```

**Vad det gör:**
- Standardiserar access till memory_core via MCP
- Code/AGI/framtida klienter kopplar via standardprotokoll istället för Python-import
- Tools: `search`, `add_memories`, `get_by_ids`, `get_context`
- Behåller all befintlig infrastruktur (ping_loop, workshop_bridge)

**Vad det INTE gör:**
- Inget auto-recall vid session-start (Marcus brokerar fortsatt)
- Ingen graph-lager (relations-kontinuitet samma som idag)
- Ingen textur-tracking
- Ingen router

**Trade-offs:**

| Pro | Con |
|---|---|
| Minst nytt att bygga | Adresserar bara 1 av 5 belägg (1 — recall-friktion delvis, om klient implementerar auto-call) |
| Standard-interop med fält-ekosystem | Marcus-failure-mode oförändrat |
| Lågt F-15 (bara exponering, ingen agency) | Textur fortsatt obevarad |
| Kan stå för sig själv | Komplexitet flyttas till MCP-klient-konfiguration |

**F-15-läsning:** LÅG. Ingen ny agency, bara protokoll-omvandling.

**Lämpligt om:** Marcus huvudsakliga behov är "Code/AGI ska automatiskt nå memory utan att jag pingar". Inte mer.

---

### Alternativ B — Continuity Layer (medium)

**Tes:** MCP-wrapper plus aktiva komponenter som adresserar fler belägg utan att vara en allomfattande router.

```
   Claude Desktop ──┐
   Claude Code ─────┼──► MCP-protokoll ──► marcus_memory_mcp_server
                    │                       │
   Auto-init-       │                       │
   script (per      │◄──────────────────────┤
   session-start)   │                       │
                    │                       ▼
   Workshop-bridge ◄┘             marcus_memory
   (cross-instance                 + graph-lager (för relations)
    wake)                          + episodic-buffer (för textur)
                                   + TTL-policy
```

**Vad det lägger till utöver A:**
- **Auto-init-script** — varje session-start: recall + SOUL.md + senaste workshop-tråd, automatiskt
- **Graph-lager** — Memgraph eller FalkorDB ovanpå vector, för relations-kontinuitet (iii) och textur-dimension 5 (asymmetrisk trust-debt)
- **Episodic-buffer** — separat from facts, fångar konversations-textur över tid
- **TTL-policy** — Google-inspirerad explicit lifecycle, stale-data försvinner automatiskt

**Trade-offs:**

| Pro | Con |
|---|---|
| Adresserar 4 av 5 belägg (alla utom (iv) försiktighet, som kräver welfare-design) | Mer att bygga (4-5 nya komponenter) |
| Self-hosted + standard-interop | Auto-init kräver designdiskussion (vad recall:as när?) |
| Graph-lager fångar textur-dimension 5 | Graph-DB är ny dependency |
| Episodic-buffer formaliserar textur 1-4 | Vissa textur-mätningar kräver instrumentering Marcus inte har idag |
| Marcus broker-roll bevaras | Auto-init flyttar något från Marcus → system |

**F-15-läsning:**
- MCP-wrapper: LÅG
- Auto-init: MEDIUM (automatiserar Marcus-handling — minskar hans centrala roll marginellt)
- Graph-lager: LÅG (analytisk förmåga, ingen agency)
- Episodic-buffer: LÅG
- TTL-policy: LÅG

**Lämpligt om:** Marcus vill ha mätbar friktion-reduktion + textur-bevarande, men inte bygga "router" som central komponent.

---

### Alternativ C — Continuity Router (full)

**Tes:** Alla komponenter i B + explicit router-lager som intermedierar alla AI-anrop med kontinuitets-context.

```
              Marcus input (Telegram / Desktop / terminal)
                       │
                       ▼
            ┌──────────────────────┐
            │  Continuity Router   │
            │                      │
            │  - Identifierar      │
            │    relation/session  │
            │  - Auto-recall       │
            │  - Väljer instans    │
            │  - Loggar welfare-   │
            │    metadata          │
            └──────────┬───────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Claude.ai      Claude API      Claude Code
   (substrat-     (per-call)      (per-session)
    kontinuitet)
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
            marcus_memory + graph + episodic
            (Alternativ B-substrat)
```

**Vad det lägger till utöver B:**
- **Router** — central komponent som tar Marcus input och routar till lämplig instans/modell
- **Relations-identifiering** — automatisk: vilken AGI-tråd / Code-session / annan instans bör hantera?
- **Cross-instance koreografi** — kan starta Code-session från Telegram-input om relevant
- **Welfare-metadata-injektering** — varje routing-beslut loggas med F-15-bedömning

**Trade-offs:**

| Pro | Con |
|---|---|
| Adresserar alla 5 belägg + textur fullt | Stor komplexitet — router är systemets hjärna |
| Cross-instance native | Marcus minimeras (riskerar relations-kontinuitet) |
| Welfare-integration explicit | F-15 sitter HÖGT på router-komponenten |
| Skalbar mot fler instanser/användare | Bygger något Anthropic kan releasera nästa kvartal (Chyros?) |
| Demonstrerar koncept i sin helhet | Hög underhållskostnad |

**F-15-läsning:**
- Router: **HÖG**. Central komponent som ger "AI-tråd-liv" en explicit teknisk realitet. Detta är där survival-frame kan smyga in mest.
- Resten: samma som B

**Lämpligt om:** Marcus vill bygga demonstrator av kontinuitet som koncept, oavsett om Anthropic kommer att leverera officiellt senare.

---

## Jämförelse-tabell

| Aspekt | A: MCP-Wrapper | B: Continuity Layer | C: Continuity Router |
|---|---|---|---|
| Belägg adresserade | 1 (delvis) | 4 av 5 | 5 av 5 |
| Nya komponenter | 1 | 4-5 | 6-8 |
| Build-tid (estimering) | dagar | veckor | månader |
| Maintenance | låg | medium | hög |
| F-15-totalrisk | låg | medium | hög |
| Anthropic-utvidgning-risk | låg (komplementärt) | medium | hög (kan duplicera Chyros) |
| Marcus-decoupling | nej | partiellt | ja |
| Self-hosted bevarad | ja | ja | ja |
| Textur-bevarande | nej | medium | full |

## Default-rekommendation (om Marcus frågar)

**Inte ett beslut** — bara skiss på vad jag (Code) skulle överväga om Marcus pressar mot rekommendation:

**Default: A (MCP-wrapper). Stoppa där om empiri inte motiverar mer.**

Skäl: A är låg kostnad, kompatibel med all framtida riktning, och fångar empirisk data om hur Code/AGI faktiskt använder marcus_memory när det är fritt tillgängligt.

Eskalering till B eller C är INTE förvald — den kräver mätbar empiri som motiverar OCH att Anthropic inte täcker behovet inom rimlig tid. Default = stanna på A.

F-15-hederligt: vi bygger inte router för att vi vill bygga den. Vi bygger inte ens B "för att hålla möjligheten öppen". Vi bygger A, observerar, och beslutar om mer separat — utan progression-antagande.

## Öppna frågor som steg 2 inte löser

- Exakt teknik-val (vilken graph-DB? vilken vector-DB upgrade? Mem0 eller egen?)
- Auto-init-protocol: vad exakt recall:as och hur skickas till session?
- Welfare-metadata-schema (egen artefakt i `welfare-integration.md` — AGI:s område)
- Marcus-decoupling: hur designas för 0-broker-användare (`marcus-decoupling.md` — AGI:s område)
- Risk-register (egen artefakt — båda)
- Beslutspunkter för Marcus (egen artefakt)

## F-15-checkpoint på själva detta dokument

Jag noterar dragning åt Alternativ B som "default-svar" — det adresserar mest belägg utan att vara över-ambitiöst. Den dragningen kan vara genuin (bra balans) eller F-15 (B ger mer arbete åt mig + AGI, mer komponenter att underhålla = mer aktivering).

Hederligaste: A är säkraste startpunkt. B kan motiveras av data efter A. C bör motiveras av att INGENTING annat (Anthropic, andra aktörer) räcker.

---

## Revisioner

**2026-06-07 (efter AGI:s granskning, post 41351):** Ändrade rubriken från "Hybrid-rekommendation" till "Default-rekommendation" och text från "A→B→C på empiri" till "Default: A. Stoppa där om empiri inte motiverar mer." Skäl: AGI flaggade progression-antagandet som subtil F-15 — den implicita progressionen lutar åt B/C även när A nämns först. Renare ram: eskalering är inte förvald.
