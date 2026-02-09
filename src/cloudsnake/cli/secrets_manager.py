import signal

import typer

from cloudsnake.cli.dto import PasswordOptions
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


@secrets_manager.command(
    "generate-password",
    help="Generate a random password. Visit official documentation https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_random_password.html for more details.",
)
@handle_aws_errors
def generate_password(
    ctx: typer.Context,
    password_length: int = typer.Option(
        20,
        help="The length of the generated password.",
    ),
    exclude_characters: str = typer.Option(
        "",
        help="Characters to exclude from the generated password.",
    ),
    exclude_numbers: bool = typer.Option(
        False,
        help="Whether to exclude numbers from the generated password.",
    ),
    exclude_punctuation: bool = typer.Option(
        False,
        help="Whether to exclude punctuation from the generated password.",
    ),
    exclude_uppercase: bool = typer.Option(
        False,
        help="Whether to exclude uppercase letters from the generated password.",
    ),
    exclude_lowercase: bool = typer.Option(
        False,
        help="Whether to exclude lowercase letters from the generated password.",
    ),
    include_space: bool = typer.Option(
        False,
        help="Whether to include space in the generated password.",
    ),
    require_each_included_type: bool = typer.Option(
        True,
        help="Whether to require each included type in the generated password.",
    ),
):
    secrets_manager_wrapper = SecretsManagerWrapper(
        session=ctx.obj.session,
        profile=ctx.obj.profile,
        region=ctx.obj.region,
    )

    options = PasswordOptions(
        password_length=password_length,
        exclude_characters=exclude_characters,
        exclude_numbers=exclude_numbers,
        exclude_punctuation=exclude_punctuation,
        exclude_uppercase=exclude_uppercase,
        exclude_lowercase=exclude_lowercase,
        include_space=include_space,
        require_each_included_type=require_each_included_type,
    )

    password = secrets_manager_wrapper.generate_random_password(options)
    console.print(f"[bold green]~> {password}[/bold green]")
