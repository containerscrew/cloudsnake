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


app_version = version("cloudsnake")


"""Register new app typer"""
app = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


"""Add subcommands/typer"""
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
    cloudsnake is an AWS cli wrapper with beautiful TUI using rich, typer and textual. It does not implement all the
    commands, flags... of the official cli. It's just an example to see how to use aws sdk boto3, rich and
    typer.
    Example: cloudsnake ec2 describe-instances
    """
    session = SessionWrapper(profile, region).with_local_session()
    ctx.obj = Common(session, profile, region)
    logger = init_logger(log_level.value)
    logger.info("Starting cloudsnake 🐍☁")
