import signal
import sys
import typer

from cloudsnake.helpers import (
    log_groups_to_items,
    normalize_log_group_arn_for_live_tail,
)
from cloudsnake.sdk.cloudwatch import CloudWatchLogsWrapper, print_colored_log
from cloudsnake.tui_v2 import SelectorApp

DEFAULT_LOG_FILTER = "[].{logGroupName: logGroupName, size: storedBytes, arn: arn}"


def signal_handler(sig, frame):
    typer.secho("You pressed Ctrl+C! Exiting gracefully...", fg="bright_red")
    sys.exit(0)


cw_logs = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@cw_logs.command(
    "stream", help="Live stream logs from a CloudWatch log group", no_args_is_help=False
)
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
        typer.secho(f"~> Selected log group: {selected_log_group}", fg="green")
        log_group_arn = next(
            g["arn"] for g in log_groups if g["logGroupName"] == selected_log_group
        )

        live_tail_arn = normalize_log_group_arn_for_live_tail(log_group_arn)

        try:
            if since:
                typer.secho(f"~> Fetching historical logs since {since}...", fg="cyan")
                for event in cw.get_historical_logs(
                    log_group_arn=log_group_arn,
                    since=since,
                    end=end,
                    filter_pattern=filter_pattern,
                ):
                    print_colored_log(event, highlight_term=filter_pattern)

            if not end:
                typer.secho(
                    "~> Starting live tail",
                    fg="cyan",
                )
                for event in cw.tail_log_group_live(
                    log_group_arn=live_tail_arn,
                    filter_pattern=filter_pattern,
                ):
                    print_colored_log(event, highlight_term=filter_pattern)
            else:
                typer.secho("~> Historical search finished.", fg="bright_yellow")

        except KeyboardInterrupt:
            typer.secho("\nStopped.", fg="bright_yellow")
    else:
        typer.secho("~> No log group selected", fg="bright_yellow")
        raise typer.Exit(1)
    return
