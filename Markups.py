from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


toMainMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Главное меню'))


makeAnOrder = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Сделать заказ'),
    KeyboardButton('Очистить корзину'),
    KeyboardButton('Главное меню'))


mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Зарегистрироваться'),
    KeyboardButton('Войти в аккаунт'),
    KeyboardButton('Посмотреть меню'),
    KeyboardButton('Посмотреть корзину'))

unLogin = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Выйти из аккаунта'),
    KeyboardButton('Главное меню'))



menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).add(
    KeyboardButton('Четыре сыра'),
    KeyboardButton('Цыпленок филадельфия'),
    KeyboardButton('Вегетарианская'),
    KeyboardButton('Флорентина'),
    KeyboardButton('Филадельфия чиз'),
    KeyboardButton('Халапенью BBQ'),
    KeyboardButton('Суприм'),
    KeyboardButton('Мясное безумие'),
    KeyboardButton('Гавайи BBQ'))

backToMenu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Посмотреть меню'))

pizzaMarkup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    KeyboardButton('Добавить в корзину'),
    KeyboardButton('Главное меню'))
