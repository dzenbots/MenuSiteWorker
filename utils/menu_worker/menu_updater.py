from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from utils.menu_worker.site_worker import SiteWorker


def update_tomorrow(call: CallbackQuery, dp: Dispatcher):
    pass


def update_today(dp: Dispatcher):
    sw = SiteWorker(site_auth=dp.bot.get('config').misc.school_auth,
                    folder_paths=dp.bot.get('config').misc.files_paths)
    sw.copy_tomorrow_today()
