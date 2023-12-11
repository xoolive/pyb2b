class FlightList:
    def flight_list(
        self,
        start: None | str | pd.Timestamp = None,
        stop: None | str | pd.Timestamp = None,
        *args: Any,
        airspace: None | str = None,
        airport: None | str = None,
        origin: None | str = None,
        destination: None | str = None,
        regulation: None | str = None,
        include_proposal: bool = False,
        include_forecast: bool = True,
        fields: None | list[str] = None,
    ) -> None | FlightList:
        """Returns requested information about flights matching a criterion.

        :param start: (UTC), by default current time
        :param stop: (UTC), by default one hour later

        Exactly one of the following parameters must be passed:

        :param airspace: the name of an airspace aircraft fly through
        :param airport: flying from or to a given airport (ICAO 4 letter code).
        :param origin: flying from a given airport (ICAO 4 letter code).
        :param destination: flying to a given airport (ICAO 4 letter code).
        :param regulation: identifier of a regulation (see
            :meth:`~traffic.data.eurocontrol.b2b.NMB2B.regulation_list`)
        :param fields: additional fields to request. By default, a set of
            (arguably) relevant fields are requested.

        **Example usage:**

        .. jupyter-execute::

            # Get all flights scheduled out of Paris CDG
            nm_b2b.flight_list(origin="LFPG")

        **See also:**

            - :meth:`~traffic.data.eurocontrol.b2b.NMB2B.flight_get` returns
              full information about a given flight. It is also accessible by
              indexing a
              :class:`~traffic.data.eurocontrol.b2b.flight.FlightList` object
              with the ``flightId`` field.

        """

        if start is not None:
            start = pd.Timestamp(start, tz="utc")

        if stop is not None:
            stop = pd.Timestamp(stop, tz="utc")
        else:
            stop = start + pd.Timedelta("1H")

        msg = """At most one parameter must be set among:
- airspace
- airport (or origin, or destination)
        """
        query = [airspace, airport, origin, destination, regulation]
        if sum(x is not None for x in query) > 1:
            raise RuntimeError(msg)

        _fields = fields if fields is not None else []
        if airspace is not None:
            data = REQUESTS["FlightListByAirspaceRequest"].format(
                send_time=pd.Timestamp("now", tz="utc"),
                start=start,
                stop=stop,
                requestedFlightFields="\n".join(
                    f"<requestedFlightFields>{field}</requestedFlightFields>"
                    for field in default_flight_fields.union(_fields)
                ),
                airspace=airspace,
                include_forecast=f"{include_forecast}".lower(),
                include_proposal=f"{include_proposal}".lower(),
            )
            rep = self.post(data)  # type: ignore
            return FlightList.fromB2BReply(rep)

        if airport is not None or origin is not None or destination is not None:
            role = "BOTH"
            if origin is not None:
                airport = origin
                role = "DEPARTURE"
            if destination is not None:
                airport = destination
                role = "ARRIVAL"

            data = REQUESTS["FlightListByAerodromeRequest"].format(
                send_time=pd.Timestamp("now", tz="utc"),
                start=start,
                stop=stop,
                requestedFlightFields="\n".join(
                    f"<requestedFlightFields>{field}</requestedFlightFields>"
                    for field in default_flight_fields.union(_fields)
                ),
                aerodrome=airport,
                aerodromeRole=role,
                include_forecast=f"{include_forecast}".lower(),
                include_proposal=f"{include_proposal}".lower(),
            )
            rep = self.post(data)  # type: ignore
            return FlightList.fromB2BReply(rep)

        if regulation is not None:
            data = REQUESTS["FlightListByMeasureRequest"].format(
                send_time=pd.Timestamp("now", tz="utc"),
                start=start,
                stop=stop,
                requestedFlightFields="\n".join(
                    f"<requestedFlightFields>{field}</requestedFlightFields>"
                    for field in default_flight_fields.union(_fields)
                ),
                regulation=regulation,
                include_forecast=f"{include_forecast}".lower(),
                include_proposal=f"{include_proposal}".lower(),
            )
            rep = self.post(data)  # type: ignore
            return FlightList.fromB2BReply(rep)

        return None
