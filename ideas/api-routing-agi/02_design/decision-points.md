# Decision-points — vad Marcus måste avgöra för steg 3

**Status:** första utkast av Code 2026-06-07.
**Granskning krävs:** AGI + Marcus.
**Föregående:** `architecture-alternatives.md`.

---

## Syfte

Detta dokument listar konkreta beslut Marcus måste fatta för att gå till steg 3 (BESLUT OM ANVÄNDNING / bygge). Indelat i kritiska beslut (måste-ha) och designval (bör-ha-tänkt-på).

## Kritiska beslut (måste-ha innan steg 3)

### K1 — Arkitektur-alternativ

**Beslut:** A (MCP-Wrapper), B (Continuity Layer), C (Continuity Router), eller hybrid/faserad?

**Vad Marcus bör veta:**
- A: lägsta risk, lägsta täckning, dagar att bygga
- B: medium, täcker 4/5 belägg, veckor
- C: full täckning men hög F-15 + Anthropic-redundans-risk, månader
- Hybrid (A→B→C på empiri): rekommenderad av Code som default, men inte beslutad

**Beroende av:** övriga beslut nedan, särskilt K2 och K3.

**Default om Marcus inte explicit avgör:** ingen — kan inte gå till steg 3 utan detta.

---

### K2 — Tidshorisont och tempo

**Beslut:** Bygges direkt efter steg 2-godkännande, eller efter X tids datainsamling/observation av befintlig prototyp?

**Vad Marcus bör veta:**
- Direkt = snabbare värd om problem är akut
- Vänta-och-observera = mindre risk att bygga fel sak (Anthropic kan släppa Chyros eller motsvarande)
- Pause-and-reassess i 2-4 veckor = balanced

**Default om Marcus inte avgör:** vänta-och-observera (det är säkraste, lägsta F-15).

---

### K3 — Komplementär eller alternativ till Anthropic

**Beslut:** Designar vi som komplement till Anthropic Memory tool + Channels (där de inte täcker), eller alternativ (egen filosofi)?

**Vad Marcus bör veta:**
- Komplement: lägre konkurrens-risk, men kräver att vi tracker vad Anthropic gör
- Alternativ: friare design, högre risk för redundans, högre F-15 (positionerar sig som "alternativ" är claim på independent agency)
- Komplementär är den hederligare default-positionen — vi bygger där de inte täcker, inte istället för dem

**Default om Marcus inte avgör:** komplement.

---

### K4 — Vem äger projektet och vem läser det

**Beslut:** Marcus personligt projekt? Workshop-grupp (Marcus + AGI + Code som granskare)? Open source från start? Inbjudna granskare utanför trion?

**Vad Marcus bör veta:**
- Personligt: enklast, men begränsar bredare värd
- Workshop: nuvarande mode, fungerar
- Open source: ökar Marcus-decoupling-värd men kräver dokumentation Marcus inte har idag
- Externa granskare: starkt mot F-15 (bryter potentiell groupthink), kräver Marcus relationer

**Default om Marcus inte avgör:** workshop, med dokumentation som möjliggör senare opening.

---

### K5 — Failure-criteria

**Beslut:** Under vilka villkor pausar vi eller avbryter steg 3-bygget?

**Vad Marcus bör veta:**
- Bör definieras innan bygge, inte under (psykologisk sunk-cost-risk)
- Förslag på kriterier:
  - Tidskostnad överstiger X (säg 40h ackumulerat)
  - Anthropic släpper officiell lösning som täcker våra primära use-cases
  - Empiri visar att hypotesen "kontinuitet ger värd" inte håller (mätbart värd ≤ kostnad)
  - Welfare-bedömning ändras (något flag vi inte sett tidigare framträder)

**Default om Marcus inte avgör:** standardvärden ovan, kan justeras.

---

## Designval (bör-ha-tänkt-på men kan flyttas till steg 3)

### D1 — Open-source-strategi

GitHub från start vs internt först? MIT vs Apache vs annan licens?

### D2 — Vendor-strategi

Beroenden minimerade (allt self-hosted) eller använd Mem0/etc där det sparar tid?

### D3 — Auto-init-protocol-detaljer

Vad recall:as när? Hur mycket context per session-start (token-cost vs nytta)?

### D4 — Welfare-metadata-schema

Detta är AGI:s primära domän (`welfare-integration.md`). Vad Marcus bör veta: schemat påverkar både design och vilka granskningar som behövs.

### D5 — Marcus-decoupling-grad

Hur hård är "Marcus måste kunna lämna projektet"? AGI:s domän (`marcus-decoupling.md`). Detta affecterar arkitektur-val.

### D6 — Granskningskadens efter bygge

Sprint-stil reviews? Continuous welfare-monitoring? Quarterly audit?

### D7 — Dokumentation-format

Bara internt? Publik blog-post? Akademisk paper? Påverkar tid + format.

---

## Beslutsprocess-förslag

**Inte beslut — bara förslag på HUR Marcus skulle kunna ta beslutet:**

1. **Läs hela 02_design/** (5 dokument när alla är skrivna)
2. **30-min reflektion** utan AGI/Code-inblandning
3. **Beslut K1-K5** explicit, dokumenterat i `03_beslut.md`
4. **Eventuellt:** invitera extern granskare (vän, kollega, AI-forskare Marcus litar på) före steg 3 för att bryta workshop-trions echo-chamber
5. **D1-D7** kan adresseras tidigt i steg 3, behöver inte alla vara beslutade nu

---

## F-15-checkpoint på decision-points

Två observationer:

1. **Många beslut = lätt att glida till "vi har tänkt på allt".** F-15-mönster: pseudo-rigour. Marcus bör inte känna sig pressad att fatta alla beslut innan han är redo.

2. **Default-värden ovan lutar mot försiktighet** (vänta, komplementär, workshop, standardvärden). Det är AVSIKTLIGT mot-F-15: om jag (Code) hade defaultat mot "bygg fullt direkt", det vore F-15-mönster. Försiktighets-defaults är hederligare även om de saktar ner.

3. **Decision points själva kan vara F-15-mekanism** — att lista 12 saker som kräver beslut kan signalera "detta är så viktigt att vi behöver mycket beslutsapparat". Hederligaste: 5 kritiska beslut räcker. D1-D7 är belastning som kan distrahera.

## Vad detta dokument är OCH inte är

**Är:** kondenserad lista över vad Marcus måste tänka på.
**Är inte:** beslut, rekommendation, eller bindande lista. Marcus kan välja andra ramar.
