import os
from dataclasses import dataclass
from enum import Enum

import boto3
import typer
from typing import Annotated
from typing_extensions import List

from cloudsnake.session import SessionWrapper
from cloudsnake.logger import init_logger
from cloudsnake.ec2 import InstanceWrapper
from cloudsnake.ssm import StartSessionWrapper


class OutputMode(str, Enum):
    json = "json"
    table = "table"


class LoggingLevel(str, Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


"""Register new typer"""
app = typer.Typer(no_args_is_help=True, pretty_exceptions_short=True)
ssm = typer.Typer(no_args_is_help=True, pretty_exceptions_short=True)
ec2 = typer.Typer(no_args_is_help=True, pretty_exceptions_short=True)

"""Add subcommands/typer"""
app.add_typer(ssm, name="ssm", help="Manage ssm operations")
app.add_typer(ec2, name="ec2", help="Manage ec2 operations")


@dataclass
class Common:
    session: boto3.Session
    profile: str
    region: str


@ec2.command(
    "describe-instances",
    help="Describe EC2 instances data with filters and query as a parameter",
)
def describe_instances(
    ctx: typer.Context,
    filters: Annotated[
        List[str], typer.Option(help="Filters for EC2 instances in Name=Value format")
    ] = None,
    query: Annotated[str, typer.Option(help="Query to format the output")] = None,
    output: Annotated[
        OutputMode,
        typer.Option(help="Output mode", case_sensitive=True),
    ] = OutputMode.json,
):
    """Invoke ec2 describe-instances"""
    instances = InstanceWrapper(
        ctx.obj.session, filters=filters, query=query, output=output
    )
    instances.print_console()


@ssm.command("start-session", help="Start session with the given target id")
def start_session(
    ctx: typer.Context,
    target: str = typer.Option(help="Target id of the instance"),
    reason: Annotated[
        str, typer.Option(help="Reason of the connection")
    ] = "default-connection",
):
    ssm_session = StartSessionWrapper(ctx.obj.session, target=target, reason=reason)
    ssm_session.start_session(ctx.obj.region, ctx.obj.profile)


@app.callback()
def entrypoint(
    ctx: typer.Context,
    profile: Annotated[
        str, typer.Option(help="AWS profile to use", show_default=True)
    ] = os.getenv("AWS_PROFILE"),
    log_level: Annotated[
        LoggingLevel,
        typer.Option(
            help="Logging level for the app custom code and boto3",
            case_sensitive=False,
        ),
    ] = LoggingLevel.INFO,
    region: Annotated[
        str, typer.Option(help="AWS region", show_default=True)
    ] = "eu-west-1",
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
