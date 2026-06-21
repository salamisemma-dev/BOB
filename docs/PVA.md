# PvA — BOB plan van aanpak: voor- en nadelen + fix per nadeel

Plan van aanpak in antwoord op de "Brutal Edition" review. Elk nadeel uit de review
heeft nu een concrete fix die **in deze repo geleverd en getest** is. Status per fix
verwijst naar echte bestanden.

## Doel
SDD niet als manifest maar als werkend product: concreet specformaat, geautomatiseerde
handhaving, echte voorbeelden, meetbare discipline.

---

## Voordelen (wat BOB goed doet)
| # | Voordeel |
|---|----------|
| V1 | Anti-vibe-coding by design — intent wordt uitvoerbaar + versiebeheerd. |
| V2 | Tokenkosten omlaag — recall + goedkope sub-agents; duur model enkel plan/review. |
| V3 | Permanent systeemgeheugen — context stapelt over sessies. |
| V4 | Spec-driven i.p.v. prompt-driven — spec is bron van waarheid, code is gevolg. |
| V5 | Retrofit — bestaande chaos te redden via `bob analyze` + retrofit-track. |
| V6 | Graceful degradation — werkt met of zonder companions/sub-agents. |
| V7 | Heldere scheiding plan (duur) vs uitvoering (goedkoop). |

---

## Nadelen uit de review + geleverde fix

| # | Nadeel (review) | Fix | Geleverd in |
|---|-----------------|-----|-------------|
| N1 | **Geen concreet specformaat** | Canoniek formaat gedefinieerd: Markdown + YAML-frontmatter subset; Contract-sectie bevat het formele artefact (JSON Schema/DDL/Gherkin) per type. Templates copy-paste klaar. | `docs/SPEC-FORMAT.md`, `templates/` |
| N2 | **Geen CI/CD** | Werkende validator + GitHub Actions die de build rood maakt bij drift; herbruikbaar CI-template voor eigen repos. | `scripts/bob_validate.py`, `.github/workflows/bob-validate.yml`, `templates/github-actions/bob-validate.yml` |
| N3 | **Sub-agents onderspecificeerd** | Rollen, input/output-contract, failure modes, en hoe te vervangen gedocumenteerd. | `docs/SUB-AGENTS.md` |
| N4 | **Geen migratiepad bestaande projecten** | `bob analyze` scant code en genereert draft-constitution + spec-stubs; retrofit-track met characterization-tests. | `scripts/bob_analyze.py`, `skills/bob/references/retrofit-existing.md` |
| N5 | **Geen metrics/succescriteria** | Deels gesloten: benchmark-harness levert herhaalbare kwaliteits- + footprint-metingen (validator + tests + tokentelling, `--json`, CI-gate). Nog open: with/zonder-BOB ROI-vergelijking (aparte harness, roadmap). | `scripts/bob_benchmark.py`, `docs/BENCHMARK.md`, CI |
| N6 | **Companion-afhankelijkheid onduidelijk** | Exacte integratiepunten + "minimal viable BOB" (nul companions) beschreven; degradatie gedocumenteerd. | `skills/bob/SKILL.md` (Dependencies), `docs/SUB-AGENTS.md`, README |
| N7 | **Geen teststrategie** | Default stack benoemd (stdlib `unittest`), demo met 9 spec-getraceerde tests, validator met 12 tests; CI draait beide. | `examples/todo-api/tests/`, `tests/test_bob_validate.py`, CI |
| N8 | **Geen governance voor spec-evolutie** | Wijzigingsproces (propose→review→version→implement→validate), semver, statuslevenscyclus, conflictregel. | `docs/GOVERNANCE.md` |

### Wat de review als "geheel ontbrekend" noemde
| Item | Fix | Geleverd in |
|------|-----|-------------|
| Real-world voorbeeld | Compleet, validerend demo-project gebouwd vanaf nul. | `examples/todo-api/` |
| Troubleshooting | Symptoom→oorzaak→fix tabel. | `docs/TROUBLESHOOTING.md` |
| Onboarding/leercurve | 30-minuten tutorial. | `docs/TUTORIAL.md` |
| Community/support | CONTRIBUTING + issues-verwijzing. | `CONTRIBUTING.md` |
| Security | Threat model + practices. | `SECURITY.md` |

---

## Bewijs (getest, niet beloofd)
- `python -m unittest tests.test_bob_validate` → 12/12 pass.
- `python -m unittest discover -s examples/todo-api/tests` → 9/9 pass.
- `python scripts/bob_validate.py examples/todo-api` → `OK: spec layer valid`.
- `python scripts/bob_analyze.py examples/todo-api` → detecteert modules, dry-run plan.

## Eerlijke open punten (roadmap)
- **N5 ROI-vergelijking**: footprint + kwaliteit worden nu gemeten (`bob_benchmark.py`),
  maar tokens-met/zonder-BOB nog niet. Volgende stap: vergelijkingsharness via de Claude
  API (met consent + anonimisering) + gepubliceerde case study. Zie `docs/BENCHMARK.md`.
- JSON Schema in schema-specs wordt nog niet *uitgevoerd* tegen runtime-data in CI —
  nu structureel gevalideerd; volgende stap: optionele `jsonschema`-check achter een flag.
- Validator dekt het YAML-subset van de templates, niet volledige YAML — bewust, om
  dependency-vrij te blijven. Bij behoefte: optionele PyYAML-modus.

## Conclusie
De review's kernverwijt — "vision met skeleton, mist de operationele 80%" — is
geadresseerd: formaat, handhaving (CI), voorbeeld, sub-agent-docs, retrofit-tooling,
governance en security zijn er en getest. Resterend gat (metrics) is expliciet benoemd
i.p.v. weggepoetst.

---

## Ronde 3 — anti-vibe handhaving (gedrag afdwingen, niet alleen documenteren)

Kritiek: specs konden "mooi bestaan" zonder hard aan tests/runtime gekoppeld te zijn.
Elk PvA-punt uit die review met de geleverde fix:

| Punt | Nadeel/risico | Fix | Geleverd in |
|------|---------------|-----|-------------|
| Validator | checkt structuur, niet of code semantisch klopt | **Spec-to-test traceability gate**: elke approved (niet-ai-workflow) spec moet in Verification een bestaande test noemen; CI faalt anders | `bob_validate.py` (traceability), 7 nieuwe tests |
| CI gate | kon groen zijn terwijl implementatie functioneel afwijkt | traceability + **golden/runtime checks**: schema-specs gevalideerd tegen sample data | `bob_runtime_check.py`, `examples/todo-api/golden/` |
| `bob_analyze.py` | draft specs lijken waarheid | stubs zijn `status: draft` + TODO-markers; approval verplicht; draft wordt niet door traceability/ready-gate geaccepteerd | bestaand gedrag + gate |
| Subagents | drift bij te brede taak | regel: agent werkt alleen vanuit **spec-id + acceptatiecriteria**, één slice per agent | SKILL.md Phase 3 |
| Constitution | bureaucratie | mini-constitution volstaat; uitbreiden alleen bij complexiteit | `templates/`, ADOPTION |
| Memory/DOX | ruis | policy: alleen besluiten/risico's/specpaden/verificatie | `docs/ADOPTION.md` |
| Token benchmark | approx ≠ echte kosten | gelabeld als footprint, niet ROI | `docs/BENCHMARK.md` |
| "100% goed" | bestaat niet | falen vroeg zichtbaar: gates + fail-fast + ready-check | `bob_ready.py`, CI |
| Adoption | wanneer is project BOB-ready? | 6-punts **adoption gate** + fail-fast anti-vibe modus | `bob_ready.py`, `docs/ADOPTION.md`, SKILL.md |

### Open (bewust, volgorde per advies)
- **Pilot op echte rommelige repo** — kan niet op de schone demo; vereist dat je BOB op
  een bestaande repo richt. Tooling staat klaar (`bob_analyze` → fill/approve →
  validator+runtime in CI → `bob_ready` groen).
- **ROI-vergelijking met/zonder BOB** — pas ná de pilot (advies gevolgd).
