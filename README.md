# diffmanifests

[![PyPI](https://img.shields.io/pypi/v/diffmanifests.svg?color=brightgreen)](https://pypi.org/project/diffmanifests/)
[![Coverage Status](https://coveralls.io/repos/github/craftslab/diffmanifests/badge.svg?branch=master)](https://coveralls.io/github/craftslab/diffmanifests?branch=master)
[![License](https://img.shields.io/github/license/craftslab/diffmanifests.svg?color=brightgreen)](https://github.com/craftslab/diffmanifests/blob/master/LICENSE)



*diffmanifests* is a tool used to see deeper differences between manifests via Gerrit & Gitiles API.



## Requirement

- Python >= 3.7



## Install

```bash
pip install diffmanifests
```



## Update

```bash
pip install diffmanifests --upgrade
```



## Run

```bash
diffmanifests --config-file config.json --manifest1-file manifest1.xml --manifest2-file manifest2.xml --output-file output.json
```



## Settings

*Diff Manifests* parameters can be set in the directory [config](https://github.com/craftslab/diffmanifests/blob/master/diffmanifests/config).

An example of configuration in [config.json](https://github.com/craftslab/diffmanifests/blob/master/diffmanifests/config/config.json):

```json
{
  "gerrit": {
    "pass": "pass",
    "url": "http://localhost:80",
    "user": "user"
  },
  "gitiles": {
    "pass": "pass",
    "retry": 1,
    "timeout": -1,
    "url": "http://localhost:80",
    "user": "user"
  }
}
```



## Features

*Diff Manifests* supports the following capabilities:

### 📊 Manifest Comparison

Compare commit 2 with commit 1 in diagram A/B/C to identify changes between manifest versions.

![branch](branch.png)



### 🏷️ Hashtags Support

The tool includes comprehensive support for querying changes with hashtags from the Gerrit REST API v3.12.1. This feature enhances change tracking and categorization.

**Key Benefits:**

- Automatic hashtag extraction from Gerrit changes
- Enhanced change categorization and filtering
- Better integration with Gerrit workflows
- Graceful fallback for changes without hashtags

**Output Structure:**

Each commit in the output JSON now includes a `hashtags` field containing an array of hashtags:

```json
{
  "author": "Developer Name <dev@example.com>",
  "branch": "master",
  "change": "https://gerrit.example.com/c/12345",
  "commit": "abc123def456789...",
  "committer": "Developer Name <dev@example.com>",
  "date": "2025-08-20 12:00:00 +0000",
  "diff": "ADD COMMIT",
  "hashtags": ["security", "cve", "bugfix"],
  "message": "Fix security vulnerability CVE-2025-1234",
  "repo": "platform/frameworks/base",
  "topic": "security-fix",
  "url": "https://android.googlesource.com/platform/frameworks/base/+/abc123def456789"
}
```

**Examples of hashtag usage:**

- `["feature", "ui", "enhancement"]` - New UI features
- `["bugfix", "critical"]` - Critical bug fixes
- `["security", "cve"]` - Security-related changes
- `[]` - Changes without hashtags (empty array)

**Technical Details:**

- Hashtags are retrieved using the [Gerrit REST API ChangeInfo entity](https://gerrit-documentation.storage.googleapis.com/Documentation/3.12.1/rest-api-changes.html#change-info)
- Automatic error handling ensures stable operation even when hashtags are unavailable
- Backward compatibility maintained for existing workflows



## License

Project License can be found [here](https://github.com/craftslab/diffmanifests/blob/master/LICENSE).



## Reference

[git-repo/subcmds/diffmanifests](https://gerrit.googlesource.com/git-repo/+/master/subcmds/diffmanifests.py)
