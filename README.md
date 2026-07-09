# doc-skills

Portable [Agent Skills](https://skills.sh) for document work. Each skill is
**self-contained**: clone the repo, run the skill's `setup` script, and it
works — no other skills, plugins, or framework required.

## Skills

| Skill | What it does |
|-------|--------------|
| [`hwpx-table-kit`](skills/hwpx-table-kit) | Insert real, editable OWPML tables into an existing Hangul `.hwpx` without corrupting it. The reusable engine. |
| [`hwpx-image-table-to-table`](skills/hwpx-image-table-to-table) | Recipe: convert a table embedded as an **image** inside a `.hwpx` into a native editable table (optionally pulling data from `.xlsx`). Uses `hwpx-table-kit`. |

## Quick start (any agent, no base setup)

```bash
git clone https://github.com/<owner>/doc-skills.git
cd doc-skills/skills/hwpx-table-kit
bash setup.sh          # or: pwsh setup.ps1  (Windows)

# generate
python scripts/inject_tables.py --base IN.hwpx --tables tables.json --out OUT.hwpx
# verify (optional, needs Node)
node scripts/verify_hwpx.mjs OUT.hwpx
```

See each skill's `SKILL.md` for full instructions.

## Using with Claude Code / Claude agents

Point your agent at the skill folder, or install into your skills directory:

```bash
# user-level (all projects)
cp -r skills/* ~/.claude/skills/
# or project-level
cp -r skills/* .claude/skills/
```

The skills are also discoverable via the Skills CLI once published:
`npx skills add <owner>/doc-skills@hwpx-table-kit`.

## Requirements

- **Python 3.9+** — table generation (Pillow + openpyxl, installed by `setup`).
- **Node 18+** — optional, only for roundtrip verification via
  [`kordoc`](https://www.npmjs.com/package/kordoc).

## Scope & limits

These skills generate/repackage HWPX XML directly. They do **not** require or
automate the Hangul (한글) application. Because of that, always have a human open
the produced `.hwpx` to confirm the visual result. Merged cells
(colspan/rowspan) are out of scope for generation.

## License

MIT
