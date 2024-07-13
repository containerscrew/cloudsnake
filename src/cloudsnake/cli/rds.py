import os
from typing import Optional
import typer
from cloudsnake.cli.dto import OutputMode
from cloudsnake.sdk.rds_session import RDSInstanceConnectWrapper


rds = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@rds.command(
    "generate-db-auth-token",
    help="Generate RDS auth token for IAM authentication",
)
def generate_db_auth_token(
    ctx: typer.Context,
    hostname: str = typer.Option(
        ..., "--hostname", "-h", help="Hostname of the RDS instance"
    ),
    port: Optional[int] = typer.Option(3306, "--port", "-p", help="DB instance port"),
    username: str = typer.Option(
        ...,
        "--username",
        "-u",
        help="Database username to connect",
        case_sensitive=True,
    ),
    print: Optional[bool] = typer.Option(
        True, "--no-print", "-np", help="Do not print the token in the console"
    ),
):
    """Invoke RDS generate-db-auth-token"""
    rds = RDSInstanceConnectWrapper.with_client(
        "rds",
        ctx.obj.session,
        hostname=hostname,
        port=port,
        db_username=username,
        region=ctx.obj.region,
    )
    token = rds.get_db_auth_token()
    if print:
        ctx.obj.tui.pretty_print(token, "text", True)


def validate_hostname(ctx: typer.Context, param: typer.CallbackParam, value: str):
    if not ctx.params.get("with_instance_selector") and not value:
        raise typer.BadParameter(
            "hostname is required if --with-instance-selector is not used"
        )
    return value


@rds.command(
    "connect",
    help="Connect to the RDS instance using a token",
)
def rds_connect(
    ctx: typer.Context,
    hostname: Optional[str] = typer.Option(
        None,
        "--hostname",
        "-h",
        callback=validate_hostname,
        help="Hostname of the RDS instance",
    ),
    port: Optional[int] = typer.Option(3306, "--port", "-p", help="DB instance port"),
    username: str = typer.Option(
        ...,
        "--username",
        "-u",
        help="Database username to connect",
        case_sensitive=True,
    ),
    cert: str = typer.Option(..., "--cert", "-c", help="Path to the certificate"),
    with_instance_selector: Optional[bool] = typer.Option(
        False,
        "--with-instance-selector",
        "-is",
        help="Prompt a terminal menu and select the instance you want to connect. --target flag is no longer used",
    ),
):
    """Invoke generate-db-auth-token command to obtain the token"""
    rds = RDSInstanceConnectWrapper.with_client(
        "rds",
        ctx.obj.session,
        hostname=hostname,
        port=port,
        db_username=username,
        region=ctx.obj.region,
        cert=cert,
    )
    token = rds.get_db_auth_token()
    rds.db_connect(token)


@rds.command(
    "download-cert",
    help="Download the RDS certificate",
)
def download_rds_certificate(
    ctx: typer.Context,
    save_path: Optional[str] = typer.Option(
        os.getcwd(), "--save-path", "-sp", help="Path to save the certificate"
    ),
):
    """Invoke RDS download-cert"""
    rds = RDSInstanceConnectWrapper.with_client(
        "rds", ctx.obj.session, region=ctx.obj.region
    )
    rds.download_cert(save_path)


@rds.command(
    "describe-db-instances",
    help="Download the RDS certificate",
)
def describe_db_instances(
    ctx: typer.Context,
    filters: Optional[str] = typer.Option(
        None, "--filters", "-f", help="Filters for EC2 instances in Name=Value format"
    ),
    query: Optional[str] = typer.Option(
        None, "--query", "-q", help="Query to format the output"
    ),
    output: Optional[OutputMode] = typer.Option(
        OutputMode.json, "--output", "-o", help="Output mode", case_sensitive=True
    ),
    colored: Optional[bool] = typer.Option(
        True, "--no-color", "-nc", help="Output with highlights."
    ),
):
    """Invoke rds describe-db-instances"""
    rds = RDSInstanceConnectWrapper.with_client(
        "rds", ctx.obj.session, filters=filters, query=query
    )
    db_instances = rds.describe_db_instances()
    ctx.obj.tui.pretty_print(db_instances, output, colored)
