# AGENTS.md

Guidance for AI coding agents working in this repository.

## Project

`cloudsnake` is a Python CLI that wraps common AWS operations (SSM, SSO, CloudWatch Logs,
CloudTrail, Secrets Manager, RDS) behind a modern terminal UI. Built with
[Typer](https://typer.tiangolo.com/) (CLI), [Rich](https://rich.readthedocs.io/) and
[Textual](https://textual.textualize.io/) (TUI), and `boto3` for AWS access. Packaged and
distributed via Poetry / PyPI.

- Python: `^3.12` (codebase targets `py312`; use modern syntax — `str | None`, `list[...]`, `dict[...]`).
- Entry point: `cloudsnake.__main__:main` → `cloudsnake.cli.cli.app`.

## Commands

Tooling is driven by Poetry and a `Makefile` (run `make help` for the full list).

```bash
make install            # poetry install
make run                # run the CLI locally (poetry run python3 src/cloudsnake/__main__.py)
make run-tests          # poetry run pytest -v -s
make run-coverage       # pytest with coverage on tests/
make run-pre-commit     # pre-commit run -a
make build              # poetry build
```

- **Lint/format:** [Ruff](https://docs.astral.sh/ruff/) — config in `ruff.toml`. Line length 88,
  double quotes, rules `E4/E7/E9/F/I`, first-party package `cloudsnake`. Run `ruff check` / `ruff format`.
- **Type checking:** basedpyright (`[tool.basedpyright]` in `pyproject.toml`, `typeCheckingMode = "basic"`, venv `.venv`).
- **Tests:** pytest with `pytest-randomly`; AWS calls are mocked with [`moto`](https://docs.getmoto.org/).
  `moto` is a **test-only** dependency — never import it from `src/`.
- **Pre-commit:** see `.pre-commit-config.yaml` (whitespace/EOF/yaml/json/toml hygiene, broken-symlink check).
- **Changelog:** managed by cocogitto (`cog bump` runs `cog changelog`); do not hand-edit `CHANGELOG.md`.

## Commit & release workflow

Commits use cocogitto (conventional commits) — never raw `git commit`:

```bash
cog commit <type> "message"        # type: feat|fix|refactor|build|chore|docs|test|ci|perf|style|revert
cog commit <type> "message" -B     # -B marks a BREAKING CHANGE
```

`-a` stages all changes (`git add -A`) into that single commit, so it sweeps **every** modified
file — don't chain multiple `cog commit -a` expecting per-commit staging. For grouped commits,
`git add <files>` first, then `cog commit <type> "message"` without `-a`.

Releasing (after the commits are in):

```bash
cog bump --version X.Y.Z         # updates pyproject.toml, regenerates CHANGELOG.md, commits and tags
```

The `pre_bump_hooks` in `cog.toml` run `poetry version {{version}}` (syncs `pyproject.toml`) and
`cog changelog` automatically — no manual version edit needed.

## Layout

```
src/cloudsnake/
  __main__.py        # entry point -> app()
  cli/               # Typer command groups (one file per AWS service)
    cli.py           # root app + @app.callback() entrypoint (global --profile/--region/--log-level)
    dto.py           # dataclasses + enums (Common context, OutputMode, LoggingLevel, ...)
    {ssm,sso,logs,trail,secrets_manager,rds}.py
  sdk/               # boto3 service wrappers, each subclassing App
    aws.py           # App ABC: lazy boto3 client, retries config, time-string parsing
    session.py       # SessionWrapper -> builds the boto3.Session
  decorators.py      # @handle_aws_errors (maps boto3 exceptions to clean CLI errors)
  utils.py           # apply_context_overrides, with_aws_overrides, config/file helpers
  logger.py          # RichHandler-based logging
  console.py         # shared Rich Console
  tui.py             # Textual selector app
  models/            # data models for the TUI
tests/               # pytest suite (mirrors src layout; sdk/ for wrapper tests)
docs/                # per-feature usage docs (README.md is the main reference)
```

## Architecture & conventions

- **Command groups:** each AWS service is a `typer.Typer()` registered in `cli/cli.py` via
  `app.add_typer(...)`. The root `@app.callback()` (`entrypoint`) builds a `SessionWrapper`,
  stores a `Common` dataclass (session, profile, region) in `ctx.obj`, and initializes logging.
- **Per-command profile/region overrides:** `--profile/-p` and `--region/-r` are global (before the
  subcommand) but can also be passed after a subcommand. This is wired with:
  - a group `@<group>.callback()` calling `apply_context_overrides(ctx, region, profile)`, and
  - `@with_aws_overrides` on leaf commands, which rewrites `__signature__` to inject `--region/-r`
    and `--profile/-p` without touching the function body.
  Convention: **`-r` always means `--region`** across the whole CLI. If a command needs a short flag
  that would clash with `-r`/`-p`, choose a different alias (e.g. `trail events` uses `--resource`
  with no short form).
- **SDK wrappers:** every service wrapper subclasses `App` (`sdk/aws.py`). `App` lazily creates the
  boto3 client (`client` property), applies a standard retry `Config`, and exposes helpers like
  `_parse_time_str` ("15m", "1h", "2d"). Subclasses implement the `client_name` property.
- **Error handling:** decorate commands with `@handle_aws_errors` to convert `NoCredentialsError`,
  `ClientError`, `BotoCoreError`, and `KeyboardInterrupt` into friendly Rich output + `typer.Exit`.
  Decorator order on leaf commands is `@<group>.command(...)` → `@handle_aws_errors` → `@with_aws_overrides`.
- **Output:** use the shared `console` from `console.py` (Rich) for user-facing output; use the
  `logging` module (configured in `logger.py`) for diagnostics. `--log-level debug` enables boto3/botocore logs.
- **Typing:** prefer built-in generics and `X | None` over `typing.Optional`/`List`/`Dict`.
  Do not add `typing-extensions`.

## Gotchas

- Keep `moto` and other test-only packages out of `[tool.poetry.dependencies]` and out of `src/` imports.
- The `rds` command group exists under `src/cloudsnake/cli/rds.py` and `docs/rds.md` but is **not**
  currently registered in `cli/cli.py`.
- SSM sessions require the AWS `session-manager-plugin` to be installed on the host.
- After editing dependencies in `pyproject.toml`, update `poetry.lock` (`poetry lock`).
