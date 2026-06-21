# Project Constitution — <PROJECT NAME>

Version: 0.1 · Last updated: <YYYY-MM-DD> · Owner: <name>

The supreme, slow-changing contract. Everything (specs, code, CI) conforms to this.
Keep it short and durable. If a rule changes weekly, push it down into a spec instead.

## 1. Technology standards
- Languages / runtimes:
- Frameworks:
- Allowed dependencies / forbidden dependencies:

## 2. Naming conventions
- Files / modules:
- Data (tables, columns, fields):
- Jobs / env vars:

## 3. Architecture rules & boundaries
- Layers and allowed dependency direction:
- What may talk to what:
- Data-flow rules:

## 4. Governance
- Spec approval: who/what approves a spec before code is written.
- Versioning scheme: semver for specs (major = breaking contract change).
- Breaking-change policy:
- Deprecation policy:

## 5. Invariants (must hold platform-wide)
- e.g. all timestamps UTC ISO-8601
- e.g. no PII in logs
- e.g. every table has a surrogate key

## 6. Amendment log
- <YYYY-MM-DD> — created. Why: <reason>.
