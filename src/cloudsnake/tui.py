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
                        rows = []
                        for key, value in obj.items():
                            rows.append(value)
                            # print(key, value)
                        table.add_row(*rows, style=random.choice(table_row_colors))

        self.console.print(table)
