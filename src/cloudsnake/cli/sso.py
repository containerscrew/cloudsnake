import signal
import sys
from typing import Optional, List

import typer

from cloudsnake.sdk.sso import SSOWrapper
from cloudsnake.sdk.sso_oidc import SSOOIDCWrapper
from cloudsnake.utils import open_browser_url


def signal_handler(sig, frame):
    typer.secho("You pressed Ctrl+C! Exiting gracefully...", fg="bright_red")
    sys.exit(0)


sso = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@sso.command("get-credentials", help="Get SSO credentials", no_args_is_help=True)
def get_credentials(
    ctx: typer.Context,
    start_url: str = typer.Option(..., help="SSO Start URL"),
    role_override: Optional[List[str]] = typer.Option(
        None,
        "--role-override",
        "-ro",
        help="Override the role name to filter",
    ),
    account_override: Optional[List[str]] = typer.Option(
        None,
        "--account-override",
        "-ao",
        help="Override the account id to filter",
    ),
):
    signal.signal(signal.SIGINT, signal_handler)
    sso_oidc = SSOOIDCWrapper(
        session=ctx.obj.session,
        profile=ctx.obj.profile,
        region=ctx.obj.region,
    )
    device_registration = sso_oidc.register_device_code("cloudsnake", "public")
    device_auth = sso_oidc.create_device_code(
        device_registration.client_id, device_registration.client_secret, start_url
    )

    open_browser_url(device_auth.verification_uri_complete)

    input("Press Enter after you have authorized the device...")

    token = sso_oidc.create_token(
        device_registration.client_id,
        device_registration.client_secret,
        device_auth.device_code,
        "urn:ietf:params:oauth:grant-type:device_code",
    )

    sso = SSOWrapper(
        session=ctx.obj.session,
        profile=ctx.obj.profile,
        region=ctx.obj.region,
    )

    sso.list_accounts(token)

    typer.echo("sso get-credentials is not yet implemented")
