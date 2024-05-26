<div style="text-align:center">
    <h1>cloudsnake 🐍</h1>
    <img src="img/aws.png" width="150"/>
    <img src="img/snake.png" width="150"/>
    <h3>Wrapping some awscli commands with beautiful TUI</h3>
    <h3>Build with ❤ in Python</h3>
</div>


# Introduction


# Installation

```console
pip3 install cloudsnake
```

# Badges

| | |
| --- | --- |
| CI/CD | [![CI - Test](https://github.com/ofek/hatch-showcase/actions/workflows/test.yml/badge.svg)](https://github.com/ofek/hatch-showcase/actions/workflows/test.yml) [![CD - Build](https://github.com/ofek/hatch-showcase/actions/workflows/build.yml/badge.svg)](https://github.com/ofek/hatch-showcase/actions/workflows/build.yml) |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/hatch-showcase.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/hatch-showcase/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/hatch-showcase.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/hatch-showcase/) |
| Meta | [![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/ambv/black) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) [![GitHub Sponsors](https://img.shields.io/github/sponsors/ofek?logo=GitHub%20Sponsors&style=social)](https://github.com/sponsors/ofek) |





<p style="text-align: center" >
  <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/containerscrew/awstools">
</p>

[![python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![pydocstyle](https://img.shields.io/badge/pydocstyle-enabled-AD4CD3)](http://www.pydocstyle.org/en/stable/)

<p align="center" >
<a href="https://github.com/nanih98/aws-tools/actions/workflows/releases.yml"><img alt="Pipeline" src="https://github.com/nanih98/aws-tools/actions/workflows/releases.yml/badge.svg"></a>
<a href="https://github.com/nanih98/aws-tools/actions/workflows/lint.yml"><img alt="Pipeline" src="https://github.com/nanih98/aws-tools/actions/workflows/lint.yml/badge.svg"></a>
<a href="https://github.com/nanih98/aws-tools/blob/main/LICENSE"><img alt="LICENSE" src="https://img.shields.io/github/license/nanih98/aws-tools"></a>
</p>



# TO DO 

* Implement websocket protocol of ssm-session-plugin
* Implement python textual for OptionList



# TOP LINKS

https://github.com/aws/aws-cli/blob/b6e7c5b79e4471713b2f7c660eff99b36d977064/awscli/customizations/sessionmanager.py#L83  
https://stackoverflow.com/questions/57868722/unable-to-decode-aws-session-manager-websocket-output-in-python  
https://github.com/aws/session-manager-plugin/blob/mainline/src/sessionmanagerplugin/session/shellsession/shellsession.go  
Logger: https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output  
Textual for beginners: https://mathspp.com/blog/textual-for-beginners  
More of textual: https://dev.to/wiseai/textual-the-definitive-guide-part-1-1i0p
[Packaging projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
[Poetry](https://python-poetry.org/docs/)

# Tools

1. EC2 SSM CONNECTION
2. ECS SSM CONNECTION
3. SSM GET PARAMETERS
4. MYSQL IAM CONNECTION
5. AWS RESOURCE BY TAG OUTPUT TABLE

# Poetry commands

```shell
poetry add boto3 dacite 
poetry config pypi-token.pypi pypi-
poetry publish --build
```

## License

`cloudsnake` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.