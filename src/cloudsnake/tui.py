import json
import random

from rich.console import Console
from rich.table import Table

from cloudsnake.helpers import serialize_datetime, get_table_column_keys


class Tui:
    def __init__(self, output: str = "json"):
        """
        Create your own terminal user interface using Rich library
        About used colors: https://rich.readthedocs.io/en/stable/appendix/colors.html
        :param output:
        """
        self.console = Console()
        self.output = output
        # Get colors from https://rich.readthedocs.io/en/stable/appendix/colors.html

    def pretty_print(self, data):
        match self.output:
            case "json":
                self.print_json(data)
            case "table":
                # self.print_table(data)
                self.console.print(
                    "Table output mode not implemented yet! Executing json output by default!"
                )
                self.print_json(data)
            case _:
                self.print_json(data)

    def print_json(self, data) -> None:
        json_data = json.dumps(data, default=serialize_datetime)
        self.console.print_json(json_data, highlight=True, indent=2)

    def print_table(self, data) -> None:
        table = Table(title="EC2 information")
        keys = get_table_column_keys(data)
        for key in keys:
            table.add_column(key, justify="center")
        # Now, add rows
        for sublist in data:
            if isinstance(sublist, list):
                for obj in sublist:
                    if isinstance(obj, dict):
                        rows = []
                        for key, value in obj.items():
                            rows.append(value)
                        table.add_row(*rows, style=f"color({random.randint(0, 255)})")

        self.console.print(table)
