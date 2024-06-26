<p align="center" >
    <img src="logo.png" alt="logo" width="250"/>
    <h3 align="center">cloudsnake 🐍</h3>
    <p align="center">Wrapping some awscli commands with beautiful TUI</p>
    <p align="center">Build with ❤ in Python</p>
</p>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Why cloudsnake](#why-cloudsnake)
- [Badges](#badges)
- [Examples](#examples)
- [Installation](#installation)
  - [Using pip](#using-pip)
  - [Using pipx with virtualenv (recommended)](#using-pipx-with-virtualenv-recommended)
  - [Local install](#local-install)
- [Uninstall](#uninstall)
  - [Using pip](#using-pip-1)
  - [Using pipx](#using-pipx)
- [Local development](#local-development)
  - [Local run with poetry](#local-run-with-poetry)
  - [Run & install pre-commit](#run--install-pre-commit)
- [TO DO](#to-do)
- [Improvements](#improvements)
  - [Positional flags](#positional-flags)
    - [Actually](#actually)
    - [Wants](#wants)
- [TOP LINKS](#top-links)
- [Available wrapper commands](#available-wrapper-commands)
- [Poetry commands](#poetry-commands)
- [Cloudsnake commands](#cloudsnake-commands)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Why cloudsnake

The main intention of this tool is to continue improving my python skills, get to know the AWS [boto3](https://aws.amazon.com/es/sdk-for-python/) SDK better, and learn how to create a CLI using [typer](https://typer.tiangolo.com/), [rich](https://github.com/Textualize/rich), and [textual](https://textual.textualize.io/). The tool tries to implement some commands from the official AWS cli ([aws cli](https://github.com/aws/aws-cli)), adding my own logic and with highlights (pretty print json output/table with typer/rich).

> [!IMPORTANT]
> Do not try to use part of this code in a productive app as it is currently untested. (visit #TODO page). I also don't know if this is the best way to use any of the tools that the application uses (boto3, typer, rich...), that is why any PR is welcome, it will be appreciated so I can continue improving my skills.


# Badges

|         |                                                                                                                                                                                                                                                                                                                                                         |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Code    | ![Code Size](https://img.shields.io/github/languages/code-size/containerscrew/tftools)                                                                                                                                                                                                                                                                  |
| CI/CD   | [![CI - Test](https://github.com/ofek/hatch-showcase/actions/workflows/test.yml/badge.svg)](https://github.com/ofek/hatch-showcase/actions/workflows/test.yml) [![CD - Build](https://github.com/ofek/hatch-showcase/actions/workflows/build.yml/badge.svg)](https://github.com/ofek/hatch-showcase/actions/workflows/build.yml)                        |
| Package | [![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)[![PyPI - Version](https://img.shields.io/pypi/v/hatch-showcase.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/hatch-showcase/) ![packaging](https://img.shields.io/badge/packaging-poetry-cyan.svg) |
| Meta    | [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/)                                                                                             |
| Linter  | [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)                                                                                                                                                                                            |

# Examples

Pending to add examples...


# Installation

## Using pip

```console
pip3 install cloudsnake
```
> [!WARNING]
> Probably your system will not allow this installation method due to a broken system package.

<details>
<summary>Example error</summary>
<br>
Error:
<br><br>
<pre>
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try 'pacman -S
    python-xyz', where xyz is the package you are trying to
    install.

    If you wish to install a non-Arch-packaged Python package,
    create a virtual environment using 'python -m venv path/to/venv'.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip.

    If you wish to install a non-Arch packaged Python application,
    it may be easiest to use 'pipx install xyz', which will manage a
    virtual environment for you. Make sure you have python-pipx
    installed via pacman.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
</pre>
</details>

## Using pipx with virtualenv (recommended)

Install `pipx` with your system package manager (`apt`, `dnf`, `pacman`...).

```console
pipx install cloudsnake
```

## Local install

```console
git clone https://github.com/containerscrew/cloudsnake.git
cd cloudsnake
make pipx-local-install
```

# Uninstall

## Using pip

```console
pip3 uninstall cloudsnake
```

## Using pipx

```console
pipx uninstall cloudsnake
```

# Local development

## Local run with poetry

```console
git clone https://github.com/containerscrew/cloudsnake.git
cd cloudsnake
make update
make run
```

## Run & install pre-commit

```console
make pre-commit-install
make run-pre-commit
```

# TO DO

* Documentation with docstrings
* Testing with pytest and boto3 mock
* Remove @classmethod
* Other...

# Improvements

## Positional flags

### Actually

```shell
cloudsnake --log-level debug --region us-east-1 --profile default ec2 describe-instance
```

### Wants

```shell
cloudsnake ec2 describe-instances --log-level debug --region us-east-1 --profile default --other-specific-flags-for-this-subdommand
```


# TOP LINKS

https://github.com/aws/aws-cli/blob/b6e7c5b79e4471713b2f7c660eff99b36d977064/awscli/customizations/sessionmanager.py#L83
https://stackoverflow.com/questions/57868722/unable-to-decode-aws-session-manager-websocket-output-in-python
https://github.com/aws/session-manager-plugin/blob/mainline/src/sessionmanagerplugin/session/shellsession/shellsession.go
Logger: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
Textual for beginners: https://mathspp.com/blog/textual-for-beginners
More of textual: https://dev.to/wiseai/textual-the-definitive-guide-part-1-1i0p
[Packaging projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
[Poetry](https://python-poetry.org/docs/)
Some examples using boto3 SDK https://docs.aws.amazon.com/code-library/latest/ug/python_3_ec2_code_examples.html
Mocking: https://github.com/getmoto/moto
Pytest github action: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

# Available wrapper commands

1. EC2 SSM CONNECTION
2. ECS SSM CONNECTION
3. SSM GET PARAMETERS
4. MYSQL IAM CONNECTION
5. AWS RESOURCE BY TAG OUTPUT TABLE
6. IAM policy detector
7. All regions: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_regions.html
8. Search for a domain in your current route53 hosted zone

# Poetry commands

```shell
poetry add boto3 dacite
poetry config pypi-token.pypi pypi-
poetry publish --build
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry publish --build -r testpypi
```

# Cloudsnake commands

```shell
cloudsnake --help
cloudsnake ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].{Instance:InstanceId,VpcId:VpcId,AZ:Placement.AvailabilityZone,Name:Tags[?Key==`Name`]|[0].Value}' --output json
cloudsnake ec2 describe-instances --filters "Name=instance-state-name,Values=running" --output json
# Get instance name of running instances
cloudsnake ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].{InstanceName:Tags[?Key==`Name`]|[0].Value}' --output json
cloudsnake ec2 describe-instances  --filters "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].Tags[?Key==`Name`].Value[][]'
cloudsnake rds describe-db-instances --query 'DBInstances[*].DBInstanceIdentifier'
```

# License

`cloudsnake` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
