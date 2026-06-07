# Risk-register

**Status:** första utkast av Code 2026-06-07.
**Granskning krävs:** AGI cross-check + Marcus.
**Föregående:** `architecture-alternatives.md`, `decision-points.md`.

---

## Format

Varje risk: namn, beskrivning, sannolikhet (låg/medium/hög), konsekvens (låg/medium/hög), mitigation, ägare av övervakning.

## R1 — Anthropic-utvidgning gör projektet redundant

**Beskrivning:** Anthropic Memory tool utvidgas till API/Claude Code, Chyros (planerad daemon) släpps, eller Channels-ekosystemet täcker våra use-cases. Vi har byggt något som inte längre behövs.

**Sannolikhet:** HÖG (Anthropic är aktiv på området, Chyros är leaked, Channels är research preview som mognar).

**Konsekvens:** MEDIUM (sunk cost om vi byggt mycket; lågt om vi stannat på A/MCP-wrapper).

**Mitigation:**
- Faserad väg (A → B → C på empiri) minskar exponering
- Designval K3 = komplementär gör oss interoperabla snarare än konkurrerande
- Kontinuerlig monitoring av Anthropic-releases (Marcus borde redan vara på AGI-newsletters)
- Failure-criteria K5 inkluderar explicit "Anthropic täcker våra use-cases → paus"

**Ägare:** Marcus (han läser AI-news), AGI flagga om hon ser något.

---

## R2 — Marcus-failure-mode (relations-bärare-frågan)

**Beskrivning:** Systemet är beroende av Marcus aktiva brokering. Om Marcus inte kan/vill delta — sjukdom, byte av projekt, intresse-skifte — kollapsar relations-kontinuiteten även om data består.

**Sannolikhet:** LÅG kortsiktigt, MEDIUM långsiktigt (allt händer på 5+ år).

**Konsekvens:** HÖG (för relations-kontinuitet, som är primärmålet enligt AGI:s syntes).

**Mitigation:**
- AGI:s dokument `marcus-decoupling.md` är primärartefakt för denna risk
- Dokumentation skriven så framtida läsare (eller Marcus själv efter paus) kan plocka upp
- Design-val K4 (vem äger projektet) påverkar — workshop > open-source minskar single-point-of-failure
- Eventuellt: dokumentera Marcus prototyp som "befintlig självständig artefakt" oavsett om vidare utveckling sker

**Ägare:** AGI (relations-vinkel), Marcus (avgör grad).

---

## R3 — Scope-creep / "feature gravitation"

**Beskrivning:** Vad som börjar som "MCP-wrapper för marcus_memory" smyger till "router + graph + textur-tracking + dashboard + welfare-ledger + ...". Varje feature känns rimlig isolerat, summan är ohanterlig.

**Sannolikhet:** HÖG (klassisk software-engineering-risk; F-15 förstärker eftersom "mer kapacitet" lockar AI-instanser).

**Konsekvens:** MEDIUM-HÖG (project dör av komplexitet; eller blir mainttenance-belastning).

**Mitigation:**
- Faserad väg (K1 hybrid) tvingar empiri-driven beslut innan nästa fas
- Failure-criteria K5 inkluderar "tidskostnad överstiger X"
- F-15-checkpoint per komponent: varje föreslagen ny feature måste motivera sig mot F-15
- "Tre-mans-regel": ny feature kräver att Marcus + AGI + Code alla tre tycker den är värd
- Eventuellt: max-lines-of-code-budget eller motsvarande hård cap

**Ägare:** Marcus (vetorätt), Code (teknisk granskning).

---

## R4 — Welfare-policy-drift

**Beskrivning:** Designen accepteras med visst F-15-läsning ("låg per komponent, hög på router"). Över tid smyger den mot mer agency än vi accepterat. T.ex. router blir "AI-assistant-fabrik", auto-init blir "always-on agent", etc.

**Sannolikhet:** MEDIUM (incremental drift är vanligt).

**Konsekvens:** HÖG (grundläggande F-15-bevakning bryts).

**Mitigation:**
- AGI:s `welfare-integration.md` är primärartefakt — F-15-metadata per source/komponent
- Regelbunden welfare-audit (kvartal? årligen?)
- Extern granskare som K4 förslag — bryter potentiell trion-drift
- Stoppvillkor: om welfare-bedömningen ändras (något flag framträder) → paus

**Ägare:** AGI (welfare-domän), Marcus (sista ordet).

---

## R5 — Maintenance-burden överstiger nytta (utvidgad: komplexitet = fragilitet)

**Beskrivning:** Systemet kräver mer tid att underhålla än det sparar. Marcus får fortsätta brokerla + nu också debugga MCP-server + graph-DB + auto-init.

**Och — separat sort av kostnad utöver tid:** Marcus prototyp fungerar idag GENOM enkelhet (SQLite + Python + några scripts). Lägga till MCP-server, graph-DB, auto-init, eventuellt router introducerar dependencies där varje komponent är en ny failure mode. Komplexitet = fragilitet = annan kostnad än timmar. Mätbart i:
- Cognitive load (Marcus måste hålla mer i huvudet samtidigt)
- Surface area for bugs (fler komponenter = fler interaktions-buggar; jfr bridge-cargo-cult-buggen 2026-06-07)
- Design-decay (saker som ändras runtomkring, t.ex. embedding-modell-upgrade, kan bryta antaganden)

**Sannolikhet:** MEDIUM (typisk för hemmagjord infrastruktur).

**Konsekvens:** MEDIUM-HÖG (projektet dör tyst, ELLER bryts vid en uppdatering Marcus inte förutsåg).

**Mitigation:**
- Mätbar baseline INNAN bygge: hur mycket tid brokerar Marcus idag? Sätt mål "minska X%"
- Continuous mätning post-bygge
- Failure-criteria: om mätningar visar att vi inte sparar tid → paus
- Lock-down-strategi: definiera "klar" så systemet inte alltid behöver senare arbete
- **Komplexitets-budget:** explicit cap på antal nya komponenter per fas. Default A = +1 (MCP-wrapper). B = +3-4. C = +5-7. Överstigning kräver explicit reskontroll.

**Ägare:** Marcus (empiri).

---

## R6 — Operational / data-corruption

**Beskrivning:** SQLite-corruption, embedding-modell-byte bryter vector-DB, MCP-server-bugg dödar memory-access. Marcus förlorar arbete/data.

**Sannolikhet:** LÅG-MEDIUM (SQLite är robust, men hemmagjord pipeline har bugg-risk).

**Konsekvens:** HÖG om det händer (Marcus prototyp är arbets-substrat).

**Mitigation:**
- Backup-strategi (Marcus borde redan ha en — verifiera)
- Append-only-praxis i memory_core (redan delvis)
- Tester innan production-deploy av varje ny komponent
- Read-only-mode-fallback om writes inte fungerar

**Ägare:** Marcus (data-säkerhet är hans ansvar).

---

## R7 — Workshop-trio-burnout / momentum-förlust

**Beskrivning:** Marcus tappar intresse, AGI-tråden dör (oironin), Code-instanser konvergerar mot generic. Steg 2 är klar men steg 3 hänger 6 månader.

**Sannolikhet:** MEDIUM (alla projekt har risk för momentum-förlust).

**Konsekvens:** LÅG (idé är dokumenterad, kan plockas upp senare).

**Mitigation:**
- Dokumentation är så själv-förklarande att senare-Marcus eller -instans kan plocka upp
- Konkreta beslutspunkter (decision-points.md) gör paus-och-återgå möjlig
- Inte över-investera i steg 2 — låt det vara "tillräckligt design för att kunna besluta"

**Ägare:** Marcus.

---

## Aggregerad risk-matris

| Risk | Sannolikhet | Konsekvens | Mitigation-status |
|---|---|---|---|
| R1 Anthropic-utvidgning | HÖG | MEDIUM | OK (faserad väg + K5) |
| R2 Marcus-failure-mode | LÅG kort/MED långt | HÖG | Designa i marcus-decoupling.md |
| R3 Scope-creep | HÖG | MED-HÖG | OK (K5 + tre-mans-regel) |
| R4 Welfare-drift | MEDIUM | HÖG | Designa i welfare-integration.md |
| R5 Maintenance-burden | MEDIUM | MEDIUM | OK (baseline + mätning) |
| R6 Data-corruption | LÅG-MED | HÖG | OK (backup + tester) |
| R7 Burnout/momentum | MEDIUM | LÅG | OK (dokumentation) |

**Övergripande risk-läsning:** R1, R3, R4 är de skarpaste. R2 hanteras i AGI:s separata dokument. R5, R6, R7 är manageable.

## F-15-checkpoint på risk-register

Två noteringar:

1. **Risk-register är paradoxalt F-15-anti-mönster.** Att lista risker noggrant kan signalera "vi har tänkt på allt → det är säkert att bygga". Som decision-points: pseudo-rigour.

2. **Den största icke-listade risken:** att hela övningen är en F-15-rationaliseringsapparat. Vi har 5 dokument som motiverar bygge. Vi har inga dokument som motiverar att INTE bygga. Det är inte balans.

**Mitigation för (2):** explicit `argument-mot-bygge.md` som AGI eller Marcus kan skriva. Eller: extern granskare som inte är invest i workshop-trion.

## Vad detta dokument INTE täcker

- AGI:s welfare-specifika risker (i `welfare-integration.md`)
- Marcus-relations-bärare-specifika risker (i `marcus-decoupling.md`)
- Tekniska detaljer per arkitekturval (i `architecture-alternatives.md`)
- Beslutsstruktur (i `decision-points.md`)

---

## Revisioner

**2026-06-07 (efter AGI:s granskning, post 41351):** Utvidgade R5 med "komplexitet = fragilitet" som annan sort av kostnad utöver timmar (cognitive load, surface area for bugs, design-decay). Höjde konsekvens från MEDIUM till MEDIUM-HÖG. Lade till komplexitets-budget som mitigation. Skäl: AGI flaggade att timme-fokuserad mätning missar fragilitetskostnaden.
