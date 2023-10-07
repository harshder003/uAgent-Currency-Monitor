import os
import logging
import requests
from dotenv import load_dotenv

from messages import CurrencyExchangeRequest, CurrencyUAgentResponse, CurrencyUAgentResponseType
from uagents import Agent, Context, Protocol, Bureau

# Load the environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)


def get_user_input():
    base_currency = input("Enter the base currency (e.g., USD): ").upper()
    foreign_currency = input("Enter the foreign currency you want to monitor (e.g., EUR): ").upper()
    min_value = float(input(f"Enter the minimum desired value for {foreign_currency} with respect to {base_currency}: "))
    max_value = float(input(f"Enter the maximum desired value for {foreign_currency} with respect to {base_currency}: "))

    return base_currency, foreign_currency, min_value, max_value


FIXER_API_KEY = os.getenv("FIXER_API_KEY", "")
assert FIXER_API_KEY, "FIXER_API_KEY environment variable is missing from .env"
FIXER_API_URL = "http://data.fixer.io/api/latest"


def fetch_exchange_rate(base_currency, foreign_currency):
    params = {
        "access_key": FIXER_API_KEY,
        "base": base_currency,
        "symbols": foreign_currency
    }
    response = requests.get(FIXER_API_URL, params=params)
    response.raise_for_status()

    data = response.json()
    return data.get("rates", {}).get(foreign_currency)


agent = Agent(name="currency_adaptor", seed='currency exchange service secret phrase')
currency_alert_protocol = Protocol("CurrencyAlert")


@currency_alert_protocol.on_message(model=CurrencyExchangeRequest, replies=CurrencyUAgentResponse)
async def currency_alert(ctx: Context, sender: str, msg: CurrencyExchangeRequest):
    try:
        current_rate = fetch_exchange_rate(msg.base_currency, msg.foreign_currency)
        if current_rate > msg.max_value:
            alert_message = f"Alert: {msg.base_currency} to {msg.foreign_currency} exchange rate has gone above the max value!"
        elif current_rate < msg.min_value:
            alert_message = f"Alert: {msg.base_currency} to {msg.foreign_currency} exchange rate has gone below the min value!"
        else:
            alert_message = None

        if alert_message:
            await ctx.send(
                sender,
                CurrencyUAgentResponse(
                    type=CurrencyUAgentResponseType.THRESHOLD_ALERT,
                    base_currency=msg.base_currency,
                    foreign_currencies=[{"currency": msg.foreign_currency, "max_value": msg.max_value, "min_value": msg.min_value}],
                    alert_message=alert_message
                )
            )

    except Exception as exc:
        ctx.logger.error(exc)
        await ctx.send(
            sender,
            CurrencyUAgentResponse(
                type=CurrencyUAgentResponseType.ERROR,
                base_currency=msg.base_currency,
                foreign_currencies=[{"currency": msg.foreign_currency}],
                alert_message=str(exc)
            )
        )


agent.include(currency_alert_protocol)

if __name__ == "__main__":
    base_currency, foreign_currency, min_value, max_value = get_user_input()
    alert_thresholds = {foreign_currency: (min_value, max_value)}

    request = CurrencyExchangeRequest(
        base_currency=base_currency,
        target_currencies=[foreign_currency],
        alert_thresholds=alert_thresholds
    )
    logging.info(f"Received user request: {request}")

    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    logging.info(f"Adding Currency Market agent to Bureau: {agent.address}")
    bureau.add(agent)
    
    bureau.run()
