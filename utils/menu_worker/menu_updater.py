from aiogram import Dispatcher

from utils.menu_worker.site_worker import SiteWorker


def update_tomorrow(dp: Dispatcher):
    sw = SiteWorker(site_auth=dp.bot.get('config').misc.school_auth,
                    folder_paths=dp.bot.get('config').misc.files_paths)
    # TODO: code here!


def update_today(dp: Dispatcher):
    sw = SiteWorker(site_auth=dp.bot.get('config').misc.school_auth,
                    folder_paths=dp.bot.get('config').misc.files_paths)
    sw.copy_tomorrow_today()
