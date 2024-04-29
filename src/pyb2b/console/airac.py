import argparse
import asyncio
import logging
from pathlib import Path

import httpx

from pyb2b import b2b

description = """
Get data from Network Manager B2B Service.
"""


def main() -> None:
    parser = argparse.ArgumentParser(prog="airac", description=description)

    parser.add_argument(
        "-v",
        dest="verbose",
        action="count",
        default=0,
        help="display logging messages",
    )

    parser.add_argument("-a", dest="airac", default=None, help="AIRAC version")

    args = parser.parse_args()

    logger = logging.getLogger()
    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 2:
        logger.setLevel(logging.DEBUG)

    if args.airac is not None:

        async def download_data() -> None:
            async with httpx.AsyncClient(verify=b2b.context) as client:
                await b2b.async_aixm_request(client, args.airac, Path("."))

        asyncio.run(download_data())
    else:
        raise RuntimeError("No action requested")


if __name__ == "__main__":
    main()
