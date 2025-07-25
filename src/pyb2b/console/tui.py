from __future__ import annotations

import json
import logging
from typing import Union

import httpx
from rich.json import JSON
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.logging import TextualHandler
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
from pyb2b.services.flight.management import (
    FlightListByAerodrome,
    FlightListByAirspace,
    FlightListByMeasure,
    FlightPlanList,
    FlightRetrieval,
)
from pyb2b.services.flow.measures import RegulationList
from pyb2b.types.generated.flight import (
    FlightOrFlightPlan,
    FlightPlanOrInvalidFiling,
)

# -- Formatters --

logging.basicConfig(level="NOTSET", handlers=[TextualHandler()])


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


class Flight(VerticalScroll):
    BINDINGS = [Binding("s", "save", "Save JSON", show=True)]  # noqa: RUF012
    flight: None | FlightRetrieval = None

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield Static(id="flight_id")
            yield Static(id="callsign")
            yield Static(id="iata")
            yield Static(id="status")
        with Horizontal():
            yield Static(id="origin")
            yield Static(id="destination")
            yield Static(id="icao24")
            yield Static(id="typecode")
        with Horizontal(id="flight_times"):
            with Vertical():
                yield Static(" EOBT/COBT/AOBT ")
                yield Static(id="EOBT")
                yield Static(id="COBT")
                yield Static(id="AOBT")
            with Vertical():
                yield Static(" ETOT/CTOT/ATOT ")
                yield Static(id="ETOT")
                yield Static(id="CTOT")
                yield Static(id="ATOT")
            with Vertical():
                yield Static(" ETOA/CTOA/ATOA ")
                yield Static(id="ETOA")
                yield Static(id="CTOA")
                yield Static(id="ATOA")
        yield Static(id="icaoRoute")
        yield VerticalScroll(Static(id="regulation"), id="regulation-container")

    def action_save(self) -> None:
        if self.flight is None:
            self.notify("No data to save", severity="error")
            return
        data = self.flight.json["data"]
        if data is None:
            self.notify("No data to save", severity="error")
            return
        f_id = data["flight"]["flightId"]
        date = f_id["keys"]["estimatedOffBlockTime"]
        date = date.split(" ")[0].replace("-", "")
        origin = f_id["keys"]["aerodromeOfDeparture"]
        destination = f_id["keys"]["aerodromeOfDestination"]
        filename = f"{date}_{f_id['id']}_{origin}_{destination}.json"
        self.notify(f"File saved: {filename}", severity="information")
        self.flight.to_file(filename)

    def update_flight(
        self,
        flight_retrieval: FlightRetrieval,
        regulation: None | RegulationList,
    ) -> None:
        self.flight = flight_retrieval
        data = self.flight.json["data"]
        if data is None:
            return
        if (flight := data["flight"]) is None:
            return

        flight_id = flight["flightId"]

        self.query_one("#flight_id", Static).update(flight_id["id"])
        self.query_one("#callsign", Static).update(
            flight_id["keys"]["aircraftId"]
        )
        self.query_one("#origin", Static).update(
            flight_id["keys"]["aerodromeOfDeparture"]
        )
        self.query_one("#destination", Static).update(
            flight_id["keys"]["aerodromeOfDestination"]
        )
        self.query_one("#EOBT", Static).update(
            flight_id["keys"]["estimatedOffBlockTime"]
        )

        self.query_one("#typecode", Static).update(
            flight.get("aircraftType", "")
        )
        self.query_one("#COBT", Static).update(
            flight.get("calculatedOffBlockTime", "")
        )
        self.query_one("#AOBT", Static).update(
            flight.get("actualOffBlockTime", "")
        )
        self.query_one("#ETOT", Static).update(
            flight.get("estimatedTakeOffTime", "")
        )
        self.query_one("#CTOT", Static).update(
            flight.get("calculatedTakeOffTime", "")
        )
        self.query_one("#ATOT", Static).update(
            flight.get("actualTakeOffTime", "")
        )
        self.query_one("#ETOA", Static).update(
            flight.get("estimatedTimeOfArrival", "")
        )
        self.query_one("#CTOA", Static).update(
            flight.get("calculatedTimeOfArrival", "")
        )
        self.query_one("#ATOA", Static).update(
            flight.get("actualTimeOfArrival", "")
        )
        # deal with regulations and measures

        #
        self.query_one("#icaoRoute", Static).update(
            Text(flight.get("icaoRoute", ""))
        )
        self.query_one("#status", Static).update(flight.get("flightState", ""))
        self.query_one("#icao24", Static).update(
            flight.get("aircraftAddress", "").lower()
        )
        iata = flight.get("iataFlightDesignator", {"id": ""})
        self.query_one("#iata", Static).update(
            f"{iata if isinstance(iata, set) else iata.get('id', '')}"
        )
        if regulation is not None:
            self.query_one("#regulation", Static).update(
                JSON(json.dumps(regulation.json["data"]["regulations"]))
            )

        self.focus()  # helps activating the Binding


# -- Application --


class B2B(App[None]):
    CSS_PATH = "style.tcss"
    BINDINGS = [  # noqa: RUF012
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),  # TODO
        ("/", "search", "Search"),
        Binding("escape", "escape", show=False),
        Binding("d", "show_debug", "Debug"),
    ]

    def compose(self) -> ComposeResult:
        self.client = httpx.AsyncClient(verify=b2b.context)
        yield Header()
        yield Footer()
        with TabbedContent():
            with TabPane("B2B", id="result-pane"):
                yield SearchBlock()
                yield DataTable()
            with TabPane("Flight", id="flight-pane"):
                yield Flight()
            with TabPane("Debug", id="debug-pane"):
                yield VerticalScroll(
                    Static(id="results"), id="results-container"
                )

    def on_mount(self) -> None:
        self.title = "EUROCONTROL B2B"
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.add_columns(
            "date", "callsign", "from", "to", "EOBT", "flightid", "status"
        )
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.hide_tab("debug-pane")
        self.query_one(Tabs).add_class("hidden")

    def action_search(self) -> None:
        self.query_one(SearchBlock).focus()

    async def action_escape(self) -> None:
        if self.query_one(DataTable).has_focus:
            await self.action_quit()
        self.query_one(DataTable).focus()

    def action_show_debug(self) -> None:
        self.query_one(Tabs).remove_class("hidden")
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.show_tab("debug-pane")
        tabbed_content.active = "debug-pane"

    async def on_data_table_row_selected(
        self, event: DataTable.RowSelected
    ) -> None:
        columns = [c.label.plain for c in event.data_table.columns.values()]
        line_info = dict(zip(columns, event.data_table.get_row(event.row_key)))
        logging.info(f"Selected row {line_info}")

        result = await b2b.async_flightretrieval(
            self.client,
            pd.Timestamp(f"{line_info['date']} {line_info['EOBT']}"),
            callsign=line_info["callsign"],
            origin=line_info["from"],
            destination=line_info["to"],
        )
        await self.update_flight(result)
        self.query_one("#results", Static).update(JSON(json.dumps(result.json)))

    @on(Input.Submitted)
    async def lookup_flightplanlist(self) -> None:
        date = self.query_one("#input_date", Input)
        start_str = date.value if date.value else "now"
        start = pd.Timestamp(start_str)
        stop = start + pd.Timedelta("1 day")

        callsign = self.query_one("#input_callsign", Input).value
        origin = self.query_one("#input_origin", Input).value
        destination = self.query_one("#input_destination", Input).value
        airspace = self.query_one("#input_airspace", Input).value
        regulation = self.query_one("#input_regulation", Input).value
        results: Union[
            FlightPlanList,
            FlightListByAirspace,
            FlightListByAerodrome,
            FlightListByMeasure,
        ]

        if callsign or (origin and destination and origin != destination):
            callsign = callsign if callsign else "*"
            origin = origin if origin else "*"
            destination = destination if destination else "*"
            results = await b2b.async_flightplanlist(
                self.client,
                start=start,
                stop=stop,
                callsign=callsign,
                origin=origin,
                destination=destination,
            )
            self.update_with_flightplan(results)
        elif origin and destination:
            results = await b2b.async_flightlistbyaerodrome(
                self.client, origin, "GLOBAL", start=start, stop=stop
            )
            self.update_with_flightlist(results)
        elif origin:
            results = await b2b.async_flightlistbyaerodrome(
                self.client, origin, "DEPARTURE", start=start, stop=stop
            )
            self.update_with_flightlist(results)
        elif destination:
            results = await b2b.async_flightlistbyaerodrome(
                self.client, destination, "ARRIVAL", start=start, stop=stop
            )
            self.update_with_flightlist(results)
        elif airspace:
            results = await b2b.async_flightlistbyairspace(
                self.client, airspace, start=start, stop=stop
            )
            self.update_with_flightlist(results)
        elif regulation:
            results = await b2b.async_flightlistbymeasure(
                self.client, regulation=regulation, start=start, stop=stop
            )
            self.update_with_flightlist(results)
        else:
            return

        self.query_one("#results", Static).update(
            JSON(json.dumps(results.json))
        )

    async def update_flight(self, flight: FlightRetrieval) -> None:
        self.query_one(Tabs).remove_class("hidden")
        tabbed_content = self.query_one(TabbedContent)
        tabbed_content.show_tab("flight-pane")
        tabbed_content.active = "flight-pane"

        flight_content = self.query_one(Flight)
        regulation = None
        if regulation_id := flight.json["data"]["flight"].get(
            "mostPenalisingRegulation", None
        ):
            regulation = await b2b.async_regulationlist(
                self.client,
                start=flight.json["data"]["flight"].get(
                    "estimatedTakeOffTime", None
                ),
                stop=flight.json["data"]["flight"].get(
                    "estimatedTimeOfArrival", None
                ),
                regulations=regulation_id,
            )
        flight_content.update_flight(flight, regulation)

    def update_with_flightlist(
        self,
        flightlist: None
        | FlightListByAerodrome
        | FlightListByAirspace
        | FlightListByMeasure,
    ) -> None:
        table = self.query_one(DataTable)

        table.clear(columns=True)
        table.add_columns(
            "date",
            "icao24",
            "typecode",
            "callsign",
            "number",
            "from",
            "to",
            "EOBT",
            "flightid",
            "regulation",
        )
        if flightlist is None:
            return None

        if flightlist.json["data"] is None:
            return None

        def eobt(entry: FlightOrFlightPlan) -> str:
            if flight_id := entry.get("flight", None):
                return flight_id["flightId"]["keys"]["estimatedOffBlockTime"]
            return ""

        fpl_data = flightlist.json
        s = fpl_data["data"]["flights"]
        summaries: list[FlightOrFlightPlan] = s if isinstance(s, list) else [s]
        summaries = sorted(summaries, key=eobt)

        table.add_rows(
            (
                (
                    f"{Time(eobt(entry)):%d %b %y}",
                    flight.get("aircraftAddress", "").lower(),
                    flight.get("aircraftType", None),
                    flight["flightId"]["keys"]["aircraftId"],
                    flight.get("iataFlightDesignator", {"id": ""})["id"],
                    flight["flightId"]["keys"]["aerodromeOfDeparture"],
                    flight["flightId"]["keys"]["aerodromeOfDestination"],
                    f"{Time(eobt(entry)):%H:%MZ}",
                    flight["flightId"].get("id", None),
                    flight.get("mostPenalisingRegulation", None),
                )
                for entry in summaries
                if (flight := entry.get("flight", None))
            ),
        )

    def update_with_flightplan(
        self, flightplanlist: None | FlightPlanList
    ) -> None:
        table = self.query_one(DataTable)

        table.clear(columns=True)
        table.add_columns(
            "date", "callsign", "from", "to", "EOBT", "flightid", "status"
        )
        if flightplanlist is None:
            return None

        if flightplanlist.json["data"] is None:
            return None

        def eobt(entry: FlightPlanOrInvalidFiling) -> str:
            if lfvp := entry.get("lastValidFlightPlan", None):
                return lfvp["id"]["keys"]["estimatedOffBlockTime"]
            return ""

        fpl_data = flightplanlist.json
        s = fpl_data["data"]["summaries"]
        summaries = s if isinstance(s, list) else [s]
        summaries = sorted(summaries, key=eobt)

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
