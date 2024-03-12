import asyncio
from aiogram import Bot, Dispatcher
from aiogram import Bot, Dispatcher, F
import logging
from aiogram.filters import Command
from core.utils.dbconnect import engine
from core.handlers import adminHandler,userHandler, payments
from core.utils.settings import BOT_TOKEN
from core.states.userState import UserState,AdminState

    


async def start():  
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
    bot = Bot(token = BOT_TOKEN)
    dp = Dispatcher()
    dp.message.register(userHandler.start_user, Command('start'))
    dp.message.register(userHandler.cancel_chat, Command('cancel'))
    dp.message.register(userHandler.clear_chat, Command('clear'))
    dp.message.register(userHandler.menu, Command('menu'))
    dp.message.register(payments.successful_payment, F.successful_payment)
    dp.message.register(userHandler.send_message_to_ai, UserState.CONVERSATION)
    dp.message.register(userHandler.send_image_from_ai, UserState.IMAGE)
    dp.callback_query.register(userHandler.send_image_from_ai, F.data.startswith('count:'))

    # dp.chat_join_request.register(botAction.closed_group_join_request)
    dp.callback_query.register(userHandler.start_conversation, F.data == 'conversation_start')
    dp.callback_query.register(userHandler.start_create_image, F.data == 'image_generation')
    dp.callback_query.register(userHandler.send_profile, F.data == 'profile')
    dp.callback_query.register(payments.create_payment, F.data == 'sub_create')
    dp.callback_query.register(adminHandler.admin_menu, F.data == 'admin_menu')
    dp.callback_query.register(userHandler.menu, F.data == 'menu')
    dp.callback_query.register(adminHandler.set_price, F.data == 'change_price')
    dp.callback_query.register(adminHandler.set_keys, F.data == 'add_keys')

    dp.pre_checkout_query.register(payments.process_pre_checkout_query)


    try:
        await dp.start_polling(bot,skip_updates=True)
    finally:
        await bot.session.close()

if  __name__ == '__main__':
    asyncio.run(start())