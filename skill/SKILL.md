---
name: diffmanifests
description: Compare manifest XML files via Gerrit and Gitiles APIs, producing JSON/txt/xlsx reports. Use when comparing Android or repo manifest versions, diffing manifest files, or when the user mentions diffmanifests, manifest comparison, or Gerrit/Gitiles manifest diffs.
---

# diffmanifests Skill (OpenClaw)

Use the **diffmanifests** CLI to compare two manifest XML files and get detailed commit/change reports. Install with `pip install diffmanifests`. Configuration lives in a JSON file; all four CLI arguments are required.

## Installation

```bash
pip install diffmanifests
```

Upgrade: `pip install diffmanifests --upgrade`

## Configuration

Configuration is read from a JSON file. **Bundled config** (packed with this skill for OpenClaw hub): use `config.json` in this skill directory. Reference structure:

| Section   | Parameter   | Type    | Description |
|-----------|-------------|---------|-------------|
| **gerrit** | `url`       | string  | Gerrit instance URL |
|           | `user`      | string  | Auth username |
|           | `pass`      | string  | Password or API token |
|           | `query.option` | array | e.g. `["CURRENT_REVISION"]` |
| **gitiles** | `url`     | string  | Gitiles instance URL |
|           | `user`      | string  | Auth username |
|           | `pass`      | string  | Password or API token |
|           | `retry`     | integer | Retry attempts (default: 1) |
|           | `timeout`   | integer | Timeout in seconds (-1 = no timeout) |

Example `config.json`:

```json
{
  "gerrit": {
    "url": "https://android-review.googlesource.com",
    "user": "",
    "pass": "",
    "query": { "option": ["CURRENT_REVISION"] }
  },
  "gitiles": {
    "url": "https://android.googlesource.com",
    "user": "",
    "pass": "",
    "retry": 1,
    "timeout": -1
  }
}
```

## Parameters (CLI)

| Argument            | Required | Description |
|---------------------|----------|-------------|
| `--config-file`     | ✅       | Path to configuration JSON file |
| `--manifest1-file`  | ✅       | Path to first (older) manifest XML |
| `--manifest2-file`  | ✅       | Path to second (newer) manifest XML |
| `--output-file`     | ✅       | Output path; format by extension: `.json`, `.txt`, `.xlsx` |

## Basic usage

Use the bundled `config.json` in this skill directory (or pass your own):

```bash
diffmanifests \
  --config-file config.json \
  --manifest1-file path/to/older.xml \
  --manifest2-file path/to/newer.xml \
  --output-file path/to/output.json
```

From inside the skill directory: `--config-file config.json`.

Output format is chosen by `--output-file` extension: `.json` (structured), `.txt` (plain text), `.xlsx` (Excel).

## Output (JSON)

Each change entry can include: `author`, `branch`, `change`, `commit`, `committer`, `date`, `diff` (e.g. ADD COMMIT / REMOVE COMMIT), `hashtags`, `message`, `repo`, `topic`, `url`.

## When to use

- User asks to compare two manifest files or manifest versions.
- User mentions diffmanifests, Gerrit manifest diff, or Gitiles manifest comparison.
- Task involves Android/repo manifest version analysis or change reports.
