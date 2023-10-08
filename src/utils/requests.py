from __future__ import annotations

import os
from typing import Optional

import aiohttp  # for making http requests

ACCESS_KEY = os.getenv("ACCESS_KEY")
assert ACCESS_KEY, "Please set the ACCESS_KEY environment variable"


class RequestHandler:
    """

    Attributes:
        _session (Optional[aiohttp.ClientSession]): aiohttp.ClientSession object

    Properties:
        session (aiohttp.ClientSession): aiohttp.ClientSession object
    """

    def __init__(self) -> None:
        self._session: Optional[aiohttp.ClientSession] = None
        # initialize session to None

    async def start(self):
        """

        Returns:
            None

        """
        if self._session and not self._session.closed:
            return  # do not proceed if session is already started
        self._session = aiohttp.ClientSession()  # start session

    async def stop(self):
        """

        Returns:
            None

        """
        if self._session is None:
            return  # do not proceed if session is None
        if not self._session.closed:
            await self._session.close()
        self._session = None

    @property
    def session(self):
        """

        Returns:
            aiohttp.ClientSession: aiohttp.ClientSession object

        Raises:
            RuntimeError: Session not started

        """
        if self._session is None or self._session.closed:
            raise RuntimeError(
                "Session not started"
            )  # raise exception if session is not started
        return self._session

    async def fetch_rate(self, base: str,foreign: str) -> float:
        """

        Args:
            base (str): Base currency
            foreign (str): Foreign currency

        Returns:
            float: rate of the foreign currency with respect to the base currency

        Raises:
            ValueError: Base not found

        """
        async with self.session.get(  # make http request to fetch latitude and longitude
            f"https://api.freecurrencyapi.com/v1/latest?apikey={ACCESS_KEY}"
        ) as response:
            data = await response.json()
            try:
                return data['data'][foreign]
            except Exception:
                raise ValueError(
                    f"Base: {base} not found"
                )  # raise exception if location is not found
