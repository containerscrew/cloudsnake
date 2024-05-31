<p align="center" >
    <img src="logo.png" alt="logo" width="250"/>
    <h3 align="center">cloudsnake 🐍</h3>
    <p align="center">Wrapping some awscli commands with beautiful TUI</p>
    <p align="center">Build with ❤ in Python</p>
</p>

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Introduction](#introduction)
- [Installation](#installation)
- [Badges](#badges)
- [TO DO](#to-do)
- [TOP LINKS](#top-links)
- [Tools](#tools)
- [Poetry commands](#poetry-commands)
- [Cloudsnake commands](#cloudsnake-commands)
  - [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Introduction

Lorem ipsum....

# Installation

```console
pip3 install cloudsnake
pipx install cloudsnake
```

# Badges

|         |                                                                                                                                                                                                                                                                                                                                                         |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Code    | ![Code Size](https://img.shields.io/github/languages/code-size/containerscrew/tftools)                                                                                                                                                                                                                                                                  |
| CI/CD   | [![CI - Test](https://github.com/ofek/hatch-showcase/actions/workflows/test.yml/badge.svg)](https://github.com/ofek/hatch-showcase/actions/workflows/test.yml) [![CD - Build](https://github.com/ofek/hatch-showcase/actions/workflows/build.yml/badge.svg)](https://github.com/ofek/hatch-showcase/actions/workflows/build.yml)                        |
| Package | [![python](https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)[![PyPI - Version](https://img.shields.io/pypi/v/hatch-showcase.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/hatch-showcase/) ![packaging](https://img.shields.io/badge/packaging-poetry-cyan.svg) |
| Meta    | [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/)                                                                                             |
| Linter  | [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)                                                                                                                                                                                            |




# TO DO

* Implement python textual for OptionList
* Documentation with docstrings
* 

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

# Tools

1. EC2 SSM CONNECTION
2. ECS SSM CONNECTION
3. SSM GET PARAMETERS
4. MYSQL IAM CONNECTION
5. AWS RESOURCE BY TAG OUTPUT TABLE
6. All regions: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_regions.html

# Poetry commands

```shell
poetry add boto3 dacite
poetry config pypi-token.pypi pypi-
poetry publish --build
```

# Cloudsnake commands

```shell
cloudsnake --help
cloudsnake ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].{Instance:InstanceId,VpcId:VpcId,AZ:Placement.AvailabilityZone,Name:Tags[?Key==`Name`]|[0].Value}' --output json
cloudsnake ec2 describe-instances --filters "Name=instance-state-name,Values=running" --output json
# Get instance name of running instances
cloudsnake ec2 describe-instances --filters "Name=instance-state-name,Values=running" --query 'Reservations[*].Instances[*].{InstanceName:Tags[?Key==`Name`]|[0].Value}' --output json
```

## License

`cloudsnake` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
