from uagents import Model
from typing import List, Optional, Dict, Tuple

class CurrencyExchangeRequest(Model):
    """
    Represents a Currency Exchange Request.

    Attributes:
        base_currency (str): The base currency from which conversion will take place (e.g., "USD").
        target_currencies (List[str]): A list of target currencies to which conversion rates are requested.
        alert_thresholds (Optional[Dict[str, Tuple[float, float]]]): An optional dictionary specifying the 
            desired alert thresholds for each target currency. 
            For example: {"EUR": (0.8, 0.9)} means the user wants to be alerted 
            if 1 USD is less than 0.8 EUR or more than 0.9 EUR.
    """

    base_currency: str
    target_currencies: List[str]
    alert_thresholds: Optional[Dict[str, Tuple[float, float]]]
