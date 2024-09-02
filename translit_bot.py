# 1.Импорт библиотек
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message             # ловим все обновления этого типа
from aiogram.filters.command import Command   # обрабатываем команды /start, /help и другие
from transliterate import translit

# 2. Инициализация объектов
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)                        # Создаем объект бота
dp = Dispatcher()                             # Создаем объект диспетчера. Все хэндлеры(обработчики) должны быть подключены к диспетчеру
logging.basicConfig(level=logging.INFO, filename = "mylog.log")

# Домашнее Задание
# - Включить запись log в файл
# - Бот принимает кириллицу отдаёт латиницу в соответствии с Приказом МИД по транслитерации
# - Бот работает из-под docker контейнера

# 3. Обработка/Хэндлер на команду /start
@dp.message(Command(commands=['start']))
async def proccess_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Привет, {user_name}! Напиши свои ФИО на кириллице.'
    logging.info(f'{user_name} {user_id} запустил бота')
    await bot.send_message(chat_id=user_id, text=text)


# 4. Обработка/Хэндлер на любые сообщения
@dp.message()
async def send_translit(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text
    logging.info(f'{user_name} {user_id}: {text}')
    try:
        transliterated = translit(text, 'ru', reversed=True)
        await message.answer(text=transliterated)
    except Exception as e:
        await message.answer(text=f"Проверьте данные: {str(e)}")


# 5. Запуск процесса пуллинга
if __name__ == '__main__':
    dp.run_polling(bot)