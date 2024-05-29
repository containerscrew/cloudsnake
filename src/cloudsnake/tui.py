import random

from rich.console import Console
from rich.pretty import pprint
from rich.table import Table

table_row_colors = ["cyan", "magenta", "red"]

# Pending to add to helpers
def get_table_column_keys(data) -> list[str]:
    if data and isinstance(data[0], list) and data[0] and isinstance(data[0][0], dict):
        keys = list(data[0][0].keys())
        return keys
    else:
        raise TypeError("Invalid json")


class Tui:
    def __init__(self, console: Console = Console()):
        self.console = console

    @staticmethod
    def pprint(data):
        pprint(data, expand_all=True)

    def print_table(self, data):
        table = Table(title="EC2 information")
        keys = get_table_column_keys(data)
        for key in keys:
            table.add_column(key)
        # Now, add rows
        for sublist in data:
            if isinstance(sublist, list):
                for obj in sublist:
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            print(key, value)
                            # table.add_row(value, style=random.choice(table_row_colors))

        self.console.print(table)

# Rich output table
# console = Console()
# table = Table(title="EC2 selected instance information")
# table.add_column("Instance name", style="cyan")
# table.add_column("Instance id", style="magenta")
# table.add_column("Instance type", style="magenta")
# table.add_column("VPC id", style="magenta")
# table.add_column("Private ip address", style="red")
# table.add_column("Platform details", style="magenta")


# def ec2_list_selector(
#     entries: list[InstanceData], title: str = "EC2 instance selector"
# ):
#     # instance_entries = []
#     #
#     # for instance in entries:
#     #     instance_entries.append(instance.name)
#     #
#     # terminal_menu = TerminalMenu(
#     #     instance_entries,
#     #     title=title,
#     #     menu_cursor="> ",
#     #     menu_cursor_style=("fg_red", "bold"),
#     #     menu_highlight_style=("fg_black", "bg_yellow", "bold"),
#     #     cycle_cursor=True,
#     #     clear_screen=True,
#     # )
#     #
#     # menu_entry_index = terminal_menu.show()
#     # selected_instance = entries[menu_entry_index]
#
#     for instance in track(entries, description="Fetching EC2 data"):
#         table.add_row(
#             instance.name,
#             instance.instance_id,
#             instance.instance_type,
#             instance.vpc_id,
#             instance.private_ip_address,
#             instance.platform_details,
#         )
#     console.print(table)
#     # return entries[menu_entry_index].instance_id
