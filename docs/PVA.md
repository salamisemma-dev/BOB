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
| N2 | **Geen CI/CD** | Werkende validator + GitHub Actions die de build rood maakt bij drift; herbruikbaar CI-template voor eigen repos. | `scripts/bob_validate.py`, `.github/workflows/bob-validate.yml`, `…-template.yml` |
| N3 | **Sub-agents onderspecificeerd** | Rollen, input/output-contract, failure modes, en hoe te vervangen gedocumenteerd. | `docs/SUB-AGENTS.md` |
| N4 | **Geen migratiepad bestaande projecten** | `bob analyze` scant code en genereert draft-constitution + spec-stubs; retrofit-track met characterization-tests. | `scripts/bob_analyze.py`, `skills/bob/references/retrofit-existing.md` |
| N5 | **Geen metrics/succescriteria** | Eerlijke beperking: nog geen telemetrie. Fix nu = meetbaarheid ingebouwd: validator geeft `--json`; demo bewijst pass/fail objectief. Telemetrie/benchmarks staan op de roadmap (N5 open, expliciet erkend i.p.v. verzwegen). | `bob_validate.py --json`, roadmap hieronder |
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
- **N5 telemetrie/benchmarks**: tokens-met/zonder-BOB nog niet gemeten. Volgende stap:
  opt-in meting + gepubliceerde benchmark.
- JSON Schema in schema-specs wordt nog niet *uitgevoerd* tegen runtime-data in CI —
  nu structureel gevalideerd; volgende stap: optionele `jsonschema`-check achter een flag.
- Validator dekt het YAML-subset van de templates, niet volledige YAML — bewust, om
  dependency-vrij te blijven. Bij behoefte: optionele PyYAML-modus.

## Conclusie
De review's kernverwijt — "vision met skeleton, mist de operationele 80%" — is
geadresseerd: formaat, handhaving (CI), voorbeeld, sub-agent-docs, retrofit-tooling,
governance en security zijn er en getest. Resterend gat (metrics) is expliciet benoemd
i.p.v. weggepoetst.
