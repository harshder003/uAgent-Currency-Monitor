from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

from src.messages import (
    SendsTo,
    CurrencyCondition,
    CurrencyRequest,
    CurrencyWarn,
    UAgentResponse,
    UAgentResponseType,
)


main_agent = Agent(
    name="main_agent",
    port=8001,
    seed='main_agent',
    endpoint=["http://localhost:8001/submit"],
)

fund_agent_if_low(str(main_agent.wallet.address()))


@main_agent.on_interval(period=5*60)
async def send_currency_request(ctx: Context):
    """await ctx.send(
        "<temperaure_agent_address>",  # Address of the currency agent
        CurrencyRequest(
            base="USD",
            foreign="INR",
            minimum_temperature=80,
            maximum_temperature=83,
            sends_to=[SendsTo.AGENT],
        ),
    )"""
    await ctx.send(
        "<temperaure_agent_address>",
        CurrencyRequest(
            base="USD",#You can set your base currency
            foreign="INR",#You can set your foreign currency
            email="receiveraddress@gmail.com",#Add your email address
            minimum_value=80,
            maximum_value=83,
            sends_to=[SendsTo.EMAIL, SendsTo.AGENT],
        ),
    )


@main_agent.on_message(model=UAgentResponse)
async def receive_update(ctx: Context, sender: str, message: UAgentResponse):
    if message.type == UAgentResponseType.MESSAGE:
        ctx.logger.info(f"{sender}: {message.message}")
    elif message.type == UAgentResponseType.ERROR:
        ctx.logger.error(f"{sender}: {message.message}")


@main_agent.on_message(model=CurrencyWarn)
async def receive_warning(ctx: Context, sender: str, message: CurrencyWarn):
    # Client can do anything with the data received

    thershold = {
        CurrencyCondition.LOW: message.minimum_value,
        CurrencyCondition.HIGH: message.maximum_value,
    }
    ctx.logger.info(
        f"Rate of {message.foreign} with respect to {message.base} is {message.rate}\n"
        f"{message.condition.value.title()}er than the set threshold of {thershold[message.condition]}!"
    )


if __name__ == "__main__":
    main_agent.run()