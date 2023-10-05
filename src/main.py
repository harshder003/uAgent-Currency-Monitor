import os
import uuid
import logging

import requests
from messages import CurrencyExchangeRequest, CurrencyUAgentResponse, CurrencyUAgentResponseType
from uagents import Agent, Context, Protocol, Bureau

logging.basicConfig(level=logging.INFO)

def get_user_input():
    base_currency = input("Enter the base currency (e.g., USD): ").upper()
    foreign_currency = input("Enter the foreign currency you want to monitor (e.g., EUR): ").upper()
    min_value = float(input(f"Enter the minimum desired value for {foreign_currency} with respect to {base_currency}: "))
    max_value = float(input(f"Enter the maximum desired value for {foreign_currency} with respect to {base_currency}: "))

    return base_currency, foreign_currency, min_value, max_value

# CURRENCY_MARKET_SEED = os.getenv(
#     "CURRENCY_MARKET_SEED", "currency market adaptor agent secret phrase"
# )
agent = Agent(name="currency_market_adaptor", seed='Currency market adaptor agent secret phrase')
currency_market_protocol = Protocol("CurrencyMarket")

FIXER_API_KEY = os.getenv("FIXER_API_KEY", "")
assert FIXER_API_KEY, "FIXER_API_KEY environment variable is missing from .env"
FIXER_API_URL = "http://data.fixer.io/api/latest"

# ... [rest of the agent and protocol definitions here]

if __name__ == "__main__":
    base_currency, foreign_currency, min_value, max_value = get_user_input()
    
    # Create a CurrencyExchangeRequest message with the user's input
    request = CurrencyExchangeRequest(base_currency=base_currency, foreign_currency=foreign_currency, min_value=min_value, max_value=max_value)
    
    # Here you can process the request using your agent or send it to another agent for processing.
    # For this example, I'll just print the request for clarity.
    logging.info(f"Received user request: {request}")

    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    logging.info(f"Adding Currency Market agent to Bureau: {agent.address}")
    bureau.add(agent)
    
    bureau.run()
