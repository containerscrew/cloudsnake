<p align="center" >
    <h3 align="center">cloudsnake 🐍</h3>
    <p align="center">Wrapping some useful AWS cli commands to operate some services like EC2, SSO and more</p>
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
    <img alt="PyPip downloads" src="https://img.shields.io/pypi/dm/cloudsnake">
</p>

---

In your terminal, set the corresponding `AWS_PROFILE=MyProfile` if not using the default. (`~/.aws/credentials`). Copy [this helper function](./aws-profile.sh) called `aws-profile` into your favourite shell (`.bashrc`, `.zshrc`, `~/.config/fish/function`) to easily switch between AWS profiles. In case of using `fish` shell, use [this other function](./aws-profile.fish).

<br><br>
<p align="center">
    <img align="center" alt="SSM session" src="docs/img/aws-profile.gif">
<h3 align="center">aws-profile</h3>
</p>

---
<br><br>
<p align="center">
    <img align="center" alt="SSM session" src="docs/img//cloudsnake-ssm-session.gif">
<h3 align="center">SSM session</h3>
</p>

Install the [REQUIRED plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html) to use SSM sessions.


```shell
cloudsnake ssm start-session -is # will print all your instances in a terminal menu
cloudsnake ssm start-session --target i-XXXXXX  # connect to the instance specifying the target id
```

---

<br><br>
<p align="center">
    <img align="center" alt="SSM get parameter" src="docs/img/cloudsnake-ssm-parameter.gif">
<h3 align="center">SSM parameter</h3>
</p>

```shell
cloudsnake ssm get-parameter # default region eu-west-1
cloudsnake --region us-east-1 ssm get-parameters # specify region
```
---

<br><br>
<p align="center">
    <img align="center" alt="SSO get-credentials" src="docs/img/cloudsnake-sso-get-credentials.png">
<h3 align="center">SSO get-credentials</h3>
</p>

```shell
cloudsnake --region eu-west-1 sso get-credentials --start-url https://myapp.awsapps.com/start
```

> [!NOTE]
> This command will open your default browser. You will need to approve manually the authentication.
> More use cases and examples for `cloudsnake sso get-credentials` can be found in [`docs/sso-get-credentials.md`](./docs/sso-get-credentials.md).

# Installation

## Using pipx (Recommended)

Install `pipx` with your system package manager (`apt`, `dnf`, `pacman`...).

```console
pipx install cloudsnake
```

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

# Uninstall

```bash
pipx uninstall cloudsnake
# or
pip3 uninstall cloudsnake
```

## Debug AWS SDK API calls

```shell
cloudsnake --log-level debug command subcommand [options]
```

# License

`cloudsnake` is distributed under the terms of the [GPL3](https://spdx.org/licenses/GPL-3.0-or-later.html) license.
