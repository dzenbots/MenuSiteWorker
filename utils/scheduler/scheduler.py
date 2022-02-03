import asyncio

import aioschedule
from aiogram import Dispatcher


async def send_replace_tomorrow_menu_notification(dp,
                                                  message='Обновить меню на завтра?'):
    for admin in dp.bot.get('config').tg_bot.admin_ids:
        await dp.bot.send_message(chat_id=admin,
                                  text=message,
                                  reply_markup=get_update_site_admin_keyboard())


async def send_replace_menu_notification(dp,
                                         message='Заменить сегодняшнее меню на завтрашнее?'):
    for admin in dp.bot.get('config').tg_bot.admin_ids:
        await dp.bot.send_message(chat_id=admin,
                                  text=message,
                                  reply_markup=get_replace_site_admin_keyboard())


async def scheduler(dp: Dispatcher):
    aioschedule.every().day.at(dp.bot.get('config').misc.scheduler.time_for_tomorrow).do(
        send_replace_tomorrow_menu_notification,
        dp=dp,
        message='Обновить меню на завтра?'
    )
    aioschedule.every().day.at(dp.bot.get('config').misc.scheduler.time_for_today).do(
        send_replace_menu_notification,
        dp=dp,
        message='Заменить сегодняшнее меню на завтрашнее?'
    )
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
