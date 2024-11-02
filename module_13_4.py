# Машина состояний
# Задача "Цепочка вопросов"

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


api = '759'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()   # Состояние ожидания ввода возраста
    growth = State()    # Состояние ожидания ввода роста
    weight = State()    # Состояние ожидания ввода веса

@dp.message_handler(commands = ['start'])
async def start_(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message_handler(text = ['Calories'])   # 1
async def set_age(message):                  # Возраст
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)     # 2
async def set_growth(message, state):       # Рост
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)      # 3
async def set_weight(message, state):                  # Вес
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)      # 4
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['weight'])) + (6.25 * float(data['growth'])) - (5 * int(data['age'])) - 161
    await message.answer(f"Ваша норма каллорий {result}")
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

