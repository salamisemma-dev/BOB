# PvA — Spec-Driven Development in project-build: voor- en nadelen + fix per nadeel

Plan van aanpak voor het invoeren van Spec-Driven Development (SDD) als kern van de
`project-build` skill. Elke nadeel heeft een concrete fix die al in de skill is
verwerkt, zodat het nadeel in de praktijk wegvalt.

## Doel
Intent (bedrijfsregels, architectuurkeuzes, validatielogica) vastleggen als
**uitvoerbare, versiebeheerde specificaties** = permanent systeemgeheugen. Zo blijft
een project ook na 6 maanden te begrijpen en te onderhouden — door mens én AI.

## Aanpak in het kort
1. Constitution opstellen (standaarden, conventies, governance, invarianten).
2. Specs schrijven per onderdeel (schema, transformatie, validatie, orchestratie,
   semantisch, AI-workflow) — uitvoerbaar + met "waarom".
3. Approval gate: geen code zonder goedgekeurde spec; spec eerst wijzigen, dan code.
4. Twee-tier uitvoering: dure model denkt (spec/plan/review), goedkope sub-agents
   bouwen.
5. CI/CD valideert specs en faalt de build bij drift.
6. Geheugen + DOX updaten na elke sessie.

---

## Voordelen

| # | Voordeel | Effect |
|---|----------|--------|
| V1 | Permanent systeemgeheugen | "Waarom werkt dit?" staat in de spec, niet in een verdwenen chat. |
| V2 | Geen vibe-coding drift | Code moet aan een goedgekeurde spec voldoen; CI vangt afwijking. |
| V3 | Lagere tokenkosten | Recall + specs voorkomen heronderzoek; goedkope sub-agents doen bulk. |
| V4 | Onderhoudbaar door mens én AI | AI-agents lezen de spec i.p.v. code te reverse-engineeren. |
| V5 | Veilige wijzigingen | Downstream-impact staat in elke spec; je weet wat breekt. |
| V6 | Onboarding sneller | Constitution + specs = leesbare kaart van het systeem. |
| V7 | Bestaande chaos te redden | Retrofit-track haalt specs uit bestaande code en saneert structuur. |

---

## Nadelen + fix (elke fix zit in de skill)

| # | Nadeel | Fix (ingebouwd) |
|---|--------|-----------------|
| N1 | **Overhead vooraf** — specs schrijven kost tijd vóór er code is. | Mode + "light"-regel: kleine taken krijgen een mini-spec (paar regels); volledige spec-set alleen voor echte onderdelen. Overhead schaalt mee met omvang. |
| N2 | **Specs verouderen** — doc rot, spec ≠ code. | Approval gate "spec eerst, dan code" (Fase 1.5/4) + CI spec-validatie die de build rood maakt bij drift. Verouderen kan niet stilletjes. |
| N3 | **Ceremonie/bureaucratie** — voelt zwaar voor solo/snel werk. | Alleen de 6 spec-typen die de taak raakt; geen verplichte volledige set. Anti-excuus-tabel zegt: run het *light*, niet *skip*. |
| N4 | **Leercurve** — gebruiker kent SDD/spec-typen niet. | `references/spec-driven.md` geeft skeletons + templates + tabel; de skill genereert de eerste constitution/spec zodat de gebruiker een voorbeeld heeft. |
| N5 | **"Uitvoerbaar" is werk** — een spec die niets aanstuurt is enkel doc. | Elke spec heeft een `Verification`-sectie + tabel "spec → wat het aanstuurt"; regel: kan een spec niets automatiseren, scherp aan of laat hem vallen. |
| N6 | **Risico bij bestaande projecten** — herstructureren breekt dingen. | Retrofit-track: characterization-tests eerst, document-then-move, kleine reversibele commits, review-gate, rollback per stap. |
| N7 | **Te rigide** — kan innovatie/snel experimenteren remmen. | Specs zijn versiebeheerd en iteratief: spike mag, maar wordt daarna in een spec vastgelegd; constitution bevat alleen trage invarianten, details zakken naar specs. |
| N8 | **Dubbele bron van waarheid** — spec + code + DOX + memory. | Heldere rolverdeling: spec = contract/intent, code = implementatie, AGENTS.md = lokale regels, memory = sessiebeslissingen. Fase 4 dwingt af dat spec leidt; geen duplicatie van dezelfde regel. |
| N9 | **Approval gate vertraagt** — wachten op goedkeuring blokkeert. | Gate is licht: korte spec → snelle OK; bij solo-gebruiker is "approve" één bevestiging. Beter 30s wachten dan dagen reverse-engineeren later. |
| N10 | **CI-setup ontbreekt** — geen pipeline om te valideren. | `references/spec-driven.md` levert een starter-pipeline; ontbreekt CI, dan draait spec-validatie lokaal in Fase 3 als check. |

---

## Conclusie
Alle tien nadelen zijn afgevangen door mechanismen die al in de skill zitten: schaalbare
overhead (light-mode), CI-afgedwongen actualiteit, templates tegen de leercurve, en een
veilige retrofit-track voor bestaande projecten. Netto: de winst (permanent geheugen,
geen drift, lagere kosten, onderhoudbaarheid) blijft, de kosten worden beheersbaar
gemaakt i.p.v. genegeerd.
