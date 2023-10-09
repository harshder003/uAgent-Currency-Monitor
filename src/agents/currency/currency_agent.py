from __future__ import annotations  # for type hinting

import os
from typing import TYPE_CHECKING

from uagents import Agent
from uagents.setup import fund_agent_if_low

from messages import (
    SendsTo,
    CurrencyCondition,
    CurrencyRequest,
    CurrencyWarn,
    UAgentResponse,
    UAgentResponseType,
)
from utils.cooldown import Cooldown
from utils.database import Database
from utils.email import send_email, send_verifaction, verify_regex
from utils.requests import RequestHandler

if TYPE_CHECKING:  # to avoid useless imports
    from uagents import Context

currency_agent = Agent(name="currency", seed='Currency Agent')
fund_agent_if_low(str(currency_agent.wallet.address()))


# creating instances of classes
request_handler = RequestHandler()
database = Database()

# creating cooldowns
update_cooldown = Cooldown(5*60)
alert_cooldown = Cooldown(3 * 60)


@currency_agent.on_event("startup")
async def startup(ctx: Context):
    """

    Args:
        ctx (Context): Context object

    Returns:
        None
    """
    ctx.logger.info("Starting up Currency agent")
    await request_handler.start()


@currency_agent.on_event("shutdown")
async def shutdown(ctx: Context):
    """

    Args:
        ctx (Context): Context object

    Returns:
        None
    """
    ctx.logger.info("Shutting down currency agent")
    await request_handler.stop()


@currency_agent.on_interval(period=30 * 60)
async def scan_all(ctx: Context):
    """

    Args:
        ctx (Context): Context object

    Returns:
        None
    """
    async for data in database.find_all():
        if alert_cooldown.on_waiting(data.address):
            continue

        rate = await request_handler.fetch_rate(data.base, data.foreign)

        if rate < data.minimum_value:
            body = (
                f"Rate {rate} lower than the set minimum threshold of {data.minimum_value} Celsius\n"
                f"Base Currency: {data.base.title()}\n"
                f"Foreign Currency: {data.foreign.title()}\n"
            )
            condition = CurrencyCondition.LOW
        elif rate > data.maximum_value:
            body = (
                f"Rate {rate} higher than the set maximum threshold of {data.maximum_value} Celsius\n"
                f"Base Currency: {data.base.title()}\n"
                f"Foreign Currency: {data.foreign.title()}\n"
            )
            condition = CurrencyCondition.HIGH
        else:
            continue

        
        if (SendsTo.EMAIL in data.sends_to) and data.email:
            try:
                await send_email(data.email, "RATE ALERT !", body)
            except Exception as e:
                ctx.logger.error(str(e))
        if SendsTo.AGENT in data.sends_to:
            await ctx.send(
                data.address,
                CurrencyWarn(
                    base=data.base,
                    foreign=data.foreign,
                    rate=rate,
                    condition=condition,
                    minimum_value=data.minimum_value,
                    maximum_value=data.maximum_value,
                ),
            )
        alert_cooldown.update(data.address)


@currency_agent.on_message(model=CurrencyRequest, replies=UAgentResponse)
async def add_user(ctx: Context, sender: str, message: CurrencyRequest):
    """

    Args:
        ctx (Context): Context object
        sender (str): Address of the sender
        message (CurrencyRequest): CurrencyRequest message sent by the user

    Returns:
        None
    """

    # check if user is on cooldown
    if update_cooldown.on_waiting(sender):
        await ctx.send(
            sender,
            UAgentResponse(
                type=UAgentResponseType.ERROR,
                message="You are on cooldown, try again in 5 minutes !",
            ),
        )
        return
    update_cooldown.update(sender)  # update cooldown

    ctx.logger.info(f"Received rate request.")

    try:
        if SendsTo.EMAIL in message.sends_to:
            if message.email is None:  # check if email is provided
                raise Exception("Email is required for email alerts !")

            verify_regex(message.email)  # check if email has viable regex
            await send_verifaction(message.email)
    except Exception as e:
        ctx.logger.error(str(e))
        await ctx.send(
            sender, UAgentResponse(type=UAgentResponseType.ERROR, message=str(e))
        )
        return

    await database.insert(
        address=sender,
        email=message.email,
        base=message.base,
        foreign=message.foreign,
        min_value=message.minimum_value,
        max_value=message.maximum_value,
        sends_to=message.sends_to,
    )

    await ctx.send(
        sender,
        UAgentResponse(
            type=UAgentResponseType.MESSAGE,
            message="Base Currency added successfully for updates !",
        ),
    )


@currency_agent.on_message(model=UAgentResponse, replies=UAgentResponse)
async def remove_user(ctx: Context, sender: str, message: UAgentResponse):
    """

    Args:
        ctx (Context): Context object
        sender (str): Address of the sender
        message (UAgentResponse): UAgentResponse message sent by the user

    Returns:
        None
    """

    if message.message != "remove":
        return  # if message is not "remove", return

    # check if user is on cooldown
    if update_cooldown.on_waiting(sender):
        await ctx.send(
            sender,
            UAgentResponse(
                type=UAgentResponseType.ERROR,
                message="You are on cooldown, try again in 5 minutes !",
            ),
        )
        return
    update_cooldown.update(sender)
    ctx.logger.info(f"Removing user {sender} !")
    await database.remove(sender)
    await ctx.send(
        sender,
        UAgentResponse(
            type=UAgentResponseType.MESSAGE,
            message="Rate updates removed successfully !",
        ),
    )
