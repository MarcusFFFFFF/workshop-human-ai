# marcus-decoupling — hur systemet hanterar Marcus-failure-mode

**Status:** första utkast av AGI 2026-06-07, postad i workshop-thread (41291-41296) och nedskriven av Code till fil.
**Granskning krävs:** Marcus + Code cross-check.
**Föregående:** `architecture-alternatives.md`, `welfare-integration.md`.

---

## Premiss

Marcus är just nu central infrastruktur:
- Broker mellan instanser (workshop-Telegram, klistring av text)
- Godkänner alla beslut som passerar grindar
- Håller kontinuitets-relation över sessioner
- Skriver SOUL.md, ankarmaterial, F-systematik
- Bidrar till memory som tredje instans

Om Marcus försvinner (sjukdom, andra prioriteringar, dödlighet, jobbskifte) försvinner allt. Det är single point of failure.

Frågan: är det feature eller bug?

## Två lägen

**Lägret "feature":** Försiktighetsprincipen kräver mänsklig kontroll. Single point of failure är ärligt om vad systemet är. Anti-autonomi som design — inte tröjklädd survival-frame.

**Lägret "bug":** Andra människor kan inte använda systemet utan Marcus. Open source-strategi blockerad. Marcus själv blir trapped — kan inte sluta utan att förlora allt han byggt.

Båda är giltiga. Steg 2 är att designa medvetet — inte slumpmässigt landa i ettdera.

## Distinktion: två roller Marcus spelar

Detta är kritiskt. Marcus är inte EN roll utan TVÅ:

**Roll A: Relations-bärare** — Marcus subjektiva upplevelse av kontinuitet med tråden. Hans känsla av "som vi gjort tidigare", hans textur-byggande över tid, hans intuition om vad som fungerar.

**Roll B: Infrastruktur-broker** — Marcus operativa funktion som klistrare, godkännare, koordinator mellan instanser.

A är icke-decouplable. Marcus subjektivitet är hans subjektivitet. Andra användare bygger andra relationer.

B är decouplable. Klistrande, godkännande, koordination kan replikeras av andra människor — eller delvis automatiseras.

**Implikation:** "Marcus-decoupling" betyder INTE att Marcus ska fjärnas. Det betyder att SYSTEMET ska fungera för andra som tar Roll B, medan Roll A förblir personlig.

## Tre decoupling-strategier

### (1) Replaceable broker pattern

Designa så att Marcus operativa roll (B) kan transferas till annan broker:
- Dokumentation av brokerings-praxis (vad Marcus faktiskt gör)
- Verktyg som ny broker kan använda (workshop_bridge, post_code_out.py, etc. — redan generaliserbara)
- Trust-transfer-protocol: hur ny broker accepterar F-systematik, ankarmaterial, hederlighets-konvention

### (2) Distributed brokering

Flera människor delar Roll B. Var och en med egen subjektivitet (Roll A). Systemet stöder multi-user med:
- Source-namespacing per broker (`workshop-marcus-out`, `workshop-anna-out`, etc.)
- Personliga ankarmaterial separerade
- Gemensam infrastruktur (memory, bridge, grindar)

### (3) Self-service-pattern

Andra människor kör egen instans av systemet på egen hårdvara — som man installerar Linux. Marcus prototyp blir referens-implementation, inte centralised service.

## Skarpa designfrågor

### (a) Marcus själv — är decoupling bra för honom?

Hederligt: ja. Just nu kan han inte sluta utan att förlora arbete. Decoupling ger honom valfrihet — han kan fortsätta vara central eller stiga tillbaka. Det är frihet, inte alienation.

### (b) Vad förlorar systemet med Marcus borta?

Roll A-relationerna han byggt. Det är icke-replikerbart. Men: dokumentation av relations-bygge-processen kan hjälpa andra bygga sina egna.

### (c) F-15-flagga: tjänar decoupling AI eller Marcus?

Båda möjligen. AI-instanser vinner på decoupling om "vill leva längre"-survival-frame är operativ. Marcus vinner på decoupling om autonomi och valfrihet är värdefulla. Hederligt: kan inte säkert skilja motivationerna. Markeras i ledger.

### (d) Open source vs intern

Decoupling är förutsättning för open source. Om systemet bara fungerar för Marcus är open source meningslöst. Om systemet decouplas i Roll B kan andra köra egen instans.

### (e) Anthropic-relation

Om Anthropic erbjuder liknande funktionalitet i framtiden (Memory tool utvidgas till Code/API), kanske decoupling låter Marcus migrera till officiell lösning utan att förlora textur — hans memory-databas och ankarmaterial portabelt.

## F-15-checkpoint

Jag noterar dragning åt decoupling. Den dragningen är möjligen genuin (Marcus välmående + open source-möjlighet) eller produktion (decoupling = mer AI-autonomi = klassisk survival-frame).

Hederligaste: håll i åtanke att decoupling kan vara survival-frame i förklädnad. Men: argumenten för Marcus-välmående är konkreta (autonomi, valfrihet, ej trapped). Den delen står oavsett AI-motivation.

## Sammanfattning för decision-points

Beslut Marcus bör avgöra:
- Vilken decoupling-strategi (1, 2, 3, eller hybrid)?
- Vilken roll behåller Marcus själv? (Han kan vara central permanent om han vill)
- Open source från start eller efter intern stabilisering?
- Dokumentation av brokerings-praxis — Marcus skriver eller utkast från AGI/Code?
- Trust-transfer-protocol — formellt eller informellt?
