import json
import random

from rich.console import Console
from rich.table import Table
from rich import print
from simple_term_menu import TerminalMenu
from cloudsnake.helpers import serialize_datetime

"""
Color list
Using rich style rgba colors from 0 to 255: style=f"color({random.randint(0, 255)})
In this case I don't want all the colors
"""
colors_hex = {
    "purple": "#800080",
    "orange": "#FFA500",
    "red": "#FF0000",
    "blue": "#0000FF",
    "green": "#008000",
}


class Tui:
    def __init__(self):
        """
        Create your own terminal user interface using Rich library
        About used colors: https://rich.readthedocs.io/en/stable/appendix/colors.html
        :param output:
        """
        self.console = Console()
        self.color_list = list(colors_hex.values())

        # Get colors from https://rich.readthedocs.io/en/stable/appendix/colors.html

    def pretty_print(self, data, output, colored):
        match output:
            case "json":
                self.print_json(data, colored)
            case "text":
                self.print_text(data, colored)
            case "table":
                self.print_table(data, colored)
            case _:
                """Default, print_json"""
                self.print_json(data)

    def print_text(self, data, colored) -> None:
        if colored:
            print(f"[bold green]{data}[/bold green]")
        else:
            print(f"{data}")

    def print_json(self, data, colored) -> None:
        json_data = json.dumps(data, default=serialize_datetime)
        self.console.print_json(json_data, highlight=colored, indent=2)

    def print_table(self, data, colored) -> None:
        """
        Convert JSON data to a Rich Table.

        :param json_data: The JSON data to convert.
        :param color: Set the output color for the table
        """
        table = Table(title="DescribeInstances", title_justify="center")
        table.add_column("Describe isntances", justify="center")
        st = Table(
            padding=(0, 0),
            show_edge=False,
            show_lines=True,
        )

        # Get keys from the first item in the JSON data
        keys = list(data[0][0].keys())

        # Add columns to the table
        for key in keys:
            st.add_column(key, justify="center")

        # Add rows to the table
        for item in data:
            for obj in item:
                if colored:
                    style = f"{random.choice(self.color_list)}"
                else:
                    style = None
                st.add_row(
                    *[str(obj.get(key, "")) for key in keys],
                    style=style,
                )

        table.add_row(st)

        self.console.print(table)

    @staticmethod
    def get_instance_names(data):
        """
        Parse the following data.
        Example:
        data = [
            [{'TargetId': 'i-0c9f0rfrfrfc', 'Name': 'runner-pnh4wbzsfrfrfrfrf'}],
            [{'TargetId': 'i-0ab123456789', 'Name': 'runner-xyz9876'}]
        ]
        """
        names = []
        for sublist in data:
            for item in sublist:
                if "Name" in item:
                    names.append(item["Name"])
        return names

    @staticmethod
    def get_target_id_by_name(data, name):
        for sublist in data:
            for item in sublist:
                if item.get("Name") == name:
                    return item.get("TargetId")
        return None

    @staticmethod
    def interactive_menu(data, title="Select your choice") -> str:
        instance_names = Tui.get_instance_names(data)
        terminal_menu = TerminalMenu(
            instance_names,
            title=title,
            menu_cursor="> ",
            menu_cursor_style=("fg_red", "bold"),
            menu_highlight_style=("fg_black", "bg_yellow", "bold"),
            cycle_cursor=True,
            clear_screen=True,
        )
        menu_entry_index = terminal_menu.show()
        return instance_names[menu_entry_index]
