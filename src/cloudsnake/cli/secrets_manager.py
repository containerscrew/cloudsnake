import signal

import typer

from cloudsnake.console import console
from cloudsnake.decorators import handle_aws_errors
from cloudsnake.helpers import secrets_manager_secrets_to_items
from cloudsnake.sdk.secrets_manager import SecretsManagerWrapper
from cloudsnake.tui import SelectorApp
from cloudsnake.utils import signal_handler

secrets_manager = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@secrets_manager.command("get-secrets", help="Get secrets from Secrets Manager")
@handle_aws_errors
def get_parameters(
    ctx: typer.Context,
):
    signal.signal(signal.SIGINT, signal_handler)
    secrets_manager_wrapper = SecretsManagerWrapper(
        session=ctx.obj.session,
        profile=ctx.obj.profile,
        region=ctx.obj.region,
    )

    secrets = secrets_manager_wrapper.list_secrets()

    if not secrets:
        console.print("[bold yellow]~> No secrets found[/bold yellow]")
        raise typer.Exit(1)

    items = secrets_manager_secrets_to_items(secrets)

    app = SelectorApp(
        items=items,
        title=f"🚀 Secrets Manager — {ctx.obj.profile}",
        placeholder="Type to filter by name ...",
    )

    result_id = app.run()
    parameter = secrets_manager_wrapper.get_secret_value_by_name(result_id)
    console.print(f"[bold green]~> {parameter}[/bold green]")
