# Waldo's Rescue Pen: Fosters Needed

Public foster page (GitHub Pages, served from `docs/`) plus the Claude Code skill
that keeps it updated and texts potential fosters through Petstablished.

- **Edit the dogs:** change `dogs.json`, run `python3 build.py`, commit and push.
- **With Claude:** "put Fargo and Iggy on the foster page, Iggy needs a foster by Friday",
  then "text the potential fosters the link". Claude previews everything and waits for your OK.
- Skill: `skill/SKILL.md` (linked into `~/.claude/skills/waldos-fosters`).

Only dog info goes on the page. No foster or adopter names, addresses or phone numbers.
Text logs are kept outside the repo in `~/.claude/petstablished-text-logs/`.
