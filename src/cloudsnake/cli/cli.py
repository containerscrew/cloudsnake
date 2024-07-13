import os
import typer
from typing import Optional
from importlib.metadata import version
from cloudsnake.cli.dto import Common, LoggingLevel
from cloudsnake.cli.ec2 import ec2
from cloudsnake.cli.ssm import ssm
from cloudsnake.cli.rds import rds
from cloudsnake.sdk.boto3_session import SessionWrapper
from cloudsnake.logger import init_logger
from cloudsnake.tui import Tui


# App version reading the package version from the pyproject.toml
app_version = version("cloudsnake")

# Main app Typer
app = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)

# Add subcommands to the main typer
app.add_typer(ec2, name="ec2", help="Manage EC2 operations")
app.add_typer(ssm, name="ssm", help="Manage SSM operations")
app.add_typer(rds, name="rds", help="Manage RDS operations")
# app.add_typer(sso, name="sso", help="Manage sso operations")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(
            typer.style(
                f"Using cloudsnake version: v{app_version}",
                fg=typer.colors.GREEN,
                bold=True,
            )
        )
        raise typer.Exit()


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
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
):
    """
    Entry point function for the cloudsnake CLI.

    Args:
        ctx (typer.Context): The Typer context object.
        profile (Optional[str], optional): AWS profile to use. Defaults to the value of the AWS_PROFILE environment variable.
        log_level (Optional[LoggingLevel], optional): Logging level for the app custom code and boto3. Defaults to LoggingLevel.WARNING.
        region (Optional[str], optional): AWS region. Defaults to "eu-west-1".
        version (Optional[bool], optional): Show the application's version and exit. Defaults to None.
    """
    session = SessionWrapper(profile, region).with_local_session()
    tui = Tui()
    ctx.obj = Common(session, profile, region, tui)
    logger = init_logger(log_level.value)
    logger.info("Starting cloudsnake 🐍☁")
