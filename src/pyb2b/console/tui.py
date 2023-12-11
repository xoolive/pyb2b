from __future__ import annotations

import json

import httpx
from rich.json import JSON
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import VerticalScroll
from textual.widgets import (
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    Static,
    TabbedContent,
    TabPane,
    Tabs,
)

import pandas as pd
from pyb2b import b2b
from pyb2b.types.flight.management.flightplanlist import (
    FlightPlanListReply,
    _Entry,
)

# -- Formatters --


class Time:
    def __init__(self, timestamp: None | int | str | pd.Timestamp):
        self.ts = timestamp

    def __format__(self, __format_spec: str) -> str:
        if self.ts is None:
            return ""
        if isinstance(self.ts, int):
            ts = pd.Timestamp(self.ts, unit="s", tz="utc")
        else:
            ts = pd.Timestamp(self.ts, tz="utc")
        return format(ts, __format_spec)


# -- Widgets --


class SearchBlock(Static):
    def compose(self) -> ComposeResult:
        yield SearchButton(id="date")
        yield SearchButton(id="callsign")
        yield SearchButton(id="origin")
        yield SearchButton(id="destination")
        yield SearchButton(id="airspace")
        yield SearchButton(id="regulation")


class SearchButton(Static):
    def compose(self) -> ComposeResult:
        assert self.id is not None
        yield Label(self.id)
        yield Input(id=f"input_{self.id}")

    def on_mount(self) -> None:
        input = self.query(Input).first()
        if input.id == "input_date":
            input.value = f"{pd.Timestamp('now'):%d %b %y}"
        if input.id == "input_callsign":
            input.focus()

    # async def on_input_submitted(self, message: Input.Submitted) -> None:
    #     await self.app.lookup_flightplanlist()
    #     return
    #     ts_widget = next(
    #         input for input in self.app.query(Input) if input.id == "date"
    #     )
    #     ts = pd.Timestamp(
    #         ts_widget.value if ts_widget.value != "" else "now",
    #         tz="utc",
    #     )

    #     if message.value:
    #         if message.input.id == "aircraft":
    #             await self.app.lookup_aircraft(message.value, ts=ts)  # type: ignore
    #         if message.input.id == "flight number":
    #             await self.app.lookup_number(message.value, ts=ts)  # type: ignore
    #         if message.input.id == "origin":
    #             await self.app.lookup_departure(message.value, ts=ts)  # type: ignore
    #         if message.input.id == "destination":
    #             await self.app.lookup_arrival(message.value, ts=ts)  # type: ignore


# -- Application --


class B2B(App[None]):
    CSS_PATH = "style.tcss"
    BINDINGS = [  # noqa: RUF012
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),  # TODO
        ("s", "search", "Search"),
        Binding("escape", "escape", show=False),
        Binding("d", "show_debug", "Debug"),
    ]

    def compose(self) -> ComposeResult:
        self.client = httpx.AsyncClient(verify=b2b.context)
        self.search_visible = True
        yield Header()
        yield Footer()
        with TabbedContent():
            with TabPane("B2B", id="result-pane"):
                yield SearchBlock()
                yield VerticalScroll(DataTable())
            with TabPane("Debug", id="debug-pane"):
                yield VerticalScroll(
                    Static(id="results"), id="results-container"
                )

    def on_mount(self) -> None:
        self.title = "EUROCONTROL B2B"
        table = self.query_one(DataTable)
        table.add_columns(
            "date", "callsign", "from", "to", "EOBT", "flightid", "status"
        )
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.hide_tab("debug-pane")
        self.query_one(Tabs).add_class("hidden")

    def action_search(self) -> None:
        self.search_visible = not self.search_visible
        if self.search_visible:
            self.query_one(SearchBlock).remove_class("hidden")
        else:
            self.query_one(SearchBlock).add_class("hidden")
            self.query_one(DataTable).focus()

    async def action_escape(self) -> None:
        if not self.search_visible:
            await self.action_quit()

        self.search_visible = False
        self.query_one(SearchBlock).add_class("hidden")
        self.query_one(DataTable).focus()

    def action_show_debug(self) -> None:
        self.query_one(Tabs).remove_class("hidden")
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.show_tab("debug-pane")
        tabbed_content.active = "debug-pane"

    # @on(DataTable.CellSelected)
    # async def on_selected(self) -> None:
    #     table = self.query_one(DataTable)
    #     cursor = table.cursor_coordinate
    #     day, callsign, origin, destination, eobt, fid, _ = table.get_row_at(
    #         cursor.row
    #     )
    #     start = pd.Timestamp(f"{day} {eobt[:-1]}")
    #     stop = start + pd.Timedelta("1H")
    #     results = await b2b.async_flightplanlist(
    #         self.client,
    #         start,
    #         stop,
    #         callsign=callsign,
    #         origin=origin,
    #         destination=destination,
    #     )
    #     self.query_one("#results", Static).update(JSON(json.dumps(results)))

    @on(Input.Submitted)
    async def lookup_flightplanlist(self) -> None:
        date = self.query_one("#input_date", Input)
        start_str = date.value if date.value else "now"
        start = pd.Timestamp(start_str)
        stop = start + pd.Timedelta("1 day")
        callsign_value = self.query_one("#input_callsign", Input).value
        callsign = callsign_value if callsign_value else "*"
        origin_value = self.query_one("#input_origin", Input).value
        origin = origin_value if origin_value else "*"
        destination_value = self.query_one("#input_destination", Input).value
        destination = destination_value if destination_value else "*"
        results = await b2b.async_flightplanlist(
            self.client,
            start,
            stop,
            callsign=callsign,
            origin=origin,
            destination=destination,
        )
        self.query_one("#results", Static).update(JSON(json.dumps(results)))
        self.update_table(results)

    def update_table(self, data: None | FlightPlanListReply) -> None:
        table = self.query_one(DataTable)

        table.clear(columns=True)
        table.add_columns(
            "date", "callsign", "from", "to", "EOBT", "flightid", "status"
        )

        if data is None:
            return

        def eobt(entry: _Entry) -> str:
            if lfvp := entry.get("lastValidFlightPlan", None):
                return lfvp["id"]["keys"]["estimatedOffBlockTime"]
            return ""

        summaries = sorted(
            data["fl:FlightPlanListReply"]["data"]["summaries"],
            key=eobt,
        )
        table.add_rows(
            (
                (
                    f"{Time(eobt(entry)):%d %b %y}",
                    lvfp["id"]["keys"]["aircraftId"],
                    lvfp["id"]["keys"]["aerodromeOfDeparture"],
                    lvfp["id"]["keys"]["aerodromeOfDestination"],
                    f"{Time(eobt(entry)):%H:%MZ}",
                    lvfp["id"]["id"],
                    lvfp["status"],
                )
                for entry in summaries
                if (lvfp := entry.get("lastValidFlightPlan", None))
            ),
        )


def main() -> None:
    app = B2B()
    app.run()


if __name__ == "__main__":
    main()
