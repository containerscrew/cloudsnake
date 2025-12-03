from rich.console import Console
from simple_term_menu import TerminalMenu

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


class SSMTui:
    def __init__(self):
        """
        Create your own terminal user interface using Rich library
        About used colors: https://rich.readthedocs.io/en/stable/appendix/colors.html
        :param output:
        """
        self.console = Console()
        self.color_list = list(colors_hex.values())

        # Get colors from https://rich.readthedocs.io/en/stable/appendix/colors.html

    @staticmethod
    def get_parameter_by_name(data):
        return [f"{item['Name']}" for item in data]

    @staticmethod
    def interactive_menu(data, title="Select parameter store parameter"):
        parameters = SSMTui.get_parameter_by_name(data)

        terminal_menu = TerminalMenu(
            parameters,
            title=title,
            menu_cursor="> ",
            menu_cursor_style=("fg_red", "bold"),
            menu_highlight_style=("fg_black", "bg_yellow", "bold"),
            cycle_cursor=True,
            clear_screen=True,
        )

        idx = terminal_menu.show()

        return parameters[idx]


class EC2Tui:
    def __init__(self):
        """
        Create your own terminal user interface using Rich library
        About used colors: https://rich.readthedocs.io/en/stable/appendix/colors.html
        :param output:
        """
        self.console = Console()
        self.color_list = list(colors_hex.values())

        # Get colors from https://rich.readthedocs.io/en/stable/appendix/colors.html

    @staticmethod
    def get_instance_names(data):
        return [f"{item['Name']}  ({item['TargetId']})" for item in data]

    @staticmethod
    def get_target_id_by_name(data, selection):
        name, _, iid = selection.rpartition(" (")
        iid = iid.rstrip(")")
        return iid

    @staticmethod
    def interactive_menu(data, title="Select instance"):
        instance_names = EC2Tui.get_instance_names(data)

        terminal_menu = TerminalMenu(
            instance_names,
            title=title,
            menu_cursor="> ",
            menu_cursor_style=("fg_red", "bold"),
            menu_highlight_style=("fg_black", "bg_yellow", "bold"),
            cycle_cursor=True,
            clear_screen=True,
        )
        idx = terminal_menu.show()

        return instance_names[idx]
