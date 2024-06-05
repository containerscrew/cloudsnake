import os
from dataclasses import dataclass
from enum import Enum

import boto3
import typer
from typing import Annotated
from typing_extensions import List

from cloudsnake.session import SessionWrapper
from cloudsnake.logger import init_logger
from cloudsnake.ec2 import EC2InstanceWrapper
from cloudsnake.ssm import SSMStartSessionWrapper
from cloudsnake.sso_oidc import SSOIDCWrapper


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
app = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)
ssm = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)
ec2 = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)
sso = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


"""Add subcommands/typer"""
app.add_typer(ssm, name="ssm", help="Manage ssm operations")
app.add_typer(ec2, name="ec2", help="Manage ec2 operations")
app.add_typer(sso, name="sso", help="Manage sso operations")


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

    instances = EC2InstanceWrapper(
        ctx.obj.session, "ec2", filters=filters, query=query, output=output
    )
    instances.print_ec2_instances()


@ssm.command(
    "start-session", help="Start session with the given target id", no_args_is_help=True
)
def start_session(
    ctx: typer.Context,
    target: Annotated[str, typer.Option(help="Target id of the instance")] = None,
    reason: Annotated[
        str, typer.Option(help="Reason of the connection")
    ] = "default-connection",
    with_instance_selector: Annotated[
        bool,
        typer.Option(
            help="Print interactive menu and select the instance you want to connect"
        ),
    ] = False,
):
    if with_instance_selector:
        filters='Name=instance-state-name,Values=running'
        query='Reservations[*].Instances[*].{InstanceName:Tags[?Key==`Name`]|[0].Value}'
        ec2_instances = EC2InstanceWrapper(
            ctx.obj.session, "ec2", filters=filters, query=query,
        )
        ec2_instances.describe_ec2_instances()
    else:
        if target is None:
            raise ValueError("You should pass --target flag with a valid instance id")
        ssm_session = SSMStartSessionWrapper(
            ctx.obj.session, "ssm", target=target, reason=reason
        )
        ssm_session.start_session(ctx.obj.region, ctx.obj.profile)

@sso.command(
    "fetch-sso-credentials", help="Fetch your AWS account credentials using SSO", no_args_is_help=True
)
def fetch_sso_credentials(
    ctx: typer.Context,
    start_url: str = typer.Option(help="SSO start url. Example: https://XXXXXX.awsapps.com/start") ,   
): 
    oidc = SSOIDCWrapper(ctx.obj.session, "sso-oidc")
    client_id, client_secret = oidc.device_registration()
    oidc.get_auth_device(client_id, client_secret, start_url)
    


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
    ] = LoggingLevel.WARNING,
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
