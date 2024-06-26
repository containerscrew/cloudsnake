from typing import Optional
import typer

from cloudsnake.cli.dto import OutputMode
from cloudsnake.sdk.ec2 import EC2InstanceWrapper
from cloudsnake.sdk.ssm_parameter_store import SSMParameterStoreWrapper
from cloudsnake.sdk.ssm_session import SSMStartSessionWrapper
from cloudsnake.tui import Tui


ssm = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@ssm.command(
    "start-session", help="Start session with the given target id", no_args_is_help=True
)
def start_session(
    ctx: typer.Context,
    target: Optional[str] = typer.Option(None, help="Target id of the instance"),
    reason: Optional[str] = typer.Option(
        "ssm-new-connection", help="Reason of the connection"
    ),
    with_instance_selector: Optional[bool] = typer.Option(
        False,
        "--with-instance-selector",
        "-is",
        help="Prompt a terminal menu and select the instance you want to connect. --target flag is no longer used",
    ),
):
    ssm_session = SSMStartSessionWrapper.with_client(
        "ssm", ctx.obj.session, reason=reason
    )
    if with_instance_selector:
        filters = "Name=instance-state-name,Values=running"
        query = "Reservations[*].Instances[*].{TargetId:InstanceId,Name:Tags[?Key==`Name`]|[0].Value}"
        ec2 = EC2InstanceWrapper.with_client(
            "ec2", ctx.obj.session, filters=filters, query=query
        )
        ec2.describe_ec2_instances()
        instance_name = Tui.interactive_menu(
            ec2.instances, title="Select the EC2 you want to connect"
        )
        instance_id = Tui.get_target_id_by_name(ec2.instances, instance_name)
        ssm_session.start_session(instance_id, ctx.obj.region, ctx.obj.profile)
    else:
        ssm_session.start_session(target, ctx.obj.region, ctx.obj.profile)


@ssm.command("get-parameters", help="Get parameters from parameter store")
def get_parameters(
    ctx: typer.Context,
    output: Optional[OutputMode] = typer.Option(
        OutputMode.json, "--output", "-o", help="Output mode", case_sensitive=True
    ),
    colored: Optional[bool] = typer.Option(
        True, "--no-color", "-nc", help="Output with highlights."
    ),
):
    ssm = SSMParameterStoreWrapper.with_client("ssm", ctx.obj.session)
    ssm.describe_parameters()
    ssm.print_parameters(output, colored)
