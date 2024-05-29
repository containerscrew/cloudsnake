import logging
import os
from enum import Enum

import typer
from typing import Annotated
from typing_extensions import Optional, List

from cloudsnake.aws_ec2 import InstanceWrapper
from cloudsnake.aws_session import SessionWrapper
from logger import init_logger


class LoggingLevel(str, Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# Define a class to store global options
class Settings:
    profile: Optional[str] = "default"
    log_level: Optional[str] = "WARNING"
    region: Optional[str] = "eu-west-1"
    logger: Optional[logging.Logger] = logging.Logger


# Instantiate the global settings object
config = Settings()

"""Register new typer"""
app = typer.Typer(no_args_is_help=True, pretty_exceptions_short=True)
ssm = typer.Typer(no_args_is_help=True, pretty_exceptions_short=True)
ec2 = typer.Typer(no_args_is_help=True, pretty_exceptions_short=True)

"""Add subcommands/typer"""
app.add_typer(ssm, name="ssm", help="Manage ssm operations")
app.add_typer(ec2, name="ec2", help="Manage ec2 operations")


@ec2.command("describe-instances")
def describe_instances(
    filters: Annotated[
        List[str], typer.Option(help="Filters for EC2 instances in Name=Value format")
    ] = None,
):
    """Invoke ec2 describe-instances"""
    session = SessionWrapper(config.profile, config.region).with_local_session()
    instances = InstanceWrapper.from_session(session)
    instances.describe_ec2_instances(filters)


# @ssm.command("start-session")
# def start_session():
#     """Declare subcommands for SSM command"""
#     config.logger.info("Start SSM session")
#     session = aws_session(config.profile, config.region, config.logger)
#     instances = Instances(session)
#     running_ec2 = instances.get_custom_instance_data()
#     ec2_list_selector(running_ec2)
#     # ssm = SSMSession(session, instance_id, config.region, config.profile, config.logger)
#     # ssm.start_session()


@app.callback(invoke_without_command=True)
def cli(
    profile: Annotated[
        str, typer.Option(help="AWS profile to use", show_default=True)
    ] = os.getenv("AWS_PROFILE"),
    log_level: Annotated[
        LoggingLevel, typer.Option(help="Logging level for the app custom code and boto3", case_sensitive=False)
    ] = LoggingLevel.WARNING,
    region: Annotated[
        str, typer.Option(help="AWS region", show_default=True)
    ] = "eu-west-1",
):
    """
    cloudsnake is an AWS cli wrapper with beautiful TUI using rich, typer and textual. It does not implement all the
    commands, flags... of the official cli. It's just an example to see how to use aws sdk boto3, rich,
    typer...
    Example: cloudsnake ec2 describe-instances
    """
    config.profile = profile
    config.region = region
    config.logger = init_logger(log_level.value)

    config.logger.info("Starting cloudsnake 🐍☁")
