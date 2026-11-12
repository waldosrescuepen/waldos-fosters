# petstablished-text

A Claude Code skill for sending custom text messages to Petstablished contacts
(adopters, fosters, applicants) through Petstablished's own **Send Text** feature.

## How it works
Ask Claude something like *"text Amanda Aaron that Biscuit is ready for pickup Saturday"*.
Claude:
1. opens Petstablished in your signed-in Chrome (Claude in Chrome extension),
2. looks up the contacts and their phone numbers,
3. shows you the recipients and the exact text and **waits for your OK**,
4. sends each text with Manage → Send Message → Send Text,
5. logs what was sent to `~/.claude/petstablished-text-logs/` (outside this repo).

Claude never stores or types your Petstablished password. Stay signed in to Petstablished in Chrome.

## Install on a Mac
```bash
git clone <this repo> ~/petstablished-text-skill
ln -s ~/petstablished-text-skill ~/.claude/skills/petstablished-text
```
