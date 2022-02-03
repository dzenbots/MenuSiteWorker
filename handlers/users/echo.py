from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state="*",
                    content_types=types.ContentTypes.ANY,
                    is_admin=True,
                    chat_type='private')
async def bot_echo(message: types.Message):
    await message.answer(f"Воспользуйтесь командами из меню или дождитесь уведомления")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*",
                    content_types=types.ContentTypes.ANY,
                    chat_type='private'
                    )
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    await message.answer(f"Только администратор может управлять ботом")
