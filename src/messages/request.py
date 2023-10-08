from enum import StrEnum
from typing import Optional

from pydantic import Field
from uagents import Model


class SendsTo(StrEnum):
    """
    This class is used to define the destinations where the user wants to receive the temperature alert.

    Attributes:
        AGENT (str): Agent
        EMAIL (str): Email

    """

    AGENT = "agent"
    EMAIL = "email"


class CurrencyRequest(Model):
    """

    Attributes:
        email (Optional[str]): Email of the user
        base (str): Base currency
        foreign (str): Foreign currency
        minimum_value (int): Minimum rate
        maximum_value (int): Maximum rate
        sends_to (list[SendsTo]): List of destinations where the user wants to receive the currency alert
    """

    email: Optional[str] = None
    base: str
    foreign: str
    minimum_value: int
    maximum_value: int
    sends_to: list[SendsTo] = Field(default=[SendsTo.AGENT])
