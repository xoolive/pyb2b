import io
import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING, cast

import httpx
from pitot.airac import airac_cycle
from tqdm.asyncio import tqdm

import pandas as pd

from ....types.airspace.structure.aixm_dataset import (
    CompleteAIXMDatasetReply,
    File,
)

if TYPE_CHECKING:
    from ....main import B2B

_log = logging.getLogger(__name__)


class AIXMDataset:
    async def _async_file_get(
        self, client: httpx.AsyncClient, file: File, output_dir: str | Path
    ):
        self = cast(B2B, self)

        buffer = io.BytesIO()
        output_dir = Path(output_dir)
        path = output_dir / Path(file["id"].split("/")[-1])
        if path.exists():
            return

        async with client.stream(
            "GET",
            url=self.mode["file_url"] + file["id"],
        ) as response:
            total = int(file["fileLength"])
            async for chunk in tqdm(
                response.aiter_bytes(1024),
                total=total // 1024 + 1 if total % 1024 > 0 else 0,
                desc=path.stem,
            ):
                buffer.write(chunk)

        buffer.seek(0)

        _log.info(f"write {path}")
        path.write_bytes(buffer.getvalue())

    async def async_aixm_request(
        self,
        client: httpx.AsyncClient,
        airac_id: str | int | pd.Timestamp,
        output_dir: str | Path,
    ) -> None:
        """
        Downloads the EUROCONTROL data files following the AIXM standard.

        :param airac_id: the AIRAC cycle, e.g. 2201 (1st cycle of 2022)
        :param output_dir: where to download the data.

        **See also**: :ref:`How to configure EUROCONTROL data files?`
        """
        self = cast(B2B, self)

        if isinstance(airac_id, int) and not re.match(r"\d{4}", str(airac_id)):
            raise ValueError(
                "airac_id must be a 4 digit number, or a timestamp"
            )
        if not re.match(r"\d{4}", airac_id):
            airac_id = pd.Timestamp(airac_id, tz="utc")
        if isinstance(airac_id, pd.Timestamp):
            airac_id = airac_cycle(airac_id)

        now = pd.Timestamp("now", tz="utc")

        res: CompleteAIXMDatasetReply
        res = await self.async_post(
            client,
            {
                "airspace:CompleteAIXMDatasetRequest": {
                    "@xmlns:airspace": "eurocontrol/cfmu/b2b/AirspaceServices",
                    "sendTime": f"{now:%Y-%m-%d %H:%M:%S}",
                    "queryCriteria": {"airac": {"airacId": f"{airac_id}"}},
                }
            },
        )

        data = res["as:CompleteAIXMDatasetReply"]["data"]
        summaries = data["datasetSummaries"]
        entry = max(summaries, key=lambda x: x["updateId"])
        for file in entry["files"]:  # don't do asyncio.gather (ReadTimeout)
            await self.get(client, file, output_dir)
        return
