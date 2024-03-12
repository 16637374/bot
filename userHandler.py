
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import  FSMContext
from aiogram import Bot
from helperAI import get_ai_image,get_ai_text
from settings import CHANNEL_ID
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup,State

class UserState(StatesGroup):
    CONVERSATION = State()
    IMAGE = State()
    
async def start_user(message : Message, state: FSMContext, bot : Bot):
    await bot.send_message(chat_id=message.from_user.id,
                           text = f'Добро пожаловать, {message.from_user.first_name} ',
                           reply_markup=await main_menu())
    
    await state.set_state(None)

async def menu(message : Message,bot : Bot):
        await bot.send_message(chat_id=message.from_user.id,
                           text = f'Главное меню. ',
                           reply_markup=await main_menu())

async def cancel_chat(message : Message, state : FSMContext, bot : Bot):
    await state.set_state(None)
    await bot.send_message(chat_id=message.from_user.id,text ='Диалог прекращен', reply_markup= await main_menu())

async def start_conversation(call : CallbackQuery, state : FSMContext, bot : Bot):
    await state.set_state(UserState.CONVERSATION)
    await bot.send_message(chat_id=call.from_user.id,text='Напишите ваш текст.'
                            'Для выхода из диалога напишите /cancel')

async def start_create_image(call : CallbackQuery, state : FSMContext, bot : Bot):    
    await state.set_state(UserState.IMAGE)
    await bot.send_message(chat_id=call.from_user.id,text='Напишите ваш запрос для создания изображения.'
                            'Для выхода напишите /cancel')

async def send_message_to_ai(message : Message, bot : Bot):
    messages = []
    messages.append({"role": "user", "content": message.text})
    ai_response = await get_ai_text(messages=messages)
    await bot.send_message(chat_id=CHANNEL_ID, text= ai_response)
    await bot.send_message(chat_id=message.from_user.id, text= 'Текст отправлен в канал')


async def send_image_from_ai(message : Message, state : FSMContext, bot : Bot):
    ai_response = await get_ai_image(message.text)
    msg =await bot.send_message(chat_id=message.from_user.id, text= 'Идет подготовка изображений')
    await bot.send_photo(chat_id=CHANNEL_ID,photo=ai_response)
    bot.edit_message_text(message_id= msg.message_id, chat_id=message.from_user.id,text ='Изображение отправлено в канал')

async def main_menu():
    builder = InlineKeyboardBuilder() 
    builder.button(text=f'Генерация текста',callback_data=f'conversation_start')
    builder.button(text=f'Генерация картинки',callback_data=f'image_generation')
    keyboard = builder.as_markup()
    return keyboard

