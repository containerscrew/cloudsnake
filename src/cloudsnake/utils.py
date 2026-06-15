import configparser
import functools
import inspect
import webbrowser

import typer

from cloudsnake.console import console
from cloudsnake.sdk.session import SessionWrapper


def open_browser_url(url: str) -> str | None:
    """Open a URL in the default web browser."""
    try:
        webbrowser.open(url)
    except Exception as e:
        return f"Failed to open browser: {str(e)}. Open the URL manually {url}"


def parse_key_val_list(values: list[str] | None) -> dict[str, str]:
    parsed: dict[str, str] = {}
    if not values:
        return parsed

    for item in values:
        for part in item.split(","):
            if "=" not in part:
                raise ValueError(
                    f"Invalid override format '{part}', expected key=value"
                )
            key, value = part.split("=", 1)
            parsed[key] = value

    return parsed


def write_config_file(
    path: str,
    credentials: list[dict],
    region: str,
    account_overrides: dict[str, str],
    role_overrides: dict[str, str],
) -> None:
    """Write content to a configuration file."""
    config = configparser.ConfigParser()

    for cred in credentials:
        account_name = cred["AccountName"].replace(" ", "")
        role_name = cred["RoleName"]

        account_part = account_overrides.get(account_name, account_name)

        override_val = role_overrides.get(role_name)
        if override_val is not None and override_val == "":
            profile_name = account_part
        elif override_val is not None:
            profile_name = override_val
        else:
            profile_name = f"{account_part}@{role_name}"

        config[profile_name] = {
            "aws_access_key_id": cred["Credentials"]["AccessKeyId"],
            "aws_secret_access_key": cred["Credentials"]["SecretAccessKey"],
            "aws_session_token": cred["Credentials"]["SessionToken"],
            "region": region,
        }

    with open(path, "w") as config_file:
        config.write(config_file)


def signal_handler(sig, frame):
    console.print("[bold red]You pressed Ctrl+C! Exiting gracefully...[/bold red]")
    raise typer.Exit(1)


def apply_context_overrides(
    ctx: typer.Context,
    region: str | None,
    profile: str | None,
) -> None:
    """Override region/profile on the shared context set by the root callback."""
    if ctx.obj and (region or profile):
        new_region = region or ctx.obj.region
        new_profile = profile or ctx.obj.profile
        ctx.obj.session = SessionWrapper(new_profile, new_region).with_local_session()
        ctx.obj.region = new_region
        ctx.obj.profile = new_profile


def with_aws_overrides(func):
    """Inject --region/-r and --profile/-p into any Typer leaf command.

    Works by rewriting __signature__ so Typer's introspection picks up the
    extra parameters without any changes to the original function body.
    """
    sig = inspect.signature(func)
    extra = [
        inspect.Parameter(
            "region",
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=typer.Option(None, "--region", "-r", help="AWS region"),
            annotation=str | None,
        ),
        inspect.Parameter(
            "profile",
            kind=inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=typer.Option(None, "--profile", "-p", help="AWS profile"),
            annotation=str | None,
        ),
    ]
    wrapper_sig = sig.replace(parameters=list(sig.parameters.values()) + extra)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        region = kwargs.pop("region", None)
        profile = kwargs.pop("profile", None)
        ctx = next(
            (a for a in args if isinstance(a, typer.Context)),
            kwargs.get("ctx"),
        )
        apply_context_overrides(ctx, region, profile)
        return func(*args, **kwargs)

    wrapper.__signature__ = wrapper_sig
    return wrapper
