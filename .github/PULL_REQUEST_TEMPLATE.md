## Summary

<!-- One imperative-mood sentence: what this change does. -->

## Why

<!-- What prompted this -- the problem, the request, or what stays wrong without it. -->

## Testing

<!-- How you checked this works (a skill/command run through manually, example output, etc).
     CI only validates marketplace structure, CODEOWNERS, and shellcheck -- it doesn't exercise
     skill or command behavior, so this is the only record of whether it actually works. -->

## Notes

<!-- Optional: alternatives considered, follow-ups, anything worth knowing on a later re-read. -->

---

- If this touches a plugin, bump its version in `plugins/<name>/.claude-plugin/plugin.json` and
  add a `CHANGELOG.md` entry -- `scripts/validate.py --base` fails the PR otherwise.
- `Closes #123` auto-closes the issue, but only when this PR merges into `main`.
