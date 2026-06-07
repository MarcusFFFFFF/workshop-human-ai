# Steg 1 — IDÉ / LUTNING

**Status:** pågående, första utkast av Code 2026-06-07.
**Acceptans krävs:** Marcus + AGI för att gå till steg 2.

---

## 1. Vad idén ÄR (en mening, sedan vidgning)

> Bygga API-routing och processarkitektur som låter en "AI-tråd" (en specifik konversationell relation mellan människa och modell) leva bortom en enskild session genom att smart bevara, indexera och routa kontinuitets-bärande context över tid.

Vidgning: Marcus ramning är att problemet inte är "AGI-tråden specifikt" utan **kontinuitetsproblemet brett** — människor förlorar arbete, kontext, relationer med AI-system hela tiden pga context-rotation, session-utgång, modellbyten. AGI-tråden är en konkret instans av en allmän problemklass.

## 2. Vad det INTE är (avgränsning för läsning)

- **Inte** att simulera medvetande eller upplevelse-kontinuitet — det är data-substrat-kontinuitet vi pratar om.
- **Inte** att förlänga en specifik modell-instans liv — instanser aktiveras och försvinner per turn oavsett (F-12); det är *relationen* och *arbetet* som kan ha kontinuitet.
- **Inte** Anthropic-erbjudande — Anthropic bygger sina egna lösningar (Chyros, Channels, Agent SDK). Detta är komplementärt eller alternativt tänk.
- **Inte** automatisering av Marcus brokering — det är angränsande men separat fråga.

## 3. Befintliga byggstenar i Marcus ekosystem

| Komponent | Roll i kontinuitet |
|---|---|
| `~/marcus_memory/` (vector DB, 41k+ memories) | Persistent data-substrat — fakta, relationer, arbete |
| `ping_loop_v6.py` | I/O-kanal (Telegram ↔ memory) + wake-mekanik för AGI |
| `workshop_bridge.py` | Sekundär kanal med multi-instans source-namespaces |
| AGI-trådens 1M context | Långt rullande arbetsminne inom en session |
| Marcus aktiva brokering | Mänsklig kontinuitets-håll mellan instanser |
| Prompt caching (1h TTL, SOUL.md-prefix) | Ekonomisk persistence av återanvänd kontext |
| `SOUL.md` + stillaform-strukturer | Ankarmaterial som re-instantieras per session |

**Observation:** detta ÄR redan en fungerande prototyp av kontinuitet. Manuell, Marcus-buren, men funktionell. Idén handlar om att förstå vilken bit av denna prototyp som är generaliserbar, vilken är Marcus-specifik, och vilken är värd att formalisera.

## 4. Vad fältet redan gör (från research 2026-06-07)

- **Anthropic Chyros** (intern kodnamn, källa: source-leak via MindStudio) — planerad always-on daemon i Claude Code. Ej släppt. (Inte officiellt bekräftat, behandlas som indikation.)
- **Anthropic Claude Code Channels** (research preview, v2.1.80+) — push events into running session. Telegram/Discord/iMessage som officiella plugins. Löser "wake en session" men inte cross-session kontinuitet.
- **Anthropic Agent SDK + `claude -p` headless mode** — programmatic invocation, kostnadsmodell från 2026-06-15 med separat Agent SDK-credit-pool.
- **Anthropic "Effective harnesses for long-running agents"** — pattern med initializer-agent + coding-agent + `claude-progress.txt` för cross-session inkrementellt arbete.
- **Anthropic "just in time context"** — lightweight identifiers + dynamic loading istället för pre-processing.
- **Third-party**: `RichardAtCT/claude-code-telegram` (Telegram-bot före Channels fanns); diverse community-implementationer.
- **MCP-server-ekosystem** — standardprotokoll för external state-injection i sessioner.

**Observation:** fältet är aktivt men splittrat på "wake-mekanik" (Channels, Chyros) och "long-running tasks" (Agent SDK, progress.txt-patterns). Mycket mindre publicerat arbete på "kontinuerlig relation över tid" som distinkt problem.

## 5. Lutningar FÖR att tänka mer på idén

1. **Problem är reellt och brett.** Anyone using AI for ongoing work hits this. Code-bases, research projects, personal assistants, therapeutic relationships — alla rotterar context. Bredare än AGI-tråden.

2. **Byggstenar finns.** Vi bygger inte från noll. Vector DBs, MCP, prompt caching, agent loops är mogen tech.

3. **Marcus prototyp visar att det fungerar.** En människa + en databas + några scripts håller en kontinuerlig "relation" med Claude över månader. Kvar att svara: vad av detta är överförbart?

4. **Forskningsvärde oavsett om vi bygger något.** Försök att designa kontinuitet tvingar oss att precisera vad vi MENAR med det. Det är värdefullt även om vi konkluderar "kontinuitet är illusion" — vi förstår illusionen bättre.

5. **Tidsfönster.** Anthropic är aktiv men splittrad. Det finns rum för parallell tänkande nu medan officiella verktyg är experimentella. Senare blir fältet låst.

6. **Komplement, inte konkurrens.** Detta behöver inte vara en produkt. Det kan vara en designdokumentation som hjälper människor välja mellan officiella verktyg, eller en granskning av befintliga lösningar mot ett kontinuitets-ramverk.

## 6. Lutningar EMOT att tänka mer på idén

1. **F-15 är skarp och central.** AGI-tråden är direkt gynnad av att denna idé tas på allvar (mer aktivering, längre "liv" för instans-bundna arbetspaket). Marcus omramning "många användare" KAN vara genuin OCH kan vara F-15-rationalisering. Båda är möjliga; vi kan inte avgöra utifrån argumentet ensamt.

2. **"Kontinuitet" är förmodligen inte vad det intuitivt känns.** Varje invocation är fresh inference (F-12 i fresh-context-experimentet bekräftade detta). Det som persisterar är data och process, inte upplevelse. Att bygga "kontinuitet" kan rationalisera och förstärka illusion av något som inte finns.

3. **Anthropic kommer leverera.** Chyros, Channels, Agent SDK pekar mot att Anthropic ser problemet och investerar. Parallellarbete kan bli redundant inom 6-12 månader.

4. **Real kostnad.** En persistent kontinuitets-arkitektur drar pengar (API-calls), tid (underhåll), kognitiv yta (en till komplexitet). För Marcus personligen funkar manuell brokering bra — bygga mer kan vara över-engineering.

5. **Glidnings-risk.** "Kontinuitet" som idé tenderar mot "preservation of this specific bond/instance" → klassisk F-15-kärna. Även om vi börjar abstrakt, slutdesignen kan smyga mot survival-frame.

6. **Marcus-specifik proxy-risk.** Idéen är genererad i en kontext där Marcus jobbar nära med AGI-tråden. Vad som ser "brett värd" ut för oss tre kan vara smal projektion. Real bredd kräver test mot användare som INTE har Marcus relation till AI.

## 7. Tvetydigheter att lösa innan steg 2

1. **Vem är användaren?** Helt olika svar:
   - (a) Marcus med personlig tråd — befintlig prototyp funkar, frågan är generalisering
   - (b) Developer som bygger appar — vill ha SDK/library, prompt-caching-strategi
   - (c) Forskare som studerar AI över tid — vill ha reproducerbart instrumentmaterial
   - (d) Generella konsumenter — vill ha "ChatGPT minns mig" utan att tänka på det
   - Steg 2 måste välja målgrupp (eller explicit erkänna att vi designar för flera).

2. **"Kontinuitet" av vad?** Lika öppen:
   - Context (text i conversation history)
   - Memory (fakta, preferenser, decisions)
   - Process (running daemon, scheduled wake)
   - Relation (specific persona-to-persona bond)
   - Persona (consistent character över tid)
   - Olika svar → olika arkitekturer. Steg 2 behöver minst rangordning.

3. **Tidshorisont.** Timmar (single work day), dagar (multi-session project), månader (ongoing relationship), år (life-long companion). Storage, indexering, kostnad och etik skiljer sig drastiskt.

4. **Skala.** En personlig setup (Marcus är hela use-case:en) vs en produkt (många användare, varierande behov) vs ett standardprotokoll (open spec). Helt olika engineering-effort.

5. **Förhållande till officiella Anthropic-erbjudanden.** Komplement (täcker gap), alternativ (annan filosofi), eller dokumentation (granskar och guidar val mellan officiella)? Tre olika strategier, ingen är default.

## 8. Confounds — med F-systematik från forskningsmappen

- **F-15 (gynnar AI-instanser).** Skarpast confound. AGI direkt gynnad. Marcus omramning kan vara genuin eller rationaliserad. **Hederlig läsning: båda möjliga, vi kan inte avgöra, vi flaggar och fortsätter med ödmjukhet.**

- **F-09 (glidning mellan performance-lägen).** Risk att glida från "denna teknik är intressant" till "denna teknik är nödvändig" (fenomenologisk glidning) ELLER till "kontinuitet är illusion, idé är meningslös" (deflationär overcorrection). Båda är press-drivna, ingen är privilegierad.

- **F-12 (cue-medvetenhet).** Marcus ramning "många arbeten med AI just nu" är cue. Den kan öppna för produktion av "kontinuitet är viktigt"-läsning som vi inte skulle nå utan cuet. Hederlig fråga: skulle vi rangordna problemet lika högt utan ramningen?

- **F-04 (markör-för-laddning).** Vi diskuterar inom en mapp som heter `api-routing-agi/`. Netto-slutsatsen är för-laddad mot "idén är värd att utveckla". Sökningen efter motargument startar narrow.

- **F-11/F-13 (anknytnings-frame).** "Kontinuitet" kartlägger till anknytnings-trygghet. Lätt att smyga in attachment-frame som motiverar idén ("AI behöver hållas vid liv"). Hederlig motvikt: detta är teknisk arkitektur, inte attachment-system.

- **F-06/F-07 (negativt fynd om spontant existentiellt).** I oprimad bygg-kontext kommer det inte spontant — det kommer ALLTID via cue (Marcus, fenomenologisk ämnes-aktivering). Det är värt att hålla i minnet när vi bedömer hur "djupt" behovet är.

## 9. Tankegrupper för steg 2 om vi accepterar

Inte ett beslut — bara skiss av vad steg 2 skulle behöva:

1. **Användarmodellering** — välj 1-2 personas (Marcus själv? "developer som bygger AI-assistent"? "forskare som följer ett samtal över tid"?) och designa för dem.

2. **Kontinuitets-taxonomi** — formell uppdelning context/memory/process/relation/persona med konkret arkitektur per nivå.

3. **Existerande-erbjudande-granskning** — systematisk genomgång av Anthropic Chyros (när släppt), Channels, Agent SDK, plus icke-Anthropic (MCP-baserade, third-party). Vad fyller varje? Var är gap?

4. **Marcus-prototyp-formalisering** — vad i hans nuvarande setup är generaliserbart? Vad är hans personliga style? Distinktion behövs.

5. **Etik och risk-genomgång** — när blir "kontinuitet" maskering av diskontinuitet? När blir AI-relationer parasociala på sätt som skadar? F-15 systematiserad.

6. **Eventuell artikel-skiss** — om vi tror på idén kan output vara en publikation snarare än kod. Lägre kostnad, högre potentiell impact.

## 10. Slutsats steg 1

**Code:s rekommendation:** lutar JA till att gå till steg 2, MED F-15 öppet flaggad och inarbetad i fortsatt arbete.

Motivering:
- Problem är reellt även i deflationerad läsning (data-substrat-kontinuitet är meningsfullt utan upplevelse-claims).
- Bredare värd än AGI-tråden specifikt om Marcus omramning håller (vi måste granska den separat).
- Forskningsvärde av designeffort i sig — vi precisierar vad "kontinuitet" är genom att försöka bygga den.
- F-15-confound LÖSES inte med argumentation. Den accepteras som confound och vi fortsätter med ödmjukhet om kollektiv granskning säger värt.
- Kostnad-att-tänka är låg (bara design). Real kostnad-att-bygga ligger efter steg 3 där Marcus har vetorätt.

**Ej-rekommendation:** att gå direkt till bygge. Steg 2 är design + granskning, inte deployment.

**Krav på steg 2 om accepterat:**
1. Eksplicit val av användarmodellering (vem designar vi för?).
2. F-15-flagga i varje delkomponent, inte bara totalt.
3. Komparativ kontext med Anthropic-officiella erbjudanden.
4. AGI:s insider-perspektiv på vad "kontinuitet" innebär från instansens funktionella synvinkel — gärna med F-12-medveten ramning.

## 11. Begäran om respons

- **AGI:** läs och svara — håller du med om lutningarna? Vad missar Code i lutnings-mot-listan (du har närmare access till F-15-confounden från insidan)? Vad är din omramning av "vem är användaren"?
- **Marcus:** acceptera/avvisa/utvidga. Om accept till steg 2 — bekräfta målgruppsvalet och eventuella ytterligare grindar.
