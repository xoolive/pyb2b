from __future__ import annotations

import json
from numbers import Integral, Real
from pathlib import Path
from typing import Any, ClassVar, Generic, Type, TypeVar

from rich.box import SIMPLE_HEAVY
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

import pandas as pd

from .types.generated.common import Reply

D = TypeVar("D", bound="DataFrameMixin")
J = TypeVar("J", bound="JSONMixin[Any]")
T = TypeVar("T", bound=Reply)


class JSONMixin(Generic[T]):
    json: T

    def __init__(self, json: T, *args: Any, **kwargs: Any) -> None:
        self.json = json

    @classmethod
    def from_file(cls: Type[J], filename: str | Path) -> J:
        path = Path(filename)
        return cls(json.loads(path.read_text()))

    def to_file(self, filename: None | str | Path = None) -> None:
        if filename is None:
            filename = " ".join(
                [self.json["requestReceptionTime"], self.json["requestId"]]
            )
        path = Path(filename)
        path.write_text(json.dumps(self.json, indent=2))


class DataFrameMixin:
    table_options: ClassVar[dict[str, Any]] = dict(
        show_lines=False, box=SIMPLE_HEAVY
    )
    max_rows: int = 10
    columns_options: ClassVar[None | dict[str, dict[str, Any]]] = None
    _obfuscate: None | list[str] = None

    @property
    def data(self) -> pd.DataFrame:
        ...

    def _repr_html_(self) -> None | str:
        return self.data._repr_html_()  # type: ignore

    def __rich_console__(
        self,
        _console: Console,
        _options: ConsoleOptions,
    ) -> RenderResult:
        my_table = Table(**self.table_options)

        if self.columns_options is None:
            self.columns_options = dict(  # type: ignore
                (column, dict()) for column in self.data.columns
            )

        for column, opts in self.columns_options.items():
            my_table.add_column(column, **opts)

        # This is only for documentation purposes, shouldn't be considered for
        # real-life code
        data = self.data[: self.max_rows]
        if self._obfuscate:
            for column in self._obfuscate:
                data = data.assign(**{column: "xxxxxx"})

        for _, elt in data.iterrows():
            my_table.add_row(
                *list(
                    format(
                        elt.get(column, ""),
                        ".4g"
                        if isinstance(elt.get(column, ""), Real)
                        and not isinstance(elt.get(column, ""), Integral)
                        else "",
                    )
                    for column in self.columns_options
                )
            )

        yield my_table

        delta = self.data.shape[0] - self.max_rows
        if delta > 0:
            yield f"... ({delta} more entries)"
