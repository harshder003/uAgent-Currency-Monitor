import logging
from agents.user import agent as user_agent
from agents.market import agent as market_agent
from uagents import Bureau

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    bureau = Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    
    logging.info(f"Adding User agent to Bureau: {user_agent.address}")
    bureau.add(user_agent)
    
    logging.info(f"Adding Market agent to Bureau: {market_agent.address}")
    bureau.add(market_agent)
    
    bureau.run()
