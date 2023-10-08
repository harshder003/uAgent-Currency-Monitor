from enum import Enum

from uagents import Model


class CurrencyCondition(Enum):
    """
    This class is used to define the temperature condition.

    Attributes:
        LOW (str): Low temperature
        HIGH (str): High temperature

    """

    LOW = "low"
    HIGH = "high"


class CurrencyWarn(Model):
    """

    Attributes:
        base(str): Base currency
        foreign(str): Foreign currency
        rate (float): Rate of foreign currency with respect to base currency
        condition (CurrencyCondition): Currency condition
        minimum_value (float): Minimum value
        maximum_value (float): Maximum value
    """

    base: str
    foreign: str
    rate: float
    condition: CurrencyCondition
    minimum_value: float
    maximum_value: float
