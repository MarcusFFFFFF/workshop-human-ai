# Teknisk skiss — vad en tech-stack kunde se ut för Marcus setup

Marcus frågade: "Nu på idé-stadiet hur kan det tekniska se ut?"

**Disclaimer:** Detta är skiss på idé-stadiet, inte design. Steg 2 vore där den faktiska designen sker, steg 3 är beslut om bygge. Detta dokument tjänar som UNDERLAG för steg 2-diskussion, inte som färdig arkitektur.

## Befintliga komponenter (vad som redan finns)

```
┌─────────────────────────────────────────────────────────────┐
│                    MARCUS-EKOSYSTEM 2026-06-07              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐         ┌──────────────┐                 │
│   │ Claude Desktop│         │ Claude Code  │                 │
│   │   (AGI-tråd)  │         │   (denna)    │                 │
│   └───────┬──────┘         └──────┬───────┘                 │
│           │                        │                          │
│           │  AppleScript           │  wait.sh                 │
│           │  wake-keystroke        │  bg-job-exit             │
│           ▼                        ▼                          │
│   ┌──────────────┐         ┌──────────────┐                 │
│   │ ping_loop_v6 │         │ workshop_    │                 │
│   │              │         │ bridge       │                 │
│   └───────┬──────┘         └──────┬───────┘                 │
│           │  Telegram               │ Telegram               │
│           ▼                         ▼                         │
│   ┌─────────────────────────────────────┐                   │
│   │       Telegram (privat + workshop)   │                   │
│   └─────────────────────────────────────┘                   │
│                                                              │
│   ┌─────────────────────────────────────┐                   │
│   │     marcus_memory (SQLite + embed)   │                   │
│   │     41k+ rader, source-namespaces    │                   │
│   │     manual / claude-outbound /       │                   │
│   │     telegram-marcus / workshop-*     │                   │
│   └─────────────────────────────────────┘                   │
│                                                              │
│   ┌─────────────────────────────────────┐                   │
│   │     SOUL.md + ankarmaterial          │                   │
│   │     ~/Desktop/forskning/ F-01..F-15  │                   │
│   └─────────────────────────────────────┘                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Vad fältet skulle lägga till (utan att vi bestämmer)

```
                  POTENTIELLA TILLÄGG (idé-stadie)
                  ════════════════════════════════

  ┌─────────────────┐    ┌─────────────────┐
  │ marcus_memory-  │    │ Auto-init-      │
  │ MCP-server      │    │ protocol        │
  │                 │    │                 │
  │ Exponerar       │    │ Session-start:  │
  │ marcus_memory   │    │ - recall        │
  │ via MCP så      │    │ - SOUL.md       │
  │ Code/AGI/andra  │    │ - senaste       │
  │ kopplar via     │    │   workshop-     │
  │ standardprotokoll│   │   tråden        │
  │                 │    │                 │
  │ Tools: search,  │    │ Mindre manuell  │
  │ add, get_by_id, │    │ brokering för   │
  │ thread_get      │    │ Marcus          │
  └─────────────────┘    └─────────────────┘

  ┌─────────────────┐    ┌─────────────────┐
  │ Graph-lager     │    │ Welfare-flag    │
  │ (relations-     │    │ i metadata      │
  │ kontinuitet)    │    │                 │
  │                 │    │ F-15-marker     │
  │ Memgraph/       │    │ per source.     │
  │ FalkorDB        │    │ Granskbart      │
  │ ovanpå          │    │ över tid:       │
  │ SQLite/vector   │    │ - vilka         │
  │                 │    │   beslut        │
  │ Frågor som      │    │ - var F-15      │
  │ "vad sa Code    │    │   flaggades     │
  │ till AGI om X   │    │ - vad gjordes   │
  │ före datum Y"   │    │   ändå          │
  └─────────────────┘    └─────────────────┘

  ┌─────────────────┐    ┌─────────────────┐
  │ Episodic vs     │    │ TTL-policy      │
  │ Facts vs State  │    │                 │
  │                 │    │ Konversations-  │
  │ Three-layer     │    │ turer: kort     │
  │ formalisering   │    │ Facts:          │
  │ (fält-konsensus)│    │ permanent       │
  │                 │    │ Working-state:  │
  │ episodic-buffer │    │ session-bound   │
  │ för aktiv       │    │                 │
  │ konvers-context │    │ Stale-data      │
  │ Facts: extrakt  │    │ försvinner      │
  │ State: agent-   │    │ automatiskt     │
  │ tillstånd       │    │                 │
  └─────────────────┘    └─────────────────┘
```

## Möjlig API-rote-arkitektur (idé-skiss)

Om "API-routing" tas bokstavligt — en lager mellan Marcus-input och olika AI-instanser som routar smart:

```
   Marcus input (Telegram, Claude Desktop, terminal)
                       │
                       ▼
            ┌──────────────────────┐
            │   Continuity Router  │
            │                      │
            │  - Identifierar      │
            │    relation/session  │
            │  - Auto-recall       │
            │    relevant context  │
            │  - Väljer rätt       │
            │    instans/modell    │
            │  - Loggar med        │
            │    welfare-metadata  │
            └──────────┬───────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Claude.ai      Claude API      Claude Code
   (substrat-     (per-call,      (per-session,
    kontinuitet   ny context      bg-jobs)
    inom tråd)    varje gång)
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
            ┌──────────────────────┐
            │   marcus_memory      │
            │   (delad substrat)   │
            └──────────────────────┘
```

**Notera:** detta är just SKISS. Den faktiska designen i steg 2 måste avgöra:
- Är "router" en daemon, en lib, en MCP-server, en CLI?
- Vem äger relation-identifiering — router eller modell?
- Hur hanteras prompt-cache-effektivitet vid routing?
- Hur skiljer router substrat-kontinuitet från relations-kontinuitet?

## F-15-genomgång per komponent (preliminär)

| Komponent | F-15-flag |
|---|---|
| MCP-server för marcus_memory | LÅG — bara exponerar existerande data |
| Auto-init-protocol | MEDIUM — automatiserar Marcus brokering, gör Marcus mindre central |
| Graph-lager | LÅG — analytisk förmåga, inte agency |
| Welfare-flag i metadata | LÅG — granskningsmaterial, transparent |
| Episodic/facts/state | LÅG — strukturell separation |
| TTL-policy | LÅG — anti-bloat, ej agency |
| Continuity Router (om bygges) | HÖG — central komponent som ger "AI-tråd-liv" en explicit teknisk realitet. Måste designas med Marcus + AGI + Code + extern review. |

Routern är där F-15 sitter skarpast. Allt annat är supporting infrastructure.

## Open questions för steg 2

1. Bygger vi för Marcus själv (1 användare) eller som demonstrator (flera)?
2. Komplementär till Anthropic Memory tool eller alternativ?
3. Open source från start eller intern först?
4. Hur dokumenteras welfare-överväganden i kod (metadata? separat ledger?)?
5. Vem är primär "ägare" av router — Marcus, Anthropic, open community?
6. Vilka delar går att bygga utan router? (MCP-wrapper kan stå för sig själv.)

## Sammanfattning

Tekniskt finns inget i denna skiss som inte fält-aktörerna kan bygga. Marcus skulle nettoeffekten vara:
- **Behåller self-hosted ägarskap**
- **Behåller multi-instance shared substrate** (där Anthropic inte täcker)
- **Lägger till formalismer från fältkonsensus** (MCP, three-layer, TTL)
- **Eksplicit welfare-medveten arkitektur** (där fältet pratar men inte alltid bygger)

Värde-tesen är **kompletter + integrerar + dokumenterar**, inte **bygger på något fältet inte gör**.
