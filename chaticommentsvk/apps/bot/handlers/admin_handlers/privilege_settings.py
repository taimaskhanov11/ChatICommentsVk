from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from chaticommentsvk.apps.bot import markups
from chaticommentsvk.apps.bot.utils.admin_helpers import admin_vips_status
from chaticommentsvk.config.config import config


class AdminSetStatesGroup(StatesGroup):
    add = State()
    delete = State()


class VipSetStatesGroup(StatesGroup):
    add = State()
    delete = State()


async def privilege_settings(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(admin_vips_status(), reply_markup=markups.privilege_menu)


async def add_admin(call: types.CallbackQuery):
    await call.message.answer("Введите ID админа для добавления")
    await AdminSetStatesGroup.add.set()


async def delete_admin(call: types.CallbackQuery):
    await call.message.answer("Введите ID админа для удаления")
    await AdminSetStatesGroup.delete.set()


async def add_vip(call: types.CallbackQuery):
    await call.message.answer("Введите ID vip для добавления")
    await VipSetStatesGroup.add.set()


async def delete_vip(call: types.CallbackQuery):
    await call.message.answer("Введите ID vip для удаления")
    await VipSetStatesGroup.delete.set()


async def add_admin_end(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        config.bot.admins.append(int(message.text))
        await message.answer(f"Админ {message.text} успешно добавлен")
    await state.finish()


async def delete_admin_end(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        ui = int(message.text)
        if ui in config.bot.admins:
            config.bot.admins.remove(ui)
        await message.answer(f"Админ {message.text} успешно удален")
    await state.finish()


async def add_vip_end(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        config.bot.vip.append(int(message.text))
        await message.answer(f"Vip {message.text} успешно добавлен")
    await state.finish()


async def delete_vip_end(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        ui = int(message.text)
        if ui in config.bot.vip:
            config.bot.vip.remove(ui)
        await message.answer(f"Vip {message.text} успешно удален")
    await state.finish()


def register_privilege_handlers(dp: Dispatcher):
    dp.register_message_handler(privilege_settings, text_startswith="👥", state="*")

    dp.register_callback_query_handler(add_admin, text="add_admin")
    dp.register_callback_query_handler(delete_admin, text="delete_admin")
    dp.register_callback_query_handler(add_vip, text="add_vip")
    dp.register_callback_query_handler(delete_vip, text="delete_vip")

    dp.register_message_handler(add_admin_end, state=AdminSetStatesGroup.add)
    dp.register_message_handler(delete_admin_end, state=AdminSetStatesGroup.delete)
    dp.register_message_handler(add_vip_end, state=VipSetStatesGroup.add)
    dp.register_message_handler(delete_vip_end, state=VipSetStatesGroup.delete)
