import os
import uuid

import requests
from messages import CurrencyExchangeRequest, KeyValue, CurrencyUAgentResponse, CurrencyUAgentResponseType
from uagents import Agent, Context, Protocol

# CURRENCY_MARKET_SEED = os.getenv(
#     "CURRENCY_MARKET_SEED", "currency market adaptor agent secret phrase"
# )
agent = Agent(name="currency_market_adaptor", seed='Currency market adaptor agent secret phrase')
currency_market_protocol = Protocol("CurrencyMarket")

FIXER_API_KEY = os.getenv("FIXER_API_KEY", "")

assert FIXER_API_KEY, "FIXER_API_KEY environment variable is missing from .env"

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


@currency_market_protocol.on_message(model=CurrencyExchangeRequest, replies=CurrencyUAgentResponse)
async def currency_market(ctx: Context, sender: str, msg: CurrencyExchangeRequest):
    ctx.logger.info(f"Received currency monitoring request from {sender}")
    try:
        current_rate = get_exchange_rate(msg.base_currency, msg.foreign_currency)
        request_id = str(uuid.uuid4())
        if current_rate > msg.max_value:
            message = f"Alert: {msg.base_currency} to {msg.foreign_currency} exchange rate has gone above the max value!"
        elif current_rate < msg.min_value:
            message = f"Alert: {msg.base_currency} to {msg.foreign_currency} exchange rate has gone below the min value!"
        else:
            message = f"{msg.base_currency} to {msg.foreign_currency} exchange rate is within the specified range."
        
        await ctx.send(
            sender,
            CurrencyUAgentResponse(
                message=message,
                type=CurrencyUAgentResponseType.FINAL,
                request_id=request_id,
            )
        )
    except Exception as exc:
        ctx.logger.error(exc)
        await ctx.send(
            sender, CurrencyUAgentResponse(message=str(exc), type=CurrencyUAgentResponseType.ERROR)
        )


agent.include(currency_market_protocol)
