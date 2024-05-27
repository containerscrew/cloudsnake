from rich.progress import track
from aws_ec2 import InstanceData
from rich.console import Console
from rich.table import Table

# Rich output table
console = Console()
table = Table(title="EC2 selected instance information")
table.add_column("Instance name", style="cyan")
table.add_column("Instance id", style="magenta")
table.add_column("Instance type", style="magenta")
table.add_column("VPC id", style="magenta")
table.add_column("Private ip address", style="red")
table.add_column("Platform details", style="magenta")


def ec2_list_selector(
    entries: list[InstanceData], title: str = "EC2 instance selector"
):
    # instance_entries = []
    #
    # for instance in entries:
    #     instance_entries.append(instance.name)
    #
    # terminal_menu = TerminalMenu(
    #     instance_entries,
    #     title=title,
    #     menu_cursor="> ",
    #     menu_cursor_style=("fg_red", "bold"),
    #     menu_highlight_style=("fg_black", "bg_yellow", "bold"),
    #     cycle_cursor=True,
    #     clear_screen=True,
    # )
    #
    # menu_entry_index = terminal_menu.show()
    # selected_instance = entries[menu_entry_index]

    for instance in track(entries):
        table.add_row(
            instance.name,
            instance.instance_id,
            instance.instance_type,
            instance.vpc_id,
            instance.private_ip_address,
            instance.platform_details,
        )
    console.print(table)
    # return entries[menu_entry_index].instance_id
