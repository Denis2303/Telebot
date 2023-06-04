from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType, File, Message
from aiogram.types.input_file import InputFile
import Markups
import FSM_classes
import sqlite3
import databases


bot = Bot(token="5927437955:AAHFbLpOXRjyFTzwElB_0d0d_85Y3sjmv1g")
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    await message.reply(
        "Добро пожаловать в нашу пиццерию!",
        reply_markup=Markups.toMainMenu)
    await FSM_classes.mainMenu.mainMenu.set()


@dp.message_handler(state=FSM_classes.mainMenu.mainMenu)
async def main_menu(message: types.Message, state: FSMContext):
    await bot.send_message(text="Добро пожаловать в главное меню! Что бы вы хотели сделать?\n"
                                "Что вы хотите сделать?\n"
                                "Зарегистрироваться\n"
                                "Войти в аккаунт\n"
                                "Посмотреть меню\n"
                                "Посмотреть свою корзину", reply_markup=Markups.mainMenu,chat_id=message.from_user.id)
    await FSM_classes.mainMenu.mainMenuStart.set()


@dp.message_handler(state=FSM_classes.mainMenu.mainMenuStart)
async def main_menu(message: types.Message, state: FSMContext):
    if message.text == 'Зарегистрироваться':
        await bot.send_message(chat_id=message.from_user.id, text='Введите свой телефон')
        await FSM_classes.registration.startReg.set()
    elif message.text == 'Войти в аккаунт':
        await bot.send_message(chat_id=message.from_user.id, text='Введите свой телефон')
        await FSM_classes.login.startLogin.set()
    elif message.text == 'Посмотреть меню':
        await bot.send_message(chat_id=message.from_user.id, text='Наше меню:\n'
                                                                  'Четыре сыра\n'
                                                                  'Цыпленок филадельфия\n'
                                                                  'Вегетарианская\n'
                                                                  'Флорентина\n'
                                                                  'Филадельфия чиз\n'
                                                                  'Халапенью BBQ\n'
                                                                  'Суприм\n'
                                                                  'Мясное безумие\n'
                                                                  'Гавайи BBQ',reply_markup=Markups.menu)
        await FSM_classes.menu.menuStart.set()
    elif message.text == 'Посмотреть корзину':
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE authorized = ?", (message.from_user.id,))
        result = cur.fetchone()[0]
        if result > 0:
            pizzas = 'Содержимое вашей корзины:\n'
            try:
                cartSize = cur.execute("SELECT cartSize FROM userCarts WHERE user_id = ?", (message.from_user.id,)).fetchone()[0]

                for i in range(cartSize):
                    pizzaName = cur.execute(f"SELECT pos_{i+1} FROM userCarts WHERE user_id = ?", (message.from_user.id,)).fetchone()[0]
                    pizzas = pizzas + f'{pizzaName}\n'
                await bot.send_message(chat_id=message.from_user.id,reply_markup=Markups.makeAnOrder,text=pizzas)
                await FSM_classes.menu.makeAnOrder.set()
            except TypeError:
                await bot.send_message(chat_id=message.from_user.id, reply_markup=Markups.toMainMenu,
                                       text='Ваша корзина пуста')
                await FSM_classes.mainMenu.mainMenu.set()
        else:
            await bot.send_message(chat_id=message.from_user.id,reply_markup=Markups.toMainMenu,text='Для использования этой функции нужно авторизироваться')
            await FSM_classes.mainMenu.mainMenu.set()


@dp.message_handler(state=FSM_classes.menu.makeAnOrder)
async def makeAnOrder(message: types.Message, state: FSMContext):
    if message.text == 'Сделать заказ':
        await bot.send_message(chat_id=message.from_user.id,text='Введите ваш адрес')
        await FSM_classes.menu.orderComplete.set()
    elif message.text == 'Очистить корзину':
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM userCarts WHERE user_id = ?", (message.from_user.id,))
        conn.commit()
        await bot.send_message(text='Корзина успешно очищена!',chat_id=message.from_user.id,reply_markup=Markups.toMainMenu)
        await FSM_classes.mainMenu.mainMenu.set()
    else:
        await bot.send_message(text='Вернуться в меню',chat_id=message.from_user.id,reply_markup=Markups.toMainMenu)
        await FSM_classes.mainMenu.mainMenu.set()


@dp.message_handler(state=FSM_classes.menu.orderComplete)
async def orderComplete(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    curDiscount = cur.execute('SELECT discount FROM users WHERE user_id = ?',(message.from_user.id,)).fetchone()[0]
    if curDiscount < 20:
        cur.execute("UPDATE users SET discount = discount + 1 WHERE user_id = ?",(message.from_user.id,))
        curDiscount+=1
    pizzas = ''
    cartSize = cur.execute("SELECT cartSize FROM userCarts WHERE user_id = ?", (message.from_user.id,)).fetchone()[0]

    for i in range(cartSize):
        pizzaName = \
        cur.execute(f"SELECT pos_{i + 1} FROM userCarts WHERE user_id = ?", (message.from_user.id,)).fetchone()[0]
        pizzas = pizzas + f'{pizzaName}\n'
    number = cur.execute("SELECT number FROM users WHERE user_id = ?",(message.from_user.id,)).fetchone()[0]
    await bot.send_message(text=f'Ваш заказ успешно принят!\n'
                                f'На ваш аккаунт зачислена скидка в 1%. Текущая скидка {curDiscount}%!',chat_id=message.from_user.id,reply_markup=Markups.toMainMenu)
    await bot.send_message(chat_id=740675354,text=f'Пользователь с номером телефона {number} сделал заказ по адресу {message.text}\n'
                                                  f'Содержание заказа:\n'
                                                  f'{pizzas}')
    cur.execute("DELETE FROM userCarts WHERE user_id = ?", (message.from_user.id,))
    conn.commit()
    await FSM_classes.mainMenu.mainMenu.set()


@dp.message_handler(state=FSM_classes.menu.menuStart)
async def menu(message: types.Message, state: FSMContext):
    if message.text == 'Четыре сыра':
        with open('pizzaPhotos/fourCheeses.jpg', 'rb') as photo:
            await bot.send_photo(reply_markup=Markups.pizzaMarkup, chat_id=message.from_user.id, photo=photo, caption='Томатный соус, базилик, сыр моцарелла, сливочный сыр, сыр пармезан, сыр с благородной плесенью, итальянские травы.')
            await state.set_data({"pizza": message.text})
            await FSM_classes.menu.addToCart.set()
    elif message.text == 'Цыпленок филадельфия':
        with open('pizzaPhotos/philadelphiaChicken.jpg', 'rb') as photo:
            await bot.send_photo(reply_markup=Markups.pizzaMarkup, chat_id=message.from_user.id, photo=photo, caption='Сливочный сыр, петрушка, сыр пармезан, красный лук, сыр моцарелла, филе цыплёнка, бекон, черри, чеснок.')
            await state.set_data({"pizza": message.text})
            await FSM_classes.menu.addToCart.set()
    elif message.text == 'Вегетарианская':
        with open('pizzaPhotos/vegetarian.jpg', 'rb') as photo:
            await bot.send_photo(reply_markup=Markups.pizzaMarkup, chat_id=message.from_user.id, photo=photo, caption='Сливочный сыр, петрушка, красный лук, сыр моцарелла, свежие шампиньоны, сладкий зелёный перец, маслины, томаты.')
            await state.set_data({"pizza": message.text})
            await FSM_classes.menu.addToCart.set()
    elif message.text == 'Флорентина':
        with open('pizzaPhotos/florentina.jpg', 'rb') as photo:
            await bot.send_photo(reply_markup=Markups.pizzaMarkup, chat_id=message.from_user.id, photo=photo, caption='Чесночный соус ранч, сыр пармезан, филе цыплёнка, хрустящий бекон, томаты Черри, запечённый шпинат, итальянские травы, сыр моцарелла.')
            await state.set_data({"pizza": message.text})
            await FSM_classes.menu.addToCart.set()
    elif message.text == 'Филадельфия чиз':
        with open('pizzaPhotos/philadelphiaCheese.jpg', 'rb') as photo:
            await bot.send_photo(reply_markup=Markups.pizzaMarkup, chat_id=message.from_user.id, photo=photo, caption='Сыр чеддер, говядина, красный лук, сыр моцарелла, сладких зелёный перец, свежие шампиньоны, сыр пармезан.')
            await state.set_data({"pizza": message.text})
            await FSM_classes.menu.addToCart.set()
    elif message.text == 'Халапенью BBQ':
        with open('pizzaPhotos/jalapenoBBQ.jpg', 'rb') as photo:
            await bot.send_photo(reply_markup=Markups.pizzaMarkup, chat_id=message.from_user.id, photo=photo, caption='Томатный соус, сыр моцарелла, филе цыплёнка, хрустящий бекон, красный лук, ананас, перчики халапеньо, соус барбекю.')
            await state.set_data({"pizza": message.text})
            await FSM_classes.menu.addToCart.set()
    elif message.text == 'Суприм':
        with open('pizzaPhotos/supreme.jpg', 'rb') as photo:
            await bot.send_photo(reply_markup=Markups.pizzaMarkup, chat_id=message.from_user.id, photo=photo, caption='Томатный соус, сыр моцарелла, колбаски пепперони, свежие шампиньоны, красный лук, маслины, хрустящие бекон, Сладких зелёный перец, говядина')
            await state.set_data({"pizza": message.text})
            await FSM_classes.menu.addToCart.set()
    elif message.text == 'Мясное безумие':
        with open('pizzaPhotos/meatMadness.jpg', 'rb') as photo:
            await bot.send_photo(reply_markup=Markups.pizzaMarkup, chat_id=message.from_user.id, photo=photo, caption='Томатный соус, сыр моцарелла, говядина, цыплёнок, ветчина, пикантной колбаски пепперони, колбаски чоризо')
            await state.set_data({"pizza": message.text})
            await FSM_classes.menu.addToCart.set()
    elif message.text == 'Гавайи BBQ':
        with open('pizzaPhotos/hawaiiBBQ.jpg', 'rb') as photo:
            await bot.send_photo(reply_markup=Markups.pizzaMarkup, chat_id=message.from_user.id, photo=photo, caption='Барбекю соус, сыр моцарелла, филе цыплёнка, хрустящий бекон, красный лук, ананасы.')
            await state.set_data({"pizza": message.text})
            await FSM_classes.menu.addToCart.set()

@dp.message_handler(state=FSM_classes.menu.addToCart)
async def addToCart(message: types.Message, state: FSMContext):
    if message.text == 'Добавить в корзину':
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users WHERE authorized = ?", (message.from_user.id,))
        result = cur.fetchone()[0]
        if result > 0:
            pizzaName = await state.get_data('pizza')
            pizzaName = pizzaName['pizza']
            await databases.preUserCarts(message.from_user.id)
            cartSize = cur.execute("SELECT cartSize FROM userCarts WHERE user_id = ?",(message.from_user.id,)).fetchone()[0]
            cur.execute("PRAGMA table_info(userCarts)")
            columns = [column[1] for column in cur.fetchall()]
            columnName = f'pos_{cartSize + 1}'
            if columnName not in columns:
                cur.execute(f"ALTER TABLE userCarts ADD COLUMN {columnName} TEXT")
            cur.execute(f"UPDATE userCarts SET {columnName} = ? WHERE user_id = ?",(pizzaName,message.from_user.id))
            cur.execute("UPDATE userCarts SET cartSize = cartSize + 1 WHERE user_id = ?",(message.from_user.id,))
            conn.commit()
            await bot.send_message(chat_id=message.from_user.id,reply_markup=Markups.backToMenu, text='Пицца успешно добавлена!')
            await FSM_classes.mainMenu.mainMenu.set()
        else:
            await bot.send_message(chat_id=message.from_user.id,reply_markup=Markups.toMainMenu, text='Сначала авторизуйтесь в аккаунте')
            await FSM_classes.mainMenu.mainMenu.set()
    else:
        await bot.send_message(chat_id=message.from_user.id, reply_markup=Markups.toMainMenu,
                               text='Вернуться в меню')
        await FSM_classes.mainMenu.mainMenu.set()



@dp.message_handler(state=FSM_classes.registration.startReg)
async def reg(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE number = ?", (message.text,))
    result = cur.fetchone()[0]
    if result > 0:
        await bot.send_message(chat_id=message.from_user.id, text='Пользователь с таким номером уже существует',reply_markup=Markups.toMainMenu)
        await FSM_classes.mainMenu.mainMenu.set()
    else:
        await databases.preRegdb(message.from_user.id,message.text)
        await bot.send_message(chat_id=message.from_user.id, text='Придумайте пароль.')
        await FSM_classes.registration.password.set()


@dp.message_handler(state=FSM_classes.registration.password)
async def regPassword(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("UPDATE users SET password = ? WHERE user_id = ?",(message.text,message.from_user.id))
    conn.commit()
    await bot.send_message(text='Вы успешно зарегистрировались!',chat_id=message.from_user.id,reply_markup=Markups.toMainMenu)
    await FSM_classes.mainMenu.mainMenu.set()


@dp.message_handler(state=FSM_classes.login.startLogin)
async def loginStart(message: types.Message, state: FSMContext):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE number = ?", (message.text,))
    result = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM users WHERE authorized = ? ", (message.from_user.id,))
    loggened = cur.fetchone()[0]
    if loggened > 0:
        await bot.send_message(text='Вы уже авторизованы!\n'
                                    'Хотите выйти из аккаунта?', chat_id=message.from_user.id,reply_markup=Markups.unLogin)
        await FSM_classes.login.unLogin.set()
    else:
        if result > 0:
            await bot.send_message(text='Введите пароль',chat_id=message.from_user.id)
            await state.set_data({"number": message.text})
            await FSM_classes.login.password.set()
        else:
            await bot.send_message(text='Пользователь с таким номером не зарегестрирован\n'
                                        'Вернутся в меню?',chat_id=message.from_user.id,reply_markup=Markups.toMainMenu)
            await FSM_classes.mainMenu.mainMenu.set()


@dp.message_handler(state=FSM_classes.login.unLogin)
async def unLogin(message: types.Message, state: FSMContext):
    if message.text == 'Выйти из аккаунта':
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("UPDATE users SET authorized = 0 WHERE authorized = ?",(message.from_user.id,))
        conn.commit()
        await bot.send_message(text='Вы успешно вышли из аккаунта!',chat_id=message.from_user.id,reply_markup=Markups.toMainMenu)
        await FSM_classes.mainMenu.mainMenu.set()
    else:
        await bot.send_message(text='Вернуться в меню?', chat_id=message.from_user.id, reply_markup=Markups.toMainMenu)
        await FSM_classes.mainMenu.mainMenu.set()

@dp.message_handler(state=FSM_classes.login.password)
async def loginPassword(message: types.Message, state: FSMContext):
    number = await state.get_data("number")
    number = number['number']
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    password = cur.execute("SELECT password FROM users WHERE number = ?", (number,)).fetchone()
    if password[0] == message.text:
        cur.execute('UPDATE users SET authorized = ? WHERE number = ?',(message.from_user.id,number))
        conn.commit()
        await bot.send_message(text='Вы успешно авторизовались!',reply_markup=Markups.toMainMenu,chat_id=message.from_user.id)
        await FSM_classes.mainMenu.mainMenu.set()
    else:
        await bot.send_message(text='Не правильный пароль!', reply_markup=Markups.toMainMenu,
                               chat_id=message.from_user.id)
        await FSM_classes.mainMenu.mainMenu.set()



if __name__ == "__main__":
    print("Starting bot...")
    executor.start_polling(dp, skip_updates=True)