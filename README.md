# Diff Manifests

[![PyPI](https://img.shields.io/pypi/v/diffmanifests.svg?color=brightgreen)](https://pypi.org/project/diffmanifests/)
[![Travis](https://travis-ci.com/craftslab/diffmanifests.svg?branch=master)](https://travis-ci.com/craftslab/diffmanifests)
[![Coverage](https://coveralls.io/repos/github/craftslab/diffmanifests/badge.svg?branch=master)](https://coveralls.io/github/craftslab/diffmanifests?branch=master)
[![License](https://img.shields.io/github/license/craftslab/diffmanifests.svg?color=brightgreen)](https://github.com/craftslab/diffmanifests/blob/master/LICENSE)



*Diff Manifests* is a tool used to see deeper differences between manifests via Gitiles API.



## Requirement

- python (3.7+)
- pip
- python-dev



## Installation

On Ubuntu / Mint, install *Diff Manifests* with the following commands:

```bash
apt update
apt install python3-dev python3-pip python3-setuptools
pip install diffmanifests
```

On OS X, install *Diff Manifests* via [Homebrew](https://brew.sh/) (or via [Linuxbrew](https://linuxbrew.sh/) on Linux):

```
TBD
```

On Windows, install *Diff Manifests* with the following commands:

```
pip install -U pywin32
pip install -U pyinstaller
pip install -Ur requirements.txt

pyinstaller --clean --name diffmanifests -F diff.py
```



## Updating

```bash
pip install diffmanifests --upgrade
```



## Running

```bash
diffmanifests \
    --config-file config.json \
    --manifest1-file manifest1.xml \
    --manifest2-file manifest2.xml \
    --output-file output.json
```



## Setting

*Diff Manifests* parameters can be set in the directory [config](https://github.com/craftslab/diffmanifests/blob/master/diffmanifests/config).

An example of configuration in [config.json](https://github.com/craftslab/diffmanifests/blob/master/diffmanifests/config/config.json):

```
{
  "gitiles": {
    "host": "localhost",
    "pass": "pass",
    "port": 80,
    "user": "user"
  }
}
```



## Feature

*Diff Manifests* supports to compare commit 2 with commit 1 in diagram A & B, but diagram C not supported.

![branch](branch.png)



## License

Project License can be found [here](https://github.com/craftslab/diffmanifests/blob/master/LICENSE).



## Reference

[git-repo/subcmds/diffmanifests](https://gerrit.googlesource.com/git-repo/+/master/subcmds/diffmanifests.py)
