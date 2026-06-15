import signal

import typer

from cloudsnake.console import console
from cloudsnake.decorators import handle_aws_errors
from cloudsnake.helpers import (
    log_groups_to_items,
    normalize_log_group_arn_for_live_tail,
)
from cloudsnake.sdk.cloudwatch import CloudWatchLogsWrapper, print_colored_log
from cloudsnake.tui import SelectorApp
from cloudsnake.utils import apply_context_overrides, signal_handler, with_aws_overrides

DEFAULT_LOG_FILTER = "[].{logGroupName: logGroupName, size: storedBytes, arn: arn}"

cw_logs = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@cw_logs.callback()
def logs_callback(
    ctx: typer.Context,
    region: str | None = typer.Option(None, "--region", "-r", help="AWS region"),
    profile: str | None = typer.Option(None, "--profile", "-p", help="AWS profile"),
) -> None:
    apply_context_overrides(ctx, region, profile)


@cw_logs.command(
    "stream", help="Live stream logs from a CloudWatch log group", no_args_is_help=False
)
@handle_aws_errors
@with_aws_overrides
def log_stream(
    ctx: typer.Context,
    filter_pattern: str = typer.Option(
        None,
        "--filter-pattern",
        "-f",
        help="Filter pattern for log events",
    ),
    since: str = typer.Option(
        None,
        "--since",
        "-s",
        help="Start time for historical logs (e.g., '1h', '2d', '30m').",
    ),
    end: str = typer.Option(
        None,
        "--end",
        "-e",
        help="End time for historical logs. If provided, live tail is skipped.",
    ),
    log_group: str = typer.Option(
        None,
        "--log-group",
        "-l",
        help="Specify the log group name directly, skipping the selector.",
    ),
):
    signal.signal(signal.SIGINT, signal_handler)

    cw = CloudWatchLogsWrapper(
        session=ctx.obj.session,
        profile=ctx.obj.profile,
        region=ctx.obj.region,
        query=DEFAULT_LOG_FILTER,
    )
    log_groups = cw.list_log_groups()
    items = log_groups_to_items(log_groups)
    selected_log_group = log_group
    if not log_group:
        app = SelectorApp(
            items=items,
            title=f"🚀 AWS Cloudwatch log groups — {ctx.obj.profile}",
            placeholder="Type to filter log groups...",
        )
        selected_log_group = app.run()

    if selected_log_group:
        console.print(
            f"[bold green]~> Preparing to stream logs from {selected_log_group}...[/bold green]"
        )
        log_group_arn = next(
            g["arn"] for g in log_groups if g["logGroupName"] == selected_log_group
        )

        live_tail_arn = normalize_log_group_arn_for_live_tail(log_group_arn)

        try:
            if since:
                console.print(
                    f"[bold cyan]~> Fetching historical logs since {since}[/bold cyan]"
                )
                for event in cw.get_historical_logs(
                    log_group_arn=log_group_arn,
                    since=since,
                    end=end,
                    filter_pattern=filter_pattern,
                ):
                    print_colored_log(event, highlight_term=filter_pattern)

            if not end:
                console.print("[bold cyan]~> Starting live tail")
                for event in cw.tail_log_group_live(
                    log_group_arn=live_tail_arn,
                    filter_pattern=filter_pattern,
                ):
                    print_colored_log(event, highlight_term=filter_pattern)
            else:
                console.print("[yellow]~> Historical search finished.[/yellow]")

        except KeyboardInterrupt:
            console.print("[bold red]~> Exiting live log stream...[/bold red]")
    else:
        console.print("[bold yellow]~> No log group selected[/bold yellow]")
        raise typer.Exit(1)
    return
