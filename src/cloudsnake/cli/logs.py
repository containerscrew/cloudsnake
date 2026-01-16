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
def start_session(
    ctx: typer.Context,
    filter_pattern: str = typer.Option(
        None,
        "--filter-pattern",
        "-f",
        help="Filter pattern for log events",
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
    app = SelectorApp(
        items=items,
        title=f"🚀 AWS Cloudwatch log groups — {ctx.obj.profile}",
        placeholder="Type to filter log groups...",
    )
    selected_log_group = app.run()

    if selected_log_group:
        log_group_arn = next(
            g["arn"] for g in log_groups if g["logGroupName"] == selected_log_group
        )
        typer.secho(
            f"~> Starting live tail for log group: {selected_log_group}",
            fg="bright_green",
        )
        try:
            for event in cw.tail_log_group_live(
                log_group_arn=normalize_log_group_arn_for_live_tail(log_group_arn),
                filter_pattern=filter_pattern,
            ):
                print_colored_log(event, highlight_term=filter_pattern)
        except KeyboardInterrupt:
            typer.secho("\nStopped.", fg="bright_yellow")
    else:
        typer.secho("~> No log group selected", fg="bright_yellow")
        raise typer.Exit(1)
    return
