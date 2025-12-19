import logging
import os
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, List

import typer
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)

from cloudsnake import utils
from cloudsnake.sdk.sso import SSOWrapper
from cloudsnake.sdk.sso_oidc import SSOOIDCWrapper
from cloudsnake.utils import open_browser_url, parse_key_val_list

AWS_CREDENTIALS_FILE_PATH = os.path.expanduser("~/.aws/credentials")

logger = logging.getLogger("cloudsnake.sso")


def signal_handler(sig, frame):
    typer.secho("\n ~> You pressed Ctrl+C! Exiting gracefully. Bye!", fg="bright_red")
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
    role_overrides: Optional[List[str]] = typer.Option(
        None,
        "--role-overrides",
        "-ro",
        help="Override the role name to filter",
    ),
    account_overrides: Optional[List[str]] = typer.Option(
        None,
        "--account-overrides",
        "-ao",
        help="Override the account id to filter",
    ),
    workers: int = typer.Option(
        4,
        "--workers",
        "-w",
        help="Number of concurrent workers to fetch credentials",
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

    typer.echo(
        typer.style(
            f"~> Press Enter after you have authorized the device in the opened browser: {device_auth.verification_uri_complete}",
            fg=typer.colors.CYAN,
            bold=True,
        ),
        nl=False,
    )

    sys.stdin.readline()

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

    accounts = sso.list_accounts(token)
    all_credentials = []
    account_list = accounts.get("accountList", [])

    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=40),
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(
            "Fetching AWS credentials",
            total=len(account_list),
        )

        with ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_account = {
                executor.submit(
                    sso.get_credentials,
                    account["accountId"],
                    account.get("accountName", ""),
                    token,
                ): account.get("accountName", "")
                for account in account_list
            }

            for future in as_completed(future_to_account):
                account_name = future_to_account[future]

                try:
                    result = future.result()
                    all_credentials.extend(result)
                    progress.update(
                        task, advance=1, description=f"[cyan]{account_name}"
                    )
                except Exception as e:
                    logger.error(f"Error fetching credentials for {account_name}: {e}")
                    progress.update(
                        task,
                        advance=1,
                        description=f"[red]ERROR {account_name}",
                    )

    role_overrides_map = parse_key_val_list(role_overrides)
    account_overrides_map = parse_key_val_list(account_overrides)
    utils.write_config_file(
        AWS_CREDENTIALS_FILE_PATH,
        all_credentials,
        ctx.obj.region,
        account_overrides_map,
        role_overrides_map,
    )
    typer.secho(
        f"~> AWS credentials have been written to {AWS_CREDENTIALS_FILE_PATH}",
        fg=typer.colors.GREEN,
        bold=True,
    )
