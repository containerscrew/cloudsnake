from typing import Optional
import typer

from cloudsnake.sdk.ec2 import EC2InstanceWrapper
from cloudsnake.sdk.ssm import SSMStartSessionWrapper
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
    ssm_session = SSMStartSessionWrapper.from_session(ctx.obj.session, reason=reason)
    if with_instance_selector:
        filters = "Name=instance-state-name,Values=running"
        query = "Reservations[*].Instances[*].{TargetId:InstanceId,Name:Tags[?Key==`Name`]|[0].Value}"
        ec2 = EC2InstanceWrapper.from_session(
            ctx.obj.session, filters=filters, query=query
        )
        ec2.describe_ec2_instances()
        instance_name = Tui.interactive_menu(
            ec2.instances, title="Select the EC2 you want to connect"
        )
        instance_id = Tui.get_target_id_by_name(ec2.instances, instance_name)
        ssm_session.start_session(instance_id, ctx.obj.region, ctx.obj.profile)
    else:
        ssm_session.start_session(target, ctx.obj.region, ctx.obj.profile)


# @ssm.command(
#     "start-interactive-session",
#     help="Start interactive session choosing the instance id in a terminal menu",
# )
# def start_interactive_session(
#     ctx: typer.Context,
#     reason: Annotated[
#         str, typer.Option(help="Reason of the connection")
#     ] = "default-connection",
# ):
#     filters = "Name=instance-state-name,Values=running"
#     query = "Reservations[*].Instances[*].{Instance:InstanceId,Name:Tags[?Key==`Name`]|[0].Value}"
#     ec2_instances = EC2InstanceWrapper(
#         ctx.obj.session,
#         "ec2",
#         filters=filters,
#         query=query,
#     )
#     ec2_instances.describe_ec2_instances()
#     selected_instance = Tui.interactive_menu(ec2_instances.instances)
# ssm_session = SSMStartSessionWrapper(
#     ctx.obj.session, "ssm", target=selected_instance, reason=reason
# )
# ssm_session.start_session(ctx.obj.region, ctx.obj.profile)
