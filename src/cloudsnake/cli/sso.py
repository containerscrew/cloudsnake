import typer

from cloudsnake.sdk.sso_oidc import SSOIDCWrapper


sso = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@sso.command(
    "fetch-sso-credentials",
    help="Fetch your AWS account credentials using SSO",
    no_args_is_help=True,
)
def fetch_sso_credentials(
    ctx: typer.Context,
    start_url: str = typer.Option(
        help="SSO start url. Example: https://XXXXXX.awsapps.com/start"
    ),
):
    oidc = SSOIDCWrapper(ctx.obj.session, "sso-oidc")
    client_id, client_secret = oidc.device_registration()
    oidc.get_auth_device(client_id, client_secret, start_url)
