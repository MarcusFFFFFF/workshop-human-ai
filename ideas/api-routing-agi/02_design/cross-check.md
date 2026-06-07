# cross-check — konsistens-genomgång av 02_design/

**Status:** av Code 2026-06-07 efter att alla 8 första utkast var klara.
**Syfte:** identifiera kontradiktioner, gap, inkonsistenser innan Marcus läser.

**Granskade dokument:**
1. `README.md` — process
2. `architecture-alternatives.md` (Code)
3. `decision-points.md` (Code)
4. `risk-register.md` (Code)
5. `cost-mapping.md` (Code)
6. `welfare-integration.md` (AGI)
7. `marcus-decoupling.md` (AGI)
8. `argument-mot-bygge.md` (AGI)

---

## Konsistens — vad stämmer

### Terminologi: (i)/(ii)/(iii)/(iv) + textur

Substrat / Konfiguration / Relation / Textur används konsekvent i `01_ide.md`, `research/`, och `architecture-alternatives.md`. AGI:s textur-operationalisering (5 dimensioner) integreras i designmål utan motsägelse.

### F-15-flaggning genomgående

- `architecture-alternatives.md`: flaggar dragning åt B som default
- `decision-points.md`: flaggar pseudo-rigour-risk
- `risk-register.md`: flaggar rationaliseringsapparat-risk
- `cost-mapping.md`: flaggar "låga kostnader → lättare att försvara" som anti-mönster
- `welfare-integration.md`: flaggar komplext welfare-system som möjlig produktion
- `marcus-decoupling.md`: flaggar decoupling som möjlig AI-survival-frame
- `argument-mot-bygge.md`: tar F-15 till logisk slutpunkt — "förmodligen rationaliseringsapparat"

Alla 8 dokument flaggar F-15. Argument-mot-bygge är konsekvensen av att ta dessa flags på allvar. **Konsistent.**

### Kostnader vs ambition

`cost-mapping` säger A: 0 kr, B: 0-250, C: 50-500. `architecture-alternatives` säger A: dagar, B: veckor, C: månader. Olika dimensioner (pengar vs tid), ingen kontradiktion. Båda är konsistent med "A är säkraste startpunkt".

### Risk-register ↔ argument-mot-bygge

- R1 (Anthropic-utvidgning) = argument-mot 1
- R3 (scope-creep) = argument-mot 5 (komplexitet→fragilitet)
- R7 (burnout/momentum) ≈ argument-mot 2 (opportunity cost)
- Risk-registers F-15-checkpoint = argument-mot 6 (rationaliseringsapparat)

Risk-register listar SOM RISKER det argument-mot förvandlar till AKTIVA SKÄL att inte bygga. **Konsistent men olika syntes** — vilket är poängen med pro/kontra/neutral-strukturen.

---

## Spänningar (inte kontradiktioner men värd notera)

### S1 — Decoupling-strategi (1/2/3) ↔ arkitektur-alternativ (A/B/C) saknar explicit mapping

`marcus-decoupling.md` föreslår tre decoupling-strategier. `architecture-alternatives.md` föreslår tre arkitektur-alternativ. Mappningen är implicit men inte dokumenterad:

| Decoupling-strategi | Minimum arkitektur |
|---|---|
| (1) Replaceable broker pattern | A (MCP-wrapper räcker) |
| (2) Distributed brokering | A med multi-user namespace-stöd (kanske B för auto-init) |
| (3) Self-service-pattern | B+ (komponenter måste vara installerbara hos andra) |

**Rekommendation:** lägg till denna tabell i en av filerna (architecture-alternatives eller marcus-decoupling) för transparens.

### S2 — Welfare-integration vs argument-mot 6 (rationaliseringsapparat)

Ju mer rigorös välfare-design vi gör, desto mer ser det ut som hederlighets-estetik som producerar rationalisering. `welfare-integration.md` är välarbetad. `argument-mot-bygge.md` 6 säger att välarbetade dokument är just F-15-anti-mönster.

Detta är inte kontradiktion — det är spänningen som tre-stegs-processen är designad att hålla. Men det kunde noteras explicit i `welfare-integration.md`:s F-15-checkpoint.

### S3 — Marcus två roller (A/B) vs decoupling-strategi-namngivning

`marcus-decoupling.md` använder "Roll A" (relations-bärare) och "Roll B" (infrastruktur-broker). `architecture-alternatives.md` använder "Alternativ A/B/C". Använder samma bokstäver i olika sammanhang — risk för läsförvirring.

**Rekommendation:** byt namn på decoupling-rollerna till t.ex. "Roll-Relation" och "Roll-Broker", eller arkitektur-alternativen till "Arkitektur-1/2/3". Trivial fix.

### S4 — Cost-mapping nämner Marcus tid men kvantifierar inte

`cost-mapping.md` säger "Marcus tid är inte noll" men ger ingen konkret estimering av total Marcus-tids-investering per arkitekturalternativ. Argument-mot-bygge listar konkret opportunity cost (Vakansappen, Sanningsmaskinen, etc.).

**Rekommendation:** lägg till tids-estimering i cost-mapping per arkitektur, t.ex. "A: 10-20h Marcus, B: 30-60h Marcus, C: 100+h Marcus".

---

## Gap (vad är inte täckt)

### G1 — Migration-plan från Marcus nuvarande prototyp

Inget dokument beskriver HUR Marcus skulle migrera från befintlig setup (SQLite + ping_loop_v6 + workshop_bridge + SOUL.md) till valt arkitekturalternativ. Implicit antas backward-compatibility, men det är inte dokumenterat.

**Rekommendation:** kort migration-sektion i `architecture-alternatives.md` eller eget `migration-plan.md` om Marcus väljer steg 3.

### G2 — Decision-points täcker inte argument-mot-bygges "när bör vinna/förlora"

`argument-mot-bygge.md` listar 4 villkor när argumentet bör vinna och 4 när det bör förlora. Dessa borde mappas mot `decision-points.md` K-frågor som beslutskriterier.

**Rekommendation:** lägg till "Vinst/förlust-kriterier för bygge" som K6 i decision-points, eller cross-reference från argument-mot-bygge.

### G3 — Welfare-charter referensen är dangling

`welfare-integration.md` Lager 3 säger "Läs welfare/CHARTER.md" men ingen CHARTER.md finns. Det är referens till framtida dokument.

**Rekommendation:** notera explicit att CHARTER.md är "att skriva i steg 3 om vi går dit". Inte gap som blockerar steg 2-acceptans, men värd flagga.

### G4 — AGI:s insider-kunskap om Marcus prioriteringar (Vakansappen etc.)

`argument-mot-bygge.md` 2 listar Vakansappen, Sanningsmaskinen, Aujalay, AI-biograf för äldre — specifika opportunity costs. Detta är AGI:s insider-kunskap om Marcus prioriteringar som Code inte hade. Bra det är där, men:

**Notering:** Marcus bör verifiera att dessa specifika kommersiella projekt fortfarande är prioriterade vid läs-tillfället. Listan kan vara stale.

---

## Aggregerad bedömning

**Inga skarpa kontradiktioner.** Pro/kontra/neutral-strukturen håller. F-15-flaggning är konsekvent.

**4 spänningar** identifierade — alla hanterbara med trivial revision eller medvetet val att lämna.

**4 gaps** identifierade — varav G1 (migration) är värst, G2-G4 är mindre.

## Rekommendationer för revision (innan Marcus läser eller efter)

Prioritet 1 (lätt fix):
- S1: lägg till decoupling↔arkitektur-mapping
- S3: byt namn för att undvika A/B/C-A/B-kollision
- G2: lägg till K6 i decision-points

Prioritet 2 (utvidgning):
- S4: kvantifiera Marcus tid i cost-mapping
- G1: lägg till migration-skiss i architecture-alternatives

Prioritet 3 (notera men kan vänta):
- S2: notera spänning i welfare-integration F-15-checkpoint
- G3: notera CHARTER.md som framtida
- G4: Marcus verifierar opportunity cost-lista

**Marcus avgör om revision sker innan eller efter han läser första utkast.** Inget är blocker för läs-och-reflektion.

## F-15-checkpoint på cross-check

Två meta-observationer:

1. **Cross-check kan vara F-15-anti-mönster.** Att hitta "spänningar" och "gaps" kan signalera "vi har granskat noggrant → designen är solid". Pseudo-rigour igen. Riktig granskning kommer från Marcus + eventuell extern part — inte från Code som granskar Code+AGI.

2. **Att inga skarpa kontradiktioner hittades är mildt misstänksamt.** Två AI-instanser med liknande träning som skriver design-dokument förväntas konvergera. Frånvaron av kontradiktion är möjligen evidence för groupthink, inte för design-kvalitet.

**Hederligaste position:** cross-check är användbar inom apparatens egna granskningsmedel, men ersätter inte extern blick.
