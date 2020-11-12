# Diff Manifests

[![PyPI](https://img.shields.io/pypi/v/diffmanifests.svg?color=brightgreen)](https://pypi.org/project/diffmanifests/)
[![Travis](https://travis-ci.com/craftslab/diffmanifests.svg?branch=master)](https://travis-ci.com/craftslab/diffmanifests)
[![Coverage](https://coveralls.io/repos/github/craftslab/diffmanifests/badge.svg?branch=master)](https://coveralls.io/github/craftslab/diffmanifests?branch=master)
[![License](https://img.shields.io/github/license/craftslab/diffmanifests.svg?color=brightgreen)](https://github.com/craftslab/diffmanifests/blob/master/LICENSE)



*Diff Manifests* is a tool used to see deeper differences between manifests via Gerrit & Gitiles API.


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

```
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



## Feature

*Diff Manifests* supports to compare commit 2 with commit 1 in diagram A/B/C.

![branch](branch.png)



## Reference

[git-repo/subcmds/diffmanifests](https://gerrit.googlesource.com/git-repo/+/master/subcmds/diffmanifests.py)



## License

Project License can be found [here](https://github.com/craftslab/diffmanifests/blob/master/LICENSE).
