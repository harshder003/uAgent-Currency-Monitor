from uagents import Model
from typing import List, Optional, Dict, Tuple

class UserPreferences(Model):
    """
    Represents a user's preferences for currency exchange monitoring.

    Attributes:
        user_id (str): Unique identifier for the user.
        base_currency (str): The user's primary currency for which they wish to monitor exchange rates.
        monitored_currencies (List[str]): A list of currencies that the user is interested in monitoring.
        alert_thresholds (Dict[str, Tuple[float, float]]): Dictionary specifying the desired alert thresholds 
            for each monitored currency. For example: {"EUR": (0.8, 0.9)} means the user wants to be alerted 
            if 1 base currency is less than 0.8 EUR or more than 0.9 EUR.
        notification_channel (Optional[str]): Preferred channel for receiving alerts (e.g., "email", "SMS").
        contact_details (Optional[str]): Contact details for sending alerts, like email address or phone number.
    """

    user_id: str
    base_currency: str
    monitored_currencies: List[str]
    alert_thresholds: Dict[str, Tuple[float, float]]
    notification_channel: Optional[str]
    contact_details: Optional[str]
