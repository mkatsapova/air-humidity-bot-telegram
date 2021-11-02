from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_get_humidity = 'get humidity 🌡🌡'
button_show_history = 'show history 📝'
button_about_me = 'about me 🙈'
button_help = 'help 🧐'
button_remove_requests = 'remove all your requests 🗑'


# hotkeys only

btnGetHumidity = KeyboardButton(button_get_humidity)
btnShowHistory = KeyboardButton(button_show_history)
btnHowItWorks = KeyboardButton(button_about_me)
btnHelp = KeyboardButton(button_help)
btnDelete = KeyboardButton(button_remove_requests)
hotKeys = ReplyKeyboardMarkup(resize_keyboard=True).add(btnGetHumidity).add(btnShowHistory,
                                                                            btnDelete).add(btnHowItWorks, btnHelp)

