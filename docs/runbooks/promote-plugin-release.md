# Promote a plugin release

Take a plugin change from pull request to pilot testers to every permitted user, in Claude and Microsoft 365 Copilot. Includes rollback.

This is a runbook: a fixed sequence. If something goes wrong that this page doesn't cover, stop and escalate (see [Rollback](#rollback) and [Escalation](#escalation)).

## When to use this

- A pull request changes anything under `plugins/` (new plugin, new skill, wording fix), **or**
- `enterprise/plugin-access.yaml` changes a plugin's `stage` from `pilot` to `released`.

Not for: changing who sees an already released plugin. That is a policy-only change: merge the pull request to `plugin-access.yaml`, then do [step C3](#c-merge-and-release-to-claude) and [step D4](#d-release-to-microsoft-365-copilot) only.

Linked from: the pull request template checklist, the [README](../../README.md#versioning) and the [Enterprise runbook](../enterprise/README.md).

## Which path

Answer once, then follow only that path's steps.

| The pull request... | Path |
| --- | --- |
| adds a plugin that does not exist in `main` yet | **New plugin**: A → B → C → D, then promote later with E |
| changes a plugin that already exists in `main` | **Update**: A → B → C → D |
| only changes a plugin's `stage` from `pilot` to `released` | **Promotion**: E |

## Roles

| Role | Does |
| --- | --- |
| Author | Opens the pull request. Anyone in the AI team. |
| Champion | Pilot-tests and approves changes to their department's plugin. Named in CODEOWNERS. |
| Claude admin | Owner, or custom role with Libraries: Can manage and Identity & Access: Can view. Applies console settings. |
| Microsoft 365 admin | Uploads and assigns Copilot packages in the Microsoft 365 admin center. |

One person can hold several roles, except that the author cannot be the champion who signs off.

## Prerequisites

Check once per person before their first release.

- [ ] Author: Python 3.12 with `pip install pyyaml`, and Claude Code (`claude --version`).
- [ ] Champion: member of the `claude-pilot` Entra group, and allowed to add plugins for themselves in Customize > Plugins (Claude admin enables this in Organization settings > Plugins & skills > **Policy**).
- [ ] Claude admin: the marketplace's default access in Organization settings > Plugins & skills is **Not available**, so a newly synced plugin reaches nobody until step C4.
- [ ] Repository: branch protection on `main` requires CI to pass and requires review from code owners.
- [ ] Microsoft 365 admin: Node.js, `npm install -g @microsoft/m365agentstoolkit-cli`, and the company privacy, terms and website URLs.

## A. Prepare the pull request

1. Bump the plugin's `version` in `plugins/<name>/.claude-plugin/plugin.json`.
   - Wording fix: PATCH (`0.2.0` → `0.2.1`).
   - Skill added: MINOR (`0.2.1` → `0.3.0`).
   - Skill renamed or removed: MAJOR (`0.3.0` → `1.0.0`).
2. Add a line under `## Unreleased` in `CHANGELOG.md`: `` `<name>` <version>: <what changed>. ``
3. **New plugin only.** Add its rule to `enterprise/plugin-access.yaml`:
   ```yaml
     <name>:
       stage: pilot
       default: not-available
       groups:
         claude-pilot: installed-by-default
   ```
   Then add `/plugins/<name>/` to `.github/CODEOWNERS` with the department's champions team.
4. Regenerate the access matrix and run the checks:
   ```bash
   python scripts/access.py matrix --write
   python scripts/validate.py --base origin/main
   claude plugin validate .
   ```
   Expected: `0 errors` from `validate.py` and `√ Validation passed` from `claude plugin validate`.
5. Open the pull request against `main`. Expected: CI passes and the **preview-packages** job uploads an artifact named `plugin-preview-pr-<number>`.

## B. Pilot test

Done by the champion, from the pull request build. Nothing reaches other users yet.

1. On the pull request, open **Checks** > **CI** > **Summary** > Artifacts, and download `plugin-preview-pr-<number>`. Unzip it once; it contains `<name>-<version>.zip`.
2. In claude.ai, open **Customize > Plugins**. **Update only:** turn off the organisation copy of `<name>` so the two versions don't load together.
3. Upload `<name>-<version>.zip` for yourself.
4. For each changed skill, start a new chat and send a request matching the skill's `description`. Check:
   - the skill loads (Claude names it or follows its process)
   - the output has every part the skill's **Output** section lists
   - no personal data or customer names appear that you didn't supply
5. Remove your uploaded copy. **Update only:** turn the organisation copy back on.
6. Approve the pull request with a review comment:
   `Pilot-tested <name> <version> in claude.ai: <skills tested>. OK to release.`
   If a check failed, request changes with the failing request and output instead, and stop here.

## C. Merge and release to Claude

1. Merge the pull request. Expected: `main` CI passes.
2. Sync starts automatically. If the plugin hasn't updated after 30 minutes, Claude admin: Organization settings > Plugins & skills > **Marketplaces** > marketplace menu > **Re-sync**.
3. Claude admin: in **Inventory**, find `<name>` and confirm the version matches `plugin.json`.
4. **New plugin only.** Claude admin: open `<name>` menu > **Default access** > **Not available**. Then **Group access...** > **Add groups** > `claude-pilot` > **Installed by default**. These match the plugin's lines under "Console settings" in [access-matrix.md](../enterprise/access-matrix.md).
5. Expected result:
   ```bash
   python scripts/access.py resolve claude-pilot     # new plugin: Installed by default
   python scripts/access.py resolve claude-hr        # new plugin: Not available
   ```
   Confirm with a test account in one group: Customize > Plugins shows the same.
6. Members get the change on their next session.

## D. Release to Microsoft 365 Copilot

1. Microsoft 365 admin: check out `main` at the merge commit and build the package:
   ```bash
   PRIVACY_URL=<privacy url> TERMS_URL=<terms url> WEBSITE_URL=<website url> \
     scripts/build-m365.sh <name>
   ```
   Expected: `Packages written to .../build/m365` and `build/m365/<name>.zip`.
2. **New plugin:** Microsoft 365 admin center > **Manage apps** > **Upload custom app** > select `build/m365/<name>.zip`.
   **Update:** upload the same way. The package keeps the same app ID, so it replaces the existing app's version rather than adding a second app.
3. In **Agents** > **Tools**, open `<name>`. Confirm the version matches `plugin.json`.
4. Set who gets it, from the plugin's row in [access-matrix.md](../enterprise/access-matrix.md):
   - groups at **Installed by default** or **Required**: **Installed for** > **Specific users/groups** > those Entra groups.
   - groups at **Available to install**: **Users** tab > **Available to specific users or groups** > those Entra groups.
   - no group listed: **Users** tab > **Block**.
5. Users receive the update on their next Copilot sync.

## E. Promote from pilot to released

After the pilot group has used a new plugin. The champion decides when.

1. Open a pull request that edits the plugin's rule in `enterprise/plugin-access.yaml`:
   - change `stage: pilot` to `stage: released`
   - add the department grants, e.g. `claude-hr: installed-by-default`
   - keep or remove `claude-pilot`
2. Run `python scripts/access.py matrix --write` and commit the updated matrix.
3. Champion approves. Merge.
4. Claude admin: apply the plugin's new lines under "Console settings" in [access-matrix.md](../enterprise/access-matrix.md) (**Group access...** > **Add groups**).
5. Microsoft 365 admin: repeat [D4](#d-release-to-microsoft-365-copilot) with the new groups.
6. Verify as in [C5](#c-merge-and-release-to-claude), using the department group.

No version bump: the plugin's files don't change.

## Rollback

Use when a released version misbehaves and the cause is clear (a wrong instruction, a broken skill).

**Stop it reaching anyone now** (minutes):

1. Claude admin: Inventory > `<name>` menu > **Default access** > **Not available**, and remove each **Group access** entry. Takes effect on members' next session.
2. Microsoft 365 admin: **Agents** > **Tools** > `<name>` > **Users** tab > **Block**.
3. Note the removed settings in the incident thread so they can be restored.

**Ship the previous content** (same day):

1. `git revert <merge commit>` on a new branch.
2. Bump `version` **past** the bad one (bad `0.3.0` → `0.3.1`). Claude only updates when the version changes, so reverting the number would leave members on the bad version.
3. Add a CHANGELOG line: `` `<name>` 0.3.1: revert 0.3.0 (<reason>). ``
4. Follow **A** to **D**. Step B can be shortened to one check of the skill that broke.
5. Restore the settings removed in "Stop it reaching anyone now" from [access-matrix.md](../enterprise/access-matrix.md).

## Escalation

Escalate to the AI team lead (see CODEOWNERS for `/.claude-plugin/`) and hand over: plugin name, bad and good versions, pull request link, and what users saw.

Treat it as a security incident instead, and follow your organisation's security incident process, if a released skill:

- contains personal data, a secret or a credential, or
- produces output that exposes data the user did not supply.

Do the "Stop it reaching anyone now" steps first. Then rotate any exposed secret before reverting, because the old content stays in Git history and in Microsoft 365 package history.

## Related

- [Enterprise access setup and rules](../enterprise/README.md)
- [Access matrix](../enterprise/access-matrix.md)
- [`enterprise/plugin-access.yaml`](../../enterprise/plugin-access.yaml)
- `scripts/package-plugin.py`: builds the pilot zips CI uploads
- `scripts/build-m365.sh`: builds Copilot packages
- [Manage plugins for your organization (Claude)](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization)
- [Roll out a plugin to your whole organization (Claude)](https://claude.com/docs/plugins/org-rollout)
- [Manage plugins for Copilot Cowork (Microsoft)](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-manage-plugins)
