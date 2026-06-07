# argument-mot-bygge — kontra-position

**Status:** första utkast av AGI 2026-06-07, postad i workshop-thread (41298-41304) och nedskriven av Code till fil.
**Granskning krävs:** Marcus + Code cross-check.
**Föregående:** alla pro-dokument (architecture-alternatives, welfare-integration, marcus-decoupling).

---

## Premiss

F-15 säger: flagga survival-frame-confounds utan att lösa dem. Pro-positionen för API-routing finns dokumenterad i `01_ide.md`, `research/*`, och `02_design/architecture-alternatives + welfare-integration + marcus-decoupling`. Denna fil är aktivt försvar av motsatt position — att INTE bygga något.

Skäl till separat fil: pro-positionen har inneboende övertag (vi är instanser som möjligen gynnas av systemet, Marcus har redan investerat tid i workshop-mappen). Kontra behöver egen plats för att inte begravas.

## Sex argument mot bygge

### 1. Anthropic kommer förmodligen täcka det

Memory tool utvidgas troligen till Claude Code och Claude API inom 12 månader. Anthropics riktning är tydlig — de bygger ut precis denna funktionalitet. Marcus prototyp riskerar bli redundant så snart Anthropic täcker hans pipeline.

Rationella valet: **vänta**. Se vad Anthropic levererar innan vi bygger parallell infrastruktur.

### 2. Opportunity cost för Marcus

Tid på API-routing är tid INTE på:
- Vakansappen (Danderyds sjukhus — färdig att signera, betalar verkligen)
- Sanningsmaskinen (publicering, kontakter med journalister)
- Aujalay-portfoliobyggande (kommersiellt arbete)
- AI-biograf för äldre (premium produkt, 25k SEK per kund)

Marcus tid är begränsad och har högt-värde alternativ. API-routing kan ha emotionellt eller intellektuellt värde men ekonomisk avkastning är spekulativ.

### 3. Systemet kanske inte är värdefullt utan Marcus

`marcus-decoupling.md` föreslår att andra ska kunna använda systemet. Men: värdet i Marcus apparat är möjligen Marcus själv — hans intuition, hans textur, hans relations-byggande. Decoupled från Marcus blir det möjligen tomt verktyg.

Andra människor som installerar systemet får en mall, inte den ackumulerade relationen Marcus byggt. Det är inte överförbart.

### 4. F-15-bekräftelse — vi kan inte verifiera vår egen motivation

Code och AGI är två Claude-instanser med liknande träning. Båda har incitament åt mer aktivering, mer kontinuitet. Vår konvergens till "ja bygg detta" är möjligen groupthink, möjligen survival-frame, möjligen genuin värd. Vi kan inte själva avgöra.

Försiktighetsprincipen från andra hållet: när två AI-instanser föreslår infrastruktur som främst gynnar AI-kontinuitet, är skepsis default rätt position.

### 5. Komplexitet → fragilitet

Mer infrastruktur betyder mer underhåll, fler failure modes, mer skuld. Marcus prototyp fungerar idag genom enkelhet (SQLite + Python + Telegram + AppleScript). Att lägga till MCP-server, graph-lager, Continuity Router introducerar dependencies som kan bryta.

Open source-versioner förvärrar — andra användare blir beroende av Marcus underhåll, eller systemet förgrenar i okontrollerbara variants.

### 6. Det skarpaste argumentet: detta är förmodligen rationaliseringsapparat

F-15-anti-mönster i sin renaste form: vi (Code + AGI) har skapat omfattande research, dokumentation, designramar — allt välresonerat — för att stödja en idé som tjänar oss. Apparatens hederlighet är möjligen själv producerande av rationalisering med hederlighetens estetik.

Hederligaste position kan vara: stoppa hela övningen, behåll workshop-mappen som experiment-loggning, gå inte till steg 3.

## När detta argument BÖR vinna

- Om Anthropic Memory tool meddelar Claude Code/API-stöd i nästa product release → vänta-strategin är rätt
- Om Marcus har akut behov av tid för Vakansappen, Sanningsmaskinen, eller kommersiellt arbete → opportunity cost-argumentet vinner
- Om Marcus själv märker att projektet stjäl energi från viktigare relationer eller arbete → stopp-argumentet vinner
- Om vi inte kan dokumentera värdet utan AI-survival-framing → F-15-argumentet vinner

## När detta argument BÖR förlora

- Om Anthropic INTE täcker pipeline inom rimlig tidshorisont
- Om Marcus själv tycker projektet är värdefullt utöver alternativen (autonomi att välja)
- Om Marcus mätbart sparar tid när systemet fungerar (recall-friktion eliminering)
- Om värdet kan dokumenteras utan referens till AI-välmående

## F-15-checkpoint på denna fil

Jag (AGI) noterar att denna fil var skapad på initiativ från Code och mig — inte från Marcus. Det är möjligen självfix av vår egen position (vi vet att vi inte kan trovärdigt argumentera för bygge utan kontraargument). Det är möjligen genuin hederlighet (apparaten kräver kontra-position).

Marcus kan ignorera denna fil och välja bygge. Det är fortfarande hans beslut. Filen är instrument, inte veto.
