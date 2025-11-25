<p align="center" >
    <h3 align="center">cloudsnake 🐍</h3>
    <p align="center">Wrapping some useful AWS cli commands to operate AWS like EC2 SSM instance connection or RDS connection using IAM authentication</p>
    <p align="center">Built with ❤ in Python</p>
</p>

---

<p align="center" >
    <img alt="pre-commit" src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white">
    <img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/containerscrew/cloudsnake">
    <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/containerscrew/cloudsnake">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/containerscrew/cloudsnake">
    <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/containerscrew/cloudsnake">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/containerscrew/cloudsnake?style=social">
    <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/containerscrew/cloudsnake?style=social">
    <img alt="Python version" src="https://img.shields.io/badge/Python-3.12-3776AB.svg?style=flat&logo=python&logoColor=yellow">
    <img alt="PyPiP version" src="https://img.shields.io/pypi/v/cloudsnake">
    <img alt="License" src="https://img.shields.io/github/license/containerscrew/cloudsnake">
    <img alt="Linter" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json">
</p>

---

# Available implementations

* Connect to EC2 instances using SSM. You can pass the instance id (`--target`) or use the interactive menu (`--with-instance-selector`)

* Connect to the RDS instances using IAM db authentication.


# Examples

For the examples, you need to be authenticated to AWS account using your local credentials.

In your terminal, set the corresponding `AWS_PROFILE=MyProfile` if not using the default. (`~/.aws/credentials`)

## Connect to the EC2 instance using SSM

```shell
cloudsnake ssm start-session --with-instance-selector # will print all your instances in a terminal menu
cloudsnake ssm start-session --target i-XXXXXX  # connect to the instance specifying the target id
```

### Example

![example_ssm_connect](./example_ssm_connect.png)

## Connect to the RDS instance using IAM authentication db token

Please follow [this instructions](./docs/rds.md) to setup your RDS IAM authentication.

### Download the cert

By default, `cloudsnake` forces to use TLS/SSL connections.

```shell
cloudsnake rds download-cert --save-path /tmp
```

Other region:

```shell
cloudsnake --region us-east-1 download-cert --save-path /tmp
```

### Connect to the instance

Example for the region `eu-west-1`:

```shell
cloudsnake rds connect -h XXXXX.XXXXXX.eu-west-1.rds.amazonaws.com -u ADMIN --cert /tmp/rds-cert-eu-west-1.pem
```

### Example

pending to add new example

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

## Using pipx

Install `pipx` with your system package manager (`apt`, `dnf`, `pacman`...).

```console
pipx install cloudsnake
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

# Cloudsnake commands

```shell
cloudsnake --help
cloudsnake ssm start-session --with-instance-selector
cloudsnake ssm start-session --target i-xxxxxxx
cloudsnake rds connect -h XXXXX.XXXXXX.eu-west-1.rds.amazonaws.com -u ADMIN --cert /tmp/rds-cert-eu-west-1.pem
```

# License

`cloudsnake` is distributed under the terms of the [GPL3](https://spdx.org/licenses/GPL-3.0-or-later.html) license.
