#Тут работа с кнопками
from telebot import types

#Функция отправки номера
def num_but():
    #Создаем пространство для кнопок
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #Создать кнопку
    num = types.KeyboardButton('Отправить номер', request_contact=True)
    #Добавить кнопку в пространство
    kb.add(num)
    return kb

#Функция отправки локации
def loc_button():
    # Создаем пространство для кнопок
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #Создаем кнопку
    loc = types.KeyboardButton('Отправить локацию', request_location=True)
    #Добавить кнопку в пространство
    kb.add(loc)
    return kb

##Кнопки для админки##
#Меню админки
def admin_menu():
    #Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #Создаем кнопки
    but1 = types.KeyboardButton('Добавить продукт')
    but2 = types.KeyboardButton('Удалить продукт')
    #Добавить кнопку в пространство
    kb.add(but1, but2)
    return kb

#Кнопки потверждения удаления продукта
def confirm():
    # Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаем кнопки
    but1 = types.KeyboardButton('Да')
    but2 = types.KeyboardButton('Нет')
    # Добавить кнопку в пространство
    kb.add(but1, but2)
    return kb

##Прописываем Inline кнопки##
#Кнопка главного меню
def main_menu(prods_from_db):
    #Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)
    #Создаем кнопки, которые будут всегда
    cart = types.InlineKeyboardButton(text='Корзина', callback_data='cart')
    #Создаем кнопки с продуктами
    all_products = [types.InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}')
                    for i in prods_from_db]
    #Добавление кнопок в пространство
    kb.add(*all_products)
    kb.row(cart)

    return kb

#Кнопки выбора количества товара
def choose_product_count(amount=1, plus_or_minus=''):
    #Создание пространства
    kb = types.InlineKeyboardMarkup(row_width=3)

    #Создаем сами кнопки
    back = types.InlineKeyboardButton(text='В главное меню', callback_data='back')
    to_cart = types.InlineKeyboardButton(text='В корзину', callback_data='to_cart')
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    count = types.InlineKeyboardButton(text=str(amount), callback_data=str(amount))

    #Алгоритм добавления и удаления одного товара
    if plus_or_minus == 'increment':
        new_amount = int(amount) + 1
        count = types.InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))
    elif plus_or_minus == 'decrement':
        if amount > 1:
            new_amount = int(amount) - 1
            count = types.InlineKeyboardButton(text=str(new_amount), callback_data=str(new_amount))

    #Добавляем кнопки в пространство
    kb.add(minus, count, plus)
    kb.row(to_cart)
    kb.row(back)

    return kb

#Кнопки корзины
def cart_buttons():
    #Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=2)

    #Создаем сами кнопки
    order = types.InlineKeyboardButton(text='Оформить заказ', callback_data='order')
    clear = types.InlineKeyboardButton(text='Очистить корзину', callback_data='clear')
    back = types.InlineKeyboardButton(text='На главную', callback_data='back')

    #Добавить кнопки в пространство
    kb.add(order, clear)
    kb.row(back)

    return kb