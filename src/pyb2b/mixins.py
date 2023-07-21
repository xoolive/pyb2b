from __future__ import annotations

from numbers import Integral, Real
from typing import Any, ClassVar, TypeVar

from rich.box import SIMPLE_HEAVY
from rich.console import Console, ConsoleOptions, RenderResult
from rich.table import Table

import pandas as pd

D = TypeVar("D", bound="DataFrameMixin")


class DataFrameMixin:
    table_options: ClassVar[dict[str, Any]] = dict(
        show_lines=False, box=SIMPLE_HEAVY
    )
    max_rows: int = 10
    columns_options: None | dict[str, dict[str, Any]] = None
    _obfuscate: None | list[str] = None

    def __init__(self, data: pd.DataFrame, *args: Any, **kwargs: Any) -> None:
        self.data = data

    def __getattr__(self: D, name: str) -> Any:
        if (handle := getattr(self.data, name, None)) is not None:
            if "DataFrame" in handle.__annotations__.get("return", ""):

                def wrapped(*args: Any, **kwargs: Any) -> D:
                    return self.__class__(handle(*args, **kwargs))

                return wrapped
            else:
                return handle
        raise AttributeError

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:
        my_table = Table(**self.table_options)

        if self.columns_options is None:
            self.columns_options = dict(
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
