import logging
import os
import typer
from typing import Annotated
from typing_extensions import Optional
from aws_client import aws_session, ec2_client
from aws_ec2 import EC2Data
from aws_ssm import SSMSession
from tui import ec2_list_selector
from logger import init_logger


# Define a class to store global options
class Settings:
    profile: Optional[str] = "default"
    log_level: Optional[str] = "INFO"
    region: Optional[str] = "eu-west-1"
    logger: Optional[logging.Logger] = logging.Logger


# Instantiate the global settings object
config = Settings()

"""Register new typer"""
app = typer.Typer(no_args_is_help=True)
ssm = typer.Typer(no_args_is_help=True)

"""Add subcommands/typer"""
app.add_typer(ssm, name="ssm", help="Manage ssm operations")


@ssm.command("start-session")
def start_session():
    """Declare subcommands for SSM command"""
    config.logger.info("Starting SSM session")
    session = aws_session(config.profile, config.region, config.logger)
    client = ec2_client(session)
    ec2 = EC2Data(client, config.logger)
    data = ec2.filter_ec2_data()
    instance_id = ec2_list_selector(config.logger, data)
    ssm = SSMSession(session, instance_id, config.region, config.profile, config.logger)
    ssm.start_session()


@app.callback(invoke_without_command=True)
def cli(
    profile: Annotated[
        str, typer.Option(help="AWS profile to use", show_default=True)
    ] = os.getenv("AWS_PROFILE"),
    log_level: Annotated[
        str, typer.Option(help="Log level", show_default=True)
    ] = "INFO",
    region: Annotated[
        str, typer.Option(help="AWS region", show_default=True)
    ] = "eu-west-1",
):
    """
    Entrypoint. Declare some global options for all the CLI
    This function will be executed when the CLI starts.
    """
    config.profile = profile
    config.region = region
    config.logger = init_logger(log_level)
