class FlightRetrieval:
    def flight_retrieval(
        self,
        EOBT: str | pd.Timestamp,
        callsign: str,
        origin: str,
        destination: str,
    ) -> FlightInfo:
        """Returns full information about a given flight.

        This method requires all parameters:

        :param EOBT: Estimated off-block time
        :param callsign: **NO** wildcard accepted
        :param origin: flying from a given airport (ICAO 4 letter code).
        :param destination: flying to a given airport (ICAO 4 letter code).

        This method is called when indexing the return value of a
        :meth:`~traffic.data.eurocontrol.b2b.NMB2B.flight_search`.

        """

        EOBT = pd.Timestamp(EOBT, tz="utc")
        data = REQUESTS["FlightRetrievalRequest"].format(
            send_time=pd.Timestamp("now", tz="utc"),
            callsign=callsign,
            origin=origin,
            destination=destination,
            eobt=EOBT,
        )
        rep = self.post(data)  # type: ignore
        return FlightInfo.fromET(rep.reply.find("data/flight"))
