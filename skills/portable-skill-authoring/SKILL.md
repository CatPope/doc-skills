---
name: portable-skill-authoring
description: >-
  Author portable, self-bootstrapping Agent Skills (스킬 만들기 / 스킬 작성) for
  document work that a "no-base" agent — one with no other skills or plugins
  installed — can use from a git clone alone. Use when creating or reviewing a
  SKILL.md, packaging scripts into a skill, deciding whether to split one skill
  into several, or checking that a skill will run on a fresh machine. Ships a
  stdlib-only portability linter and starter templates.
---

# portable-skill-authoring

The rules and tooling for writing skills in this repo so that **a plain agent
with nothing installed** can clone the repo and use them. It is the "skill for
making skills." It bundles a **standard-library-only** linter
(`scripts/check_skill.py`) and copy-paste **templates**.

## When to use

- You are creating a new skill (a new `skills/<name>/SKILL.md`).
- You are splitting a job into an engine skill + a recipe skill.
- You want to verify an existing skill is still portable before committing.

## The three rules (why this skill exists)

1. **No-base compatible.** Assume the agent has *no other skills and no
   plugins*. Everything the skill needs is inside its own folder and reachable
   from its `SKILL.md`. Never say "use the X skill" unless X is a sibling in
   the same repo and you say so explicitly.
2. **Self-bootstrapping from a clone.** After `git clone`, running the skill's
   `setup.sh` (or `setup.ps1`) is the *only* manual step. It installs every
   dependency. No hidden global state, no hardcoded machine paths, no
   pre-existing virtualenv. Prefer the standard library; when a dep is truly
   needed, pin it in `requirements.txt` / `package.json` so setup installs it.
3. **Split when it clarifies reuse.** A reusable engine (does the mechanical
   work) and a recipe (the human-facing procedure that drives the engine) are
   two skills, side by side in the repo. See `hwpx-table-kit` (engine) +
   `hwpx-image-table-to-table` (recipe).

## How to author a skill (procedure)

1. **Copy the template.** Start from `templates/SKILL.template.md`,
   `templates/setup.sh`, `templates/setup.ps1`, `templates/requirements.txt`.
   Put them under `skills/<your-name>/`.
2. **Write the frontmatter.** `name:` must equal the directory name.
   `description:` is what the agent keyword-matches on — spell out the triggers
   in both English and the target language, and end with the no-base note.
3. **Bundle scripts, declare deps.** Any third-party import goes in
   `requirements.txt`. Keep scripts self-contained and path-relative
   (`os.path.dirname(__file__)`, `cd "$(dirname "$0")"`, `$PSScriptRoot`).
4. **Ensure LF endings** for `*.sh`. Add the `templates/gitattributes.snippet`
   lines to the repo-root `.gitattributes` (CRLF breaks `bash setup.sh`).
5. **Update the docs.** Adding or changing a skill is not finished until the
   repo docs reflect it: add a row to the README skill list (and update its
   quick-start / requirements if the new skill changes them), and refresh any
   index the repo keeps. Keep the skill's own `SKILL.md` in sync too.
6. **Validate — this is a required gate, not optional (see below).**
7. **Only after it passes:** commit and push.

## Validate before you finish (required)

A skill is **not done until the linter passes.** Run it against your skill (or
the whole `skills/` folder) from this skill's directory:

```bash
python scripts/check_skill.py ../            # lint every skill in the repo
python scripts/check_skill.py ../my-skill    # lint just one
```

It checks, using only the Python standard library (so a no-base agent can run
it too):

| Code | Rule |
|------|------|
| C1 | `SKILL.md` exists |
| C2 | has YAML frontmatter |
| C3 | `name:` equals the directory name |
| C4 | `description:` present and long enough to match on |
| C5 | shell scripts use **LF** (no CRLF) |
| C6 | ships `setup.sh` **and** `setup.ps1` (or clearly delegates to a sibling's) |
| C7 | setup scripts self-locate (`dirname "$0"` / `$PSScriptRoot`) |
| C8 | no hardcoded machine-local paths (user home, temp) |
| C9 | third-party imports are declared in `requirements.txt` |

Exit code is non-zero if any **FAIL** is present. **Fix every FAIL before
committing.** WARNs are advisory — resolve them or note why not.

Passing the linter proves the *structure* is portable; it cannot open the
document or run the domain logic. So the final human check still applies: for
any document-producing skill, **ask the user to open the output once and
confirm** it looks right.

## Files

| File | Purpose |
|------|---------|
| `scripts/check_skill.py` | stdlib-only portability linter (the validation gate) |
| `templates/SKILL.template.md` | starting point for a new `SKILL.md` |
| `templates/setup.sh` / `setup.ps1` | cross-platform self-bootstrap scripts |
| `templates/requirements.txt` | where to pin Python deps |
| `templates/gitattributes.snippet` | LF/CRLF rules to paste into repo `.gitattributes` |

## Commit / push discipline

Author and verify in one pass; **publish only after the gate is green.** Do not
push a half-written skill or a skill that fails the linter. A change is
"complete" only when (a) the docs are updated (step 5) and (b) the linter
reports all skills passing. Then commit the skill **together with the doc
update** in the same push — never leave the README describing a different set
of skills than the repo ships.

## Notes / limits

- The linter is a *portability* check, not a correctness or security review; it
  does not run the skill's own logic.
- C8/C9 use conservative heuristics (known third-party module names, common
  home/temp path fragments). Extend the tables in `check_skill.py` as the repo
  grows.
