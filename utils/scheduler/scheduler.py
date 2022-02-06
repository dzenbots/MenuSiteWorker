import asyncio

import aioschedule
from aiogram import Dispatcher

from keyboards.inline.menu_notification import get_menu_notification_inline_kb


async def update_tomorrow_menu(dp,
                               message='Обновить завтрашнее меню?'):
    for admin in dp.bot.get('config').tg_bot.admin_ids:
        await dp.bot.send_message(chat_id=admin,
                                  text=message,
                                  reply_markup=get_menu_notification_inline_kb(target='update_tomorrow'))


async def update_today_menu(dp,
                            message='Обновить сегодняшнее меню?'):
    for admin in dp.bot.get('config').tg_bot.admin_ids:
        await dp.bot.send_message(chat_id=admin,
                                  text=message,
                                  reply_markup=get_menu_notification_inline_kb(target='update_today'))


async def scheduler(dp: Dispatcher):
    aioschedule.every().day.at(dp.bot.get('config').misc.scheduler.time_for_tomorrow).do(
        update_tomorrow_menu,
        dp=dp,
        message='Обновить меню на завтра?'
    )
    aioschedule.every().day.at(dp.bot.get('config').misc.scheduler.time_for_today).do(
        update_today_menu,
        dp=dp,
        message='Заменить сегодняшнее меню на завтрашнее?'
    )
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
