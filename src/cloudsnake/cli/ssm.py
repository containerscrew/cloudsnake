from typing import Optional
import typer

from cloudsnake.sdk.ec2 import EC2InstanceWrapper
from cloudsnake.sdk.ssm_session import SSMStartSessionWrapper

EC2_RUNNING_FILTER = "Name=instance-state-name,Values=running"

EC2_INSTANCE_SELECTOR_QUERY = "[].{TargetId: InstanceId, Name: Tags[?Key=='Name'].Value | [0]}"

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
    ssm = SSMStartSessionWrapper(
        session=ctx.obj.session,
        profile=ctx.obj.profile,
        region=ctx.obj.region,
    )

    if with_instance_selector:
        ec2 = EC2InstanceWrapper(
            session=ctx.obj.session,
            filters=EC2_RUNNING_FILTER,
            query=EC2_INSTANCE_SELECTOR_QUERY,
            profile=ctx.obj.profile,
            region=ctx.obj.region,
        )

        instances = ec2.describe_ec2_instances()
        if not instances:
            typer.echo("No running instances found.")
            raise typer.Exit(1)

        instance_name = ctx.obj.tui.interactive_menu(
            instances, title="Select the EC2 you want to connect"
        )
        instance_id = ctx.obj.tui.get_target_id_by_name(instances, instance_name)

        return ssm.start_session(instance_id)

    return ssm.start_session(target)


# @ssm.command("get-parameters", help="Get parameters from parameter store")
# def get_parameters(
#     ctx: typer.Context,
#     output: Optional[OutputMode] = typer.Option(
#         OutputMode.json, "--output", "-o", help="Output mode", case_sensitive=True
#     ),
#     colored: Optional[bool] = typer.Option(
#         True, "--no-color", "-nc", help="Output with highlights."
#     ),
# ):
#     ssm = SSMParameterStoreWrapper()
#     ssm.create_client
#     ssm.describe_parameters()
#     ssm.print_parameters(output, colored)
