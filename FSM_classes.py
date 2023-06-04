from aiogram.dispatcher.filters.state import StatesGroup, State

class mainMenu(StatesGroup):
    mainMenu = State()
    mainMenuStart = State()

class registration(StatesGroup):
    startReg = State()
    password = State()

class login(StatesGroup):
    startLogin = State()
    password = State()
    unLogin = State()

class menu(StatesGroup):
    menuStart = State()
    fourCheeses = State()
    philadelphiaChicken = State()
    vegetarian = State()
    florentina = State()
    philadelphiaCheese = State()
    jalapenoBBQ = State()
    supreme = State()
    meatMadness = State()
    hawaiiBBQ = State()
    addToCart = State()
    makeAnOrder = State()
    orderComplete = State()