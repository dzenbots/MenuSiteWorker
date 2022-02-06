from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

site_admin_callbacks = CallbackData('Site_admin', 'function')


def get_menu_notification_inline_kb(target: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='✅ Обновить',
                    callback_data=site_admin_callbacks.new(
                        function=target
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text='❌ Отмена',
                    callback_data=site_admin_callbacks.new(
                        function='cancel'
                    )
                )
            ]
        ]
    )

