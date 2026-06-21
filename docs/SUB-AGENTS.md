# BOB sub-agents — roles, contracts, failure modes

BOB's two-tier model: the expensive session model thinks (specs, plan, review); cheap
sub-agents do the repetitive doing. This doc makes that not-a-black-box.

## How they're invoked
Phase 3 dispatches each planned task with the `Agent` tool. The **input contract** to
every sub-agent is the same: the exact task slice from the plan + the spec id(s) it
implements + the test strategy. The **output contract**: code + passing tests for that
slice, nothing outside scope. Independent tasks are spawned in parallel in one message.
Pass `model: "haiku"` (or `sonnet`) for routine implementation to save tokens.

## Roles
| Role | Job | Input | Output |
|------|-----|-------|--------|
| `coder` / `general-purpose` | Implement one spec'd task TDD | task slice + spec id | code + tests, green |
| `tester` | Fill coverage gaps | module + spec Verification | added tests |
| `superpowers:code-reviewer` / `reviewer` | Quality gate (expensive model) | diff + spec + constitution | findings / approve |
| `Plan` | Re-plan a slice that grew | the oversized task | smaller sub-tasks |

Availability varies per environment. If a specialized agent is absent, fall back to
`general-purpose`; if no sub-agents at all (e.g. minimal Cowork), run the phase inline.
BOB degrades, it doesn't break.

## Failure modes & handling
- **Sub-agent returns failing tests** → don't accept; loop back with the failure output.
- **Output drifts from the spec** → reject at the review gate; fix the code or, if the
  spec was wrong, fix the spec first then regenerate.
- **Task too big / agent stalls** → split via `Plan`, re-dispatch smaller slices.
- **Non-deterministic flake** → re-run once; if still flaky, treat as a real defect and
  pin behavior with a characterization test.

## Customize / replace
Swap the role names in the SKILL's Phase 3 list for your environment's agents. The only
hard requirement is the input/output contract above — anything honoring it plugs in.
