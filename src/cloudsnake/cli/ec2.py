from typing import Optional
import typer

from cloudsnake.cli.dto import OutputMode
from cloudsnake.sdk.ec2 import EC2InstanceWrapper


ec2 = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@ec2.command(
    "describe-instances",
    help="Describe EC2 instances data with filters and query as a parameter",
)
def describe_instances(
    ctx: typer.Context,
    filters: Optional[str] = typer.Option(
        None, "--filters", "-f", help="Filters for EC2 instances in Name=Value format"
    ),
    query: Optional[str] = typer.Option(
        None, "--query", "-q", help="Query to format the output"
    ),
    output: Optional[OutputMode] = typer.Option(
        OutputMode.json, "--output", "-o", help="Output mode", case_sensitive=True
    ),
    colored: Optional[bool] = typer.Option(
        True, "--no-color", "-nc", help="Output with highlights."
    ),
):
    ec2 = EC2InstanceWrapper(filters=filters, query=query)
    ec2.create_client(ctx.obj.session)
    instances = ec2.describe_ec2_instances()
    ctx.obj.tui.pretty_print(instances, output, colored)
