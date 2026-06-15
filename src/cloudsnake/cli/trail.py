import json
from datetime import datetime
from typing import Any

import jq
import typer

from cloudsnake.cli.dto import OutputMode
from cloudsnake.console import console
from cloudsnake.decorators import handle_aws_errors
from cloudsnake.sdk.cloudtrail import CloudTrailWrapper
from cloudsnake.utils import apply_context_overrides, with_aws_overrides

trail = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@trail.callback()
def trail_callback(
    ctx: typer.Context,
    region: str | None = typer.Option(None, "--region", "-r", help="AWS region"),
    profile: str | None = typer.Option(None, "--profile", "-p", help="AWS profile"),
) -> None:
    apply_context_overrides(ctx, region, profile)


@trail.command("events")
@handle_aws_errors
@with_aws_overrides
def trail_events(
    ctx: typer.Context,
    user: str = typer.Option(None, "--user", "-u"),
    event_name: str = typer.Option(None, "--event", "-e"),
    resource_name: str = typer.Option(None, "--resource"),
    read_only: bool | None = typer.Option(None, "--read-only/--write-only"),
    since: str = typer.Option("15m", "--since", "-s"),
    search: str = typer.Option(None, "--search", "-q"),
    output: OutputMode | None = typer.Option(
        OutputMode.pretty,
        "--output",
        "-o",
        help="Output format: pretty | json | ndjson",
    ),
    jq_expr: str = typer.Option(
        None,
        "--jq",
        help="Apply jq expression to event JSON",
    ),
    once: bool = typer.Option(False, "--once"),
):
    """
    Monitor CloudTrail events.
    """

    if jq_expr and output not in ("json", "ndjson"):
        console.print("[bold red]Error:[/] --jq requires --output json or ndjson.")
        raise typer.Exit(1)

    ct = CloudTrailWrapper(
        session=ctx.obj.session,
        profile=ctx.obj.profile,
        region=ctx.obj.region,
    )

    filters = {
        "Username": user,
        "EventName": event_name,
        "ResourceName": resource_name,
    }

    if read_only is not None:
        filters["ReadOnly"] = "true" if read_only else "false"

    # Keep only active filters
    active = {k: v for k, v in filters.items() if v is not None}

    if len(active) > 1:
        console.print(
            "[bold red]Error:[/] Only one AWS attribute filter allowed. One of --user, --event, --resource, --read-only/--write-only."
        )
        raise typer.Exit(1)

    lookup_attr = None
    if active:
        key, value = next(iter(active.items()))
        lookup_attr = {"AttributeKey": key, "AttributeValue": value}

    start_ts = ct._parse_time_str(since)

    # All the available spinners: https://github.com/Textualize/rich/blob/master/rich/_spinners.py
    with console.status(
        "[bold cyan]Fetching CloudTrail history since[/]",
        speed=0.1,
        spinner="aesthetic",
        spinner_style="bold cyan",
    ):
        for event in ct.tail_events(
            start_time_ms=start_ts,
            lookup_attr=lookup_attr,
            once=once,
        ):
            raw = event.get("CloudTrailEvent")
            detail = None
            if raw:
                try:
                    detail = json.loads(raw)
                except Exception:
                    pass

            if search and not match_search(detail, search):
                continue

            safe_event = json_safe(event)

            if jq_expr:
                try:
                    result = jq.compile(jq_expr).input(safe_event).all()
                    if not result:
                        continue
                    safe_event = result[0] if len(result) == 1 else result
                except Exception:
                    continue

            if output == "json":
                print(json.dumps(safe_event, indent=2))
                continue

            if output == "ndjson":
                print(json.dumps(safe_event))
                continue

            print_event(event, detail)


def json_safe(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [json_safe(v) for v in obj]
    return obj


def match_search(detail: dict | None, expr: str) -> bool:
    if not detail:
        return False

    if "=" not in expr:
        return expr.lower() in json.dumps(detail).lower()

    path, expected = expr.split("=", 1)
    value = get_by_path(detail, path)
    return value is not None and expected.lower() in str(value).lower()


def get_by_path(obj: Any, path: str) -> Any:
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        elif isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except Exception:
                return None
        else:
            return None
    return cur


def print_event(event: dict, detail: dict | None):
    event_time = event["EventTime"].strftime("%H:%M:%S")
    name = event.get("EventName", "Unknown")
    source = event.get("EventSource", "").replace(".amazonaws.com", "")
    user = event.get("Username", "Unknown")

    resource = ""
    if detail:
        resource = extract_resource_id(detail)
        extracted = extract_user_identity(detail)
        if extracted:
            user = extracted

    style = "green"
    if any(k in name for k in ("Delete", "Terminate", "Fail")):
        style = "bold red"
    elif any(k in name for k in ("Update", "Modify", "Put", "Stop", "Create", "Run")):
        style = "yellow"

    res = f" ([magenta]{resource}[/])" if resource else ""
    console.print(
        f"[{event_time}] [cyan]{source:15}[/] -> "
        f"[{style}]{name:25}[/]{res:30} by [bold blue]{user}[/]"
    )


def extract_resource_id(event: dict) -> str:
    params = event.get("requestParameters")
    if not params:
        return ""

    for key in (
        "instanceId",
        "bucketName",
        "roleName",
        "userName",
        "groupName",
        "policyArn",
        "functionName",
        "trailName",
        "dbInstanceIdentifier",
        "loadBalancerArn",
        "resourceArn",
        "id",
    ):
        val = params.get(key)
        if isinstance(val, str):
            return val

    items = params.get("instancesSet", {}).get("items", [])
    if items:
        return items[0].get("instanceId", "")

    if "bucketName" in params and "key" in params:
        return f"s3://{params['bucketName']}/{params['key']}"

    return ""


def extract_user_identity(detail: dict) -> str:
    identity = detail.get("userIdentity", {})
    t = identity.get("type")

    if "userName" in identity:
        return identity["userName"]

    if t == "AssumedRole":
        arn = identity.get("arn", "")
        parts = arn.split("/")
        return "/".join(parts[-2:]) if len(parts) >= 2 else "AssumedRole"

    if t == "AWSService":
        return identity.get("invokedBy", "AWSService")

    if t == "FederatedUser":
        issuer = identity.get("sessionContext", {}).get("sessionIssuer", {})
        return issuer.get("userName", "FederatedUser")

    return "Unknown"
