import re
import asyncio
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Bot, Event

from wifi_bot.plugins.bilibili.data_source import get_av_data

# global_config = get_driver().config
# config = global_config.dict()
# b_sleep_time = config.get('b_sleep_time', 2)
# b_sleep_time = int(b_sleep_time)
b_sleep_time = 2

biliav = on_regex(r"[Aa][Vv]\d{1,12}|[Bb][Vv]1[A-Za-z0-9]{2}4.1.7[A-Za-z0-9]{2}|[Bb]23\.[Tt][Vv]/[A-Za-z0-9]{7}")


@biliav.handle()
async def _biliav_handle(bot: Bot, event: Event):
    avcode_list: list[str] = re.compile(
        r"[Aa][Vv]\d{1,12}|[Bb][Vv]1[A-Za-z0-9]{2}4.1.7[A-Za-z0-9]{2}|[Bb]23\.[Tt][Vv]/[A-Za-z0-9]{7}").findall(
        str(event.get_message()))
    if not avcode_list:
        return
    rj_list: list[str] = await get_av_data(avcode_list)
    for rj in rj_list:
        await bot.send(event=event, message=rj)
        await asyncio.sleep(b_sleep_time)
