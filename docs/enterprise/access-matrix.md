# Plugin access matrix

Generated from [`enterprise/plugin-access.yaml`](../../enterprise/plugin-access.yaml) by `uv run scripts/access.py matrix --write`. Do not edit by hand.

Each cell is what a member of only that group gets. **Bold** is a group override; plain text is the org default. A member in several groups gets the most permissive cell in their row.

Most to least permissive: Required > Installed by default > Available to install > Not available.

| Plugin | Stage | Org default | `claude-engineering` | `claude-ai-team` | `claude-hr` | `claude-sales` | `claude-marketing` | `claude-pilot` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `core` | released | Installed by default | Installed by default | Installed by default | Installed by default | Installed by default | Installed by default | Installed by default |
| `dev-review` | released | Not available | **Installed by default** | **Installed by default** | Not available | Not available | Not available | Not available |
| `hr-recruiting` | released | Not available | Not available | Not available | **Installed by default** | Not available | Not available | Not available |
| `sales-deal-desk` | released | Not available | Not available | Not available | Not available | **Installed by default** | **Available to install** | Not available |
| `mktg-content` | released | Not available | Not available | Not available | Not available | **Available to install** | **Installed by default** | Not available |

## Console settings

Set these in Organization settings > Plugins & skills > Inventory.

- `core`: Default access **Installed by default**.
- `dev-review`: Default access **Not available**.
  - Group access: `claude-engineering` **Installed by default**.
  - Group access: `claude-ai-team` **Installed by default**.
- `hr-recruiting`: Default access **Not available**.
  - Group access: `claude-hr` **Installed by default**.
- `sales-deal-desk`: Default access **Not available**.
  - Group access: `claude-sales` **Installed by default**.
  - Group access: `claude-marketing` **Available to install**.
- `mktg-content`: Default access **Not available**.
  - Group access: `claude-marketing` **Installed by default**.
  - Group access: `claude-sales` **Available to install**.
