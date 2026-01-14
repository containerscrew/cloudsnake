from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, OptionList, Input, Label
from textual.widgets.option_list import Option
from textual.containers import Vertical
from rich.text import Text


# TODO: Normalize this with other TUI apps in Cloudsnake
class InstanceSelectorApp(App[str]):
    TITLE = "AWS EC2 Manager CLI"
    CSS_PATH = "styles/tui.tcss"
    BINDINGS = [
        ("ctrl+q", "hint_quit", "Quit hint"),
        ("ctrl+c", "quit", "Quit"),
        ("escape", "quit", "Cancel"),
    ]

    def __init__(self, instances: list[dict], profile: str):
        super().__init__()
        self.all_instances = instances
        self.profile = profile

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="main-container"):
            yield Label(
                f"🚀 Instance Selector - {self.profile}",
                classes="main-title",
            )
            yield Input(
                placeholder="🐍 Type to filter by name or ID...",
                id="search-box",
            )
            yield OptionList(id="instance-list")

        yield Footer()

    def on_mount(self) -> None:
        self.update_option_list(self.all_instances)
        self.query_one("#search-box").focus()

    def create_rich_option(self, item: dict) -> Option:
        text = Text.assemble(
            (item["Name"], "bold #a78bfa"),
            " ",
            (f"({item['TargetId']})", "#94a3b8"),
        )
        return Option(text, id=item["TargetId"])

    def update_option_list(self, items_to_show: list[dict]) -> None:
        option_list = self.query_one("#instance-list", OptionList)
        option_list.clear_options()
        option_list.add_options(
            [self.create_rich_option(item) for item in items_to_show]
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        search_term = event.value.lower()

        if not search_term:
            filtered = self.all_instances
        else:
            filtered = [
                item
                for item in self.all_instances
                if search_term in item["Name"].lower()
                or search_term in item["TargetId"].lower()
            ]

        self.update_option_list(filtered)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.exit(event.option_id)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        option_list = self.query_one("#instance-list", OptionList)
        if option_list.option_count > 0:
            option_list.focus()

    def action_hint_quit(self) -> None:
        self.notify(
            "Use Ctrl+C to exit",
            title="Quit disabled",
            severity="warning",
            timeout=2.5,
        )
