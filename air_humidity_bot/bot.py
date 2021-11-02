import logging
import os
import re
from asyncio import sleep

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base

from air_humidity_bot import keyboard_markup
from air_humidity_bot.add_to_history import add_history
from air_humidity_bot.delete_history import delete_history, Delete
from air_humidity_bot.get_humidity import get_humidity
from air_humidity_bot.main_for_database import main_for_database
from air_humidity_bot.show_history import get_history
from air_humidity_bot.states_value import Value

load_dotenv()

token = os.getenv('token_from_botfather')

storage = MemoryStorage()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply('🥳')
    await sleep(3)
    await message.answer(f'Nice to meet you, {message.from_user.first_name}! 🪴 \n'
                         f'🚖  let`s try to calculate air humidity in your room! '
                         f'do you have a VIT-1 or VIT-2 device? 🌡🌡 (like the ones on the photo)')
    await sleep(3)
    await bot.send_photo(message.chat.id, photo=open('air_humidity_bot/images/hygrometers_which_are_needed.jpg', 'rb'))
    await sleep(2)
    await message.answer(f'Check the data of your hygrometer and choose a command\n'
                         f'/get_humidity\n')
    await sleep(3)
    await message.answer('you can use other commands in the menu below if needed 🛰',
                         reply_markup=keyboard_markup.hotKeys)


@dp.message_handler(commands=['about_me'])
@dp.message_handler(lambda message: message.text == 'about me 🙈')
async def send_about(message: types.Message):
    """
    This handler will be called when user sends `/about_me` command
    """
    await message.reply('🚀 \n'
                        'I`ll came up to make easier the calculation of air humidity into your room, \n'
                        'according to the readings data of VIT-1,2 devices. \n'
                        'The VIT-1, VIT-2 devices are hygrometers. \n'
                        'I`ll return the value of current relative humidity of air in the room,\n'
                        'after receiving the data of dry and wet-bulb thermometers from you🌡🌡\n')
    await sleep(2)
    await message.answer('let`s choose a command `/get_humidity`')


@dp.message_handler(commands=['help'])
@dp.message_handler(lambda message: message.text == 'help 🧐')
async def send_help(message: types.Message):
    """
    This handler will be called when user sends `/help` command
    """
    await message.reply(' - Please, check the data for mistakes (example, unexpected character or symbol) \n'
                        ' - Also check the limits of entered data - it should be from 5°C to 40°C \n'
                        ' - If you mix up values of dry and wet-bulb thermometer, don`t worry! I`ll put it right 😉 \n')


@dp.message_handler(commands=['get_humidity'], state=None)
@dp.message_handler(lambda message: message.text == 'get humidity 🌡🌡', state=None)
async def data_temp_dry(message: types.Message):
    await message.answer('enter data of DRY thermometer: ')
    # send a response to class Value
    await Value.temp_dry.set()


# state=Value.temp_dry handle the received value of the dry thermometer
@dp.message_handler(state=Value.temp_dry)
async def data_temp_wet(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(temp_dry=answer)
    await message.answer('enter data of WET thermometer: ')

    await Value.next()


# state=Value.temp_wet handle received value of the wet thermometer
@dp.message_handler(state=Value.temp_wet)
async def validate_data_dry_wet(message: types.Message, state: FSMContext):
    data = await state.get_data()
    temp_dry = data.get('temp_dry')
    temp_wet = message.text

    # replace ',' -> '.'
    temp_dry = temp_dry.replace(',', '.', 1)
    temp_wet = temp_wet.replace(',', '.', 1)

    # remove all, except -> [0-9] & '.'
    pattern_numeric_dot = re.compile(r'[^0-9.]')
    temp_dry = pattern_numeric_dot.sub('', temp_dry)
    temp_wet = pattern_numeric_dot.sub('', temp_wet)

    try:
        temp_dry = float(temp_dry)
        temp_wet = float(temp_wet)

        if temp_dry <= 4 or temp_dry >= 41 or temp_wet <= 4 or temp_wet >= 41:
            await message.answer('Oh no... \nthis data is totally out of my scope 🚀 sorry, bro!')
            await message.answer('Check the data for mistakes and try again 🤓 ')
        else:
            if temp_wet > temp_dry:
                temp_wet, temp_dry = temp_dry, temp_wet

            delta_temp = temp_dry - temp_wet

            humidity = get_humidity(temp_dry, delta_temp)
            # humidity = '...temporarily unavailable...'

            # round data
            temp_dry = round(temp_dry, 1)
            temp_wet = round(temp_wet, 1)
            # function from air_humidity_bot.add_to_history import add_history
            await message.answer(add_history(message.from_user.id,
                                             message.from_user.first_name,
                                             message.from_user.username,
                                             temp_dry,
                                             temp_wet,
                                             humidity))

            await message.answer(f'📝 for your data: \n'
                                 f'data of dry thermometer: +{temp_dry} °C\n'
                                 f'data of wet thermometer: +{temp_wet} °C\n'
                                 f'humidity is {humidity}')
    except ValueError:
        await message.answer('Sorry, I can`t help you! Please enter only digits...\n'
                             'or use command `/help`')

    await state.reset_state(with_data=False)


@dp.message_handler(commands=['show_history'])
@dp.message_handler(lambda message: message.text == 'show history 📝')
async def show_history(message: types.Message):
    """
    This handler will be called when user sends `/show_history` command
    """
    user_id = message.from_user.id
    # get_history(user_id)
    await message.reply(f'history for @{message.from_user.username} 📝\n'
                        # function from show_history import get_history
                        f'{get_history(user_id)}')


@dp.message_handler(commands=['delete_my_history'], state=None)
@dp.message_handler(lambda message: message.text == 'remove all your requests 🗑', state=None)
async def delete_history_request(message: types.Message):
    await message.answer(f'😱 {message.from_user.first_name}, are you sure?\n'
                         f'type `yes` to confirm. \n'
                         f'Or `no` if you change your mind ')
    # send a response to class Delete
    await Delete.confirm_deletion.set()


# state=Delete.confirm_deletion handle the received value of confirm deletion
@dp.message_handler(state=Delete.confirm_deletion)
async def delete_history_confirm(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    answer = message.text
    await state.update_data(confirm_deletion=answer)
    if answer.lower() == 'yes':
        await message.reply(f'{delete_history(user_id)}')
    elif answer.lower() == 'no':
        await message.reply('Great! I`m keeping it 🔒')
    else:
        await message.reply('Don`t understand 😐 try again')
    await state.reset_state(with_data=False)


@dp.message_handler()
async def text(message: types.Message):
    await message.answer('I can`t answer... 🤫')
    await message.answer('select a command and I`ll help you!')


def main():
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    Base = declarative_base()
    main_for_database()
    main()
