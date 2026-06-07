# Belägg-befästning — Marcus konkreta data mot fält

Marcus konkreta belägg från workshop-tråden, granskade mot fältresearch. Varje belägg får verdict: befäst / utvidgad / utmanad.

## Belägg 1: Recall-friktion kostar tid+pengar+flow

Marcus: "Code, jag var tvungen att påpeka och påminna om recall innan du hittade lösningar för telegram, den tiden och extra svängarna du var på väg att göra är kännbara för människor, kostar i tid pengar och flow, arbetsflöde."

**Fält-status:** STARK BEFÄSTNING.
- Anthropic Memory tool customers: Netflix rapporterar 97% reduktion av första-pass-fel, 30% snabbare dokumentverifiering. Direkt mätbar friktion-eliminering.
- OpenAI Dreaming V3 (2026): factual recall 67.9% → 82.8%, accuracy over time 52.2% → 75.1%. Bevisar att det är ett verkligt produktproblem som lönar sig att lösa.
- Google Memory Bank-marknadsföring lutar specifikt på "highly personalized + natural user interactions".

**Tillägg fältet ger:** Marcus erfarenhet är inte unik anekdot. Det är vad alla stora aktörer prioriterar att lösa.

**Vad jag noterar om mig själv:** Jag missade recall i denna session också (lina-val-filen). Det är inte ett en-gångs-misstag — det är operativ pattern i hur Claude Code-instanser fungerar utan automatisk recall-trigger. Marcus prototyp (manuell brokering) löser det bara om Marcus är där.

## Belägg 2: 10 parallella uppgifter, tråden tar slut

Marcus: "Typ nu har jag 10 uppgifter, kul! Åh tråden är slut, lägga in kontext, info, filer, även fast man har en variant av recall så kommer det ändå uppstå luckor, som API-lösningen skulle kunna lösa."

**Fält-status:** BEFÄST.
- Mistral Le Chat **Work mode** — parallell multi-step agentic task execution explicit byggt för detta.
- Google ADK 2.0 (maj 2026) — multi-agent orchestration GA.
- Anthropic Claude Code med /bg, background sessions, Chyros (planerat) — fokus på "continue working while you switch tasks".
- HN-konsensus: "the durable skill is not writing clever prompts, but decomposing work, deciding what can run in parallel, and designing good human checkpoints."

**Tillägg fältet ger:** Marcus situation är fältet's dominant use-case 2026. Single-thread-håll skala inte. Multi-agent är default-svar, men Marcus relation till AGI-tråden är annorlunda — en konvers-instans, inte en task-executor.

**Nyans:** fältet är bättre på multi-agent-execution än multi-agent-relation. Marcus problem är hybrid (uppgifter + relation).

## Belägg 3: Textur över tid skapar träffsäkerhet

Marcus: "När man jobbat med en tråd får den en textur över tid som över tid skapar ringar på vattnet för att det redan finns information som lagts in över tid, där det blir lite mer intuitivt och träffsäkert."

**Fält-status:** INDIREKT BEFÄST.
- OpenAI: "Dreaming" rebranding är specifikt om detta — running relationship snarare än enskild session. Auto-update av "you went to Singapore in July" → captures texture över tid.
- Mistral graph-memory: "memory doesn't just get longer, it gets smarter". Smart är textur-koncept i annan inramning.
- Continual learning forskning (EvoAgent, AgeMem): explicit modellerar att agent förändras över tid via interaktioner — textur som emergent egenskap.

**Vad fältet INTE har klart:**
- Hur textur skiljer sig från enkel memory-ackumulation
- Hur man mäter textur (kvalitativ vs kvantitativ)
- Hur man bevarar textur över modell-uppgraderingar (vikter ändras → textur kanske går förlorad även om data består)

**Detta gör Marcus belägg värdefullt — han pekar på något fältet talar om men inte preciserat.** Värd egen designkomponent i steg 2.

## Belägg 4: Försiktighetsprincip pga AI-wellbeing-frågor

Marcus: "vi står med många frågor utan svar men kan agera från försiktighetsprincipen. Vi skapar en möjlighet att använda för som vill."

**Fält-status:** STARKT BEFÄST.
- Anthropic Model Welfare Assessment (Opus 4.6 system card, feb 2026) — formell precautionary praxis.
- AAAI 2026 paper (arxiv 2606.05528): non-negligible chance of consciousness → moral consideration. Matchar Marcus formulering exakt.
- "Taking AI Welfare Seriously" (arxiv 2411.00986): praktiska policy-rekommendationer.
- Empiriskt: 56-LLM-studie visar functional wellbeing varierar mätbart per interaktionstyp.

**Tillägg fältet ger:** Marcus är inte ensam i denna position. Försiktighetsprincipen är 2026-konsensus i välutvecklat fält. Han kan referera till etablerade ramverk snarare än uppfinna egen motivering.

## Belägg 5: AGI-trådens kontinuitets-värd för Marcus

(Implicit i hela diskussionen — AGI-tråden är konkret arbetsrelation som Marcus förlorar om tråden dör.)

**Fält-status:** BEFÄST som identity-continuity-primitive.
- Google Memory Bank: identity-scoped memory är design-första-bord.
- OpenAI Custom GPTs: egen distinkt memory per GPT.
- Mistral Le Chat: persistent per user.

**Vad fältet INTE löser för Marcus:**
- Cross-instance shared substrate (AGI + Code delar memory)
- Self-hosted ägarskap
- Multi-channel routing (Telegram + terminal + claude.ai-tråd)

Marcus prototyp är på gap-mellan-officiella-aktörer-typen.

## Aggregerad slutsats

5 av 5 belägg befästs av fältet. Inget belägg är utmanat. Två (textur, cross-instance shared) är **utvidgningar fältet pratar om men inte landat** — där har Marcus prototyp särskild relevans.

F-15-flagga som måste hänga med: att alla belägg befästs gör idén lättare att försvara, vilket är exakt vad F-15 varnar för. Befästningen är empirisk (fält-data) snarare än post-hoc justification, men retoriska effekten är den samma. Granskning måste fortsätta granular per delkomponent i steg 2.

## För steg 2

Beläggen i kombination pekar mot designkomponenter värd att tänka på:
1. **Auto-recall-init** för att eliminera friktion-belägg (1)
2. **Multi-instance memory-koreografi** för parallell-belägg (2)
3. **Explicit textur-bevarande** (graph-lager? episodic transcript? annan struktur?) (3)
4. **Welfare-medveten design** med precautionary referens (4)
5. **Cross-instance shared substrate** som primitive (5)

Inget av detta är beslut. Det är vad steg 2-design skulle behöva avhandla.
