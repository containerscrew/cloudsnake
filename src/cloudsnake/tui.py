from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Footer, Header, Input, Label, OptionList
from textual.widgets.option_list import Option

from cloudsnake.models.selector import SelectorItem


class SelectorApp(App[str]):
    TITLE = "Cloudsnake Selector"
    CSS_PATH = "styles/tui.tcss"

    BINDINGS = [
        ("ctrl+q", "hint_quit", "Quit hint"),
        ("ctrl+c", "quit", "Quit"),
        ("escape", "quit", "Cancel"),
    ]

    def __init__(
        self,
        items: list[SelectorItem],
        title: str,
        placeholder: str,
    ):
        super().__init__()
        self.items = items
        self.title = title
        self.placeholder = placeholder

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Vertical(id="main-container"):
            yield Label(self.title, classes="main-title")
            yield Input(
                placeholder=self.placeholder,
                id="search-box",
            )
            yield OptionList(id="item-list")

        yield Footer()

    def on_mount(self) -> None:
        self.update_option_list(self.items)
        self.query_one("#search-box").focus()

    def create_rich_option(self, item: SelectorItem) -> Option:
        text = Text.assemble(
            (item.label, "bold #a78bfa"),
            " ",
            (f"({item.id})", "#94a3b8"),
        )

        for meta in item.meta:
            text.append(" ")
            text.append(f"[{meta}]", style="#fbbf24")

        return Option(text, id=item.id)

    def update_option_list(self, items: list[SelectorItem]) -> None:
        option_list = self.query_one("#item-list", OptionList)
        option_list.clear_options()
        option_list.add_options([self.create_rich_option(item) for item in items])

    def on_input_changed(self, event: Input.Changed) -> None:
        term = event.value.lower()

        if not term:
            filtered = self.items
        else:
            filtered = [
                item
                for item in self.items
                if term in item.label.lower()
                or term in item.id.lower()
                or any(term in m.lower() for m in item.meta)
            ]

        self.update_option_list(filtered)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self.exit(event.option_id)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        option_list = self.query_one("#item-list", OptionList)
        if option_list.option_count > 0:
            option_list.focus()

    def action_hint_quit(self) -> None:
        self.notify(
            "Use Ctrl+C to exit",
            title="Quit disabled",
            severity="warning",
            timeout=2.5,
        )
