from enum import Enum
from typing import Optional

from uagents import Model


class UAgentResponseType(Enum):
    """

    Attributes:
        ERROR (str): Error message
        MESSAGE (str): Success message
    """

    ERROR = "error"
    MESSAGE = "message"


class UAgentResponse(Model):
    """

    Attributes:
        type (UAgentResponseType): Type of response
        message (Optional[str]): Message sent by the agent

    """

    type: UAgentResponseType
    message: Optional[str] = None
