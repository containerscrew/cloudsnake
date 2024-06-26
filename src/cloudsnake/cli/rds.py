from typing import Optional
import typer

from cloudsnake.sdk.rds_session import RDSInstanceConnectWrapper
from cloudsnake.tui import Tui


rds = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)

tui = Tui()


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
        tui.pretty_print(token, "text", True)


@rds.command(
    "connect",
    help="Connect to the RDS instance using a token",
)
def rds_connect(
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
    cert: str = typer.Option(..., "--cert", "-c", help="Path to the certificate"),
):
    """Invoke generate-db-auth-token command to obtain the token"""
    rds = RDSInstanceConnectWrapper.with_client(
        "rds",
        ctx.obj.session,
        hostname=hostname,
        port=port,
        db_username=username,
        region=ctx.obj.region,
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
        "cert.pem", "--save-path", "-sp", help="Path to save the certificate"
    ),
):
    """Invoke RDS download-cert"""
    rds = RDSInstanceConnectWrapper.with_client(
        "rds", ctx.obj.session, region=ctx.obj.region
    )
    rds.download_cert(save_path)
