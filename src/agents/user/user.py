import os
# import uuid
import logging
import requests
from messages import CurrencyExchangeRequest, CurrencyUAgentResponse, CurrencyUAgentResponseType
from uagents import Agent, Context, Protocol

# CURRENCY_SEED = os.getenv("CURRENCY_SEED", "currency exchange service secret phrase")

agent = Agent(
    name="currency_adaptor",
    seed='currency exchange service secret phrase',
)

FIXER_API_KEY = os.environ.get("FIXER_API_KEY", "")

assert (
    FIXER_API_KEY
), "FIXER_API_KEY environment variable is missing from .env"

FIXER_API_URL = "http://data.fixer.io/api/latest"


def get_exchange_rate(base_currency: str, target_currency: str) -> float:
    """Return the current exchange rate for the target currency with respect to the base currency."""
    response = requests.get(
        url=f"{FIXER_API_URL}?access_key={FIXER_API_KEY}&base={base_currency}&symbols={target_currency}",
        timeout=5,
    )
    if response.status_code == 200:
        data = response.json()
        return data['rates'][target_currency]
    return None


currency_alert_protocol = Protocol("CurrencyAlert")


@currency_alert_protocol.on_message(model=CurrencyExchangeRequest, replies=CurrencyUAgentResponse)
async def currency_alert(ctx: Context, sender: str, msg: CurrencyExchangeRequest):
    ctx.logger.info(f"Received currency monitoring request from {sender}")
    try:
        current_rate = get_exchange_rate(msg.base_currency, msg.foreign_currency)
        if current_rate > msg.max_value:
            logging.info(f"Alert: {msg.base_currency} to {msg.foreign_currency} exchange rate has gone above the max value!")
        elif current_rate < msg.min_value:
            logging.info(f"Alert: {msg.base_currency} to {msg.foreign_currency} exchange rate has gone below the min value!")
        # else:
        #     logging.info(f"{msg.base_currency} to {msg.foreign_currency} exchange rate is within the specified range.")
    except Exception as exc:
        ctx.logger.error(exc)
        await ctx.send(
            sender, CurrencyUAgentResponse(message=str(exc), type=CurrencyUAgentResponseType.ERROR)
        )


agent.include(currency_alert_protocol)
