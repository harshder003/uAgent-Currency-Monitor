#Connect to the Database

import asyncio
import os
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient  # motor is an async mongodb driver
from odmantic.engine import AIOEngine
from odmantic.field import Field
from odmantic.model import Model

from messages import SendsTo



MONGODB_URL = os.getenv("MONGODB_URL")
assert MONGODB_URL, "Please set the MONGODB_URL environment variable"


class Data(Model):
    """

    Attributes:
        address (str): Address of the agent
        email (Optional[str]): Email of the user
        base(str): Base currency
        foreign(str): Foreign currency
        minimum_value (float): Minimum value
        maximum_value (float): Maximum value
        sends_to (list[SendsTo]): List of destinations where the user wants to receive the temperature alert

    """
    address: str = Field(primary_field=True)
    email: Optional[str] = Field(default=None)
    base: str
    foreign: str
    minimum_value: float
    maximum_value: float
    sends_to: list[SendsTo] = Field(default=[SendsTo.AGENT])


class Database:
    """

    Attributes:
        client (AsyncIOMotorClient): AsyncIOMotorClient object
        engine (AIOEngine): AIOEngine object
        _started (bool): True if the database is connected, False otherwise

    """

    def __init__(self) -> None:
        self._started = False

    async def connect(self):
        """
        This function is used to connect to the database.

        Returns:
            None

        """
        if self._started:
            return  # do not proceed if database is already connected

        # connect to the database
        self.client = AsyncIOMotorClient(
            MONGODB_URL, io_loop=asyncio.get_running_loop()
        )
        self.engine = AIOEngine(
            self.client, database="currency_agent"
        )  # create engine
        self._started = True

    async def find_all(self):
        """

        Yields:
            Data: Data object

        """
        await self.connect()  # connect to the database
        async for data in self.engine.find(Data):  # fetch all users from database
            yield data

    async def insert(
        self,
        address: str,
        base: str,
        foreign: str,
        min_value: float,
        max_value: float,
        sends_to: list[SendsTo],
        email: Optional[str] = None,
    ):
        """

        Args:
            address (str): Address of the agent
            base (str): Base currency
            foreign (str): Foreign currency
            min_value (float): Minimum value
            max_value (float): Maximum value
            sends_to (list[SendsTo]): List of destinations where the user wants to receive the temperature alert
            email (Optional[str]): Email of the user

        Returns:
            None

        """
        sends_to = list(set(sends_to))  # remove duplicates from sends_to list
        await self.connect()  # connect to the database
        await self.engine.save(
            Data(
                address=address,
                email=email,
                base=base,
                foreign=foreign,
                minimum_value=min_value,
                maximum_value=max_value,
                sends_to=sends_to,
            )
        )  # insert user into database

    async def remove(self, address: str):
        """

        Args:
            address (str): Address of the agent

        Returns:
            None

        """
        await self.connect()  # connect to the database
        await self.engine.database[Data.__collection__].delete_one({"_id": address})
        # remove user from database
