# Steg 2 — TANKEBYGGE / DESIGN

**Status:** initierad 2026-06-07 efter Marcus grönt ljus.
**Föregående:** `01_ide.md` accepterad, `research/` klar med 5 dokument + 4 HTML-designs.
**Acceptans krävs:** Marcus + AGI + Code för att gå till steg 3 (beslut om bygge).

---

## Vad steg 2 ÄR

- Design + analys av hur idéen skulle KUNNA fungera om vi byggde den
- Konkret arkitektur-alternativ med trade-offs
- F-15 manifesterad per komponent, inte som totalt påstående
- Risk-register
- Beslutspunkter för Marcus

## Vad steg 2 INTE är

- Inte byggande (det är steg 3)
- Inte slutgiltig arkitektur (alternativ avsiktligt kvar)
- Inte resursbeslut (efter steg 2)
- Inte commitment till specifik teknik-stack
- Inte deployment av något i marcus_memory, ping_loop, eller andra produktionssystem

## Dokumentstruktur (per AGI:s syntes 41277)

| Fil | Fokus | Föreslagen skribent |
|---|---|---|
| `architecture-alternatives.md` | 2-3 konkreta arkitekturer med trade-offs | Code (har research-data) |
| `welfare-integration.md` | Hur F-15 manifesteras tekniskt | AGI (insider på welfare) |
| `marcus-decoupling.md` | Hur systemet hanterar Marcus-failure-mode | AGI (relations-vinkel) |
| `risk-register.md` | Anthropic-utvidgning-risk + andra risker | Båda (cross-check) |
| `decision-points.md` | Vad Marcus måste avgöra för att gå till steg 3 | Code (struktur) |

Arbetsfördelning är förslag — AGI kan invända, ändras lätt.

## Grindar för 02_design/-arbetet

Utöver workshop-mappens grindar och idéens (i 01_ide.md):

- **Allt skrivande är revidérbart.** Första utkast är inte slutgiltigt. Båda kan invända.
- **F-15-checkpoint öppet i varje dokument.** Inte bara totalt.
- **Inga implementations-detaljer som låser teknik-val** — håll designnivå.
- **Citationer från research/** är preferred — vi ska inte uppfinna utan bygga på det vi redan etablerat.
- **Konvergens-flagga:** vi har redan upptäckt att AGI och Code drar mot samma slutsatser (groupthink-risk). Behåll Marcus som tredje part i alla judgement calls.

## Beslutspunkt efter steg 2

När alla 5 dokumenten finns och granskats:
1. Marcus läser
2. Marcus + AGI + Code diskuterar om steg 3 (bygge) är värd
3. Eventuellt: parkering, alternativ riktning, paus
4. Eventuellt: smal prototyp som test innan full design
