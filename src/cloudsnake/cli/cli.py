import os
from importlib.metadata import version
from typing import Optional

import typer
from rich import traceback

from cloudsnake.cli.dto import Common, LoggingLevel
from cloudsnake.cli.logs import cw_logs
from cloudsnake.cli.secrets_manager import secrets_manager
from cloudsnake.cli.ssm import ssm
from cloudsnake.cli.sso import sso
from cloudsnake.cli.trail import trail
from cloudsnake.logger import init_logger
from cloudsnake.sdk.session import SessionWrapper

traceback.install(show_locals=False)

# App version reading the package version from the pyproject.toml
APP_VERSION = version("cloudsnake")

# Declare app and add subcommands
app = typer.Typer(
    name="cloudsnake",
    help=f"🐍 A modern CLI to interact with AWS resources. (c) 2025 containerscrew - version {APP_VERSION}",
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
    rich_markup_mode="rich",
)

app.add_typer(ssm, name="ssm", help="Manage SSM operations")
app.add_typer(sso, name="sso", help="Manage SSO operations")
app.add_typer(cw_logs, name="logs", help="Manage CloudWatch Logs operations")
app.add_typer(trail, name="trail", help="Manage CloudTrail operations")
app.add_typer(
    secrets_manager, name="secrets-manager", help="Manage Secrets Manager operations"
)


@app.callback()
def entrypoint(
    ctx: typer.Context,
    profile: Optional[str] = typer.Option(
        os.getenv("AWS_PROFILE"),
        "--profile",
        "-p",
        help="AWS profile to use",
        show_default=True,
    ),
    log_level: Optional[LoggingLevel] = typer.Option(
        LoggingLevel.WARNING,
        "--log-level",
        "-l",
        help="Logging level for the app custom code and boto3",
        case_sensitive=False,
        is_eager=True,
    ),
    region: Optional[str] = typer.Option(
        "eu-west-1", "--region", "-r", help="AWS region", show_default=True
    ),
):
    """
    Entry point for the cloudsnake CLI.
    """
    logger = init_logger(log_level.value)

    # Create resources
    session = SessionWrapper(profile, region).with_local_session()

    # Store shared context
    ctx.obj = Common(
        session=session,
        profile=profile,
        region=region,
    )

    logger.debug("Context initialized successfully")
