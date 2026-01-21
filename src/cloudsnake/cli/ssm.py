import signal
from typing import Optional

from cloudsnake.console import console
from cloudsnake.helpers import ec2_targets_to_items, ssm_parameters_to_items
from cloudsnake.sdk.ssm_parameters import SSMParameterStoreWrapper
import typer

from cloudsnake.sdk.ec2 import EC2InstanceWrapper
from cloudsnake.sdk.ssm_session import SSMStartSessionWrapper
from cloudsnake.tui_v2 import SelectorApp
from cloudsnake.utils import signal_handler

EC2_RUNNING_FILTER = "Name=instance-state-name,Values=running"
EC2_INSTANCE_SELECTOR_QUERY = "[].{TargetId: InstanceId, Name: Tags[?Key=='Name'].Value | [0], Ip: PrivateIpAddress}"

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
    signal.signal(signal.SIGINT, signal_handler)
    ssm_wrapper = SSMStartSessionWrapper(
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

        # Fake data for testing
        # instances = [
        #     {"TargetId": "i-003a434fb9c00f0f8", "Name": "WebServer-01", "Ip": "10.100.0.2"},
        #     {"TargetId": "i-0c7cca12079e449a5", "Name": "eks-instance-nodegroup-apps", "Ip": "10.100.0.3"},
        #     {"TargetId": "i-06ad6856a7ca778c6", "Name": "Database-Primary", "Ip": "10.100.0.4"},
        #     {"TargetId": "i-050ed4067698e7d26", "Name": "Cache-Server-01", "Ip": "10.100.0.5"},
        # ]

        instances = ec2.describe_ec2_instances()

        if not instances:
            console.print("[bold yellow]~> No running instances found[/bold yellow]")
            raise typer.Exit(1)

        items = ec2_targets_to_items(instances)

        app = SelectorApp(
            items=items,
            title=f"🚀 EC2 Instances — {ctx.obj.profile}",
            placeholder="Type to filter by name or ID...",
        )

        result_id = app.run()

        if result_id:
            selected = next(item for item in instances if item["TargetId"] == result_id)
            instance_id = selected["TargetId"]
            return ssm_wrapper.start_session(instance_id, reason)
        else:
            console.print("[bold yellow]~> No instance selected[/bold yellow]")
            raise typer.Exit(1)

    return ssm_wrapper.start_session(target, reason)


@ssm.command("get-parameters", help="Get secrets from parameter store")
def get_parameters(
    ctx: typer.Context,
):
    signal.signal(signal.SIGINT, signal_handler)
    ssm_wrapper = SSMParameterStoreWrapper(
        session=ctx.obj.session,
        profile=ctx.obj.profile,
        region=ctx.obj.region,
    )

    parameters = ssm_wrapper.describe_parameters()

    # fake_parameters= [
    #     {"Name": "/myapp/db_password", "Type": "SecureString"},
    #     {"Name": "/myapp/db_endpoint", "Type": "SecureString"},
    #     {"Name": "/myapp/redis_password", "Type": "SecureString"},
    #     {"Name": "/myapp/google_oauth", "Type": "SecureString"},
    # ]

    items = ssm_parameters_to_items(parameters)

    if not parameters:
        console.print("[bold yellow]~> No parameters found[/bold yellow]")
        raise typer.Exit(1)

    app = SelectorApp(
        items=items,
        title=f"🚀 SSM Parameter — {ctx.obj.profile}",
        placeholder="Type to filter by name ...",
    )

    result_id = app.run()
    parameter = ssm_wrapper.get_parameter_by_name(result_id)
    console.print(f"[bold green]~> {parameter}[/bold green]")
