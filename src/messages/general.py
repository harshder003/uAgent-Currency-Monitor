from enum import Enum
from typing import List, Optional

from uagents import Model


class CurrencyUAgentResponseType(Enum):
    """
    Enumeration representing different types of responses from the Currency User Agent.

    Attributes:
        ERROR (str): Represents an error response type.
        THRESHOLD_ALERT (str): Represents a response type indicating that a currency has crossed the threshold.
        RATE_UPDATE (str): Represents a response type indicating an update in the currency rate.
    """

    ERROR = "error"
    THRESHOLD_ALERT = "threshold_alert"
    RATE_UPDATE = "rate_update"


class CurrencyRate(Model):
    """
    Represents a foreign currency with its max and min values.

    Attributes:
        currency (str): The foreign currency code (e.g., "INR", "EUR").
        max_value (float): The maximum value for the currency.
        min_value (float): The minimum value for the currency.
    """

    currency: str
    max_value: float
    min_value: float


class CurrencyUAgentResponse(Model):
    """
    Represents a Currency User Agent Response.

    Attributes:
        type (CurrencyUAgentResponseType): The type of the response.
        base_currency (str): The base currency code (e.g., "USD").
        foreign_currencies (List[CurrencyRate]): A list of foreign currencies with their max and min values.
        alert_message (Optional[str]): A message indicating a currency going out of bounds.
    """

    type: CurrencyUAgentResponseType
    base_currency: str
    foreign_currencies: List[CurrencyRate]
    alert_message: Optional[str]
