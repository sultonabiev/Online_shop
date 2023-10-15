#Тут работа с БД
import sqlite3

#Подключение к базе данных
connection = sqlite3.connect('delivery.db', check_same_thread=False)
#Связь SQL Python
sql = connection.cursor()

#Создание таблицы пользователей
sql.execute('CREATE TABLE IF NOT EXISTS users'
            '(id INTEGER, name TEXT, number TEXT, loc TEXT);')
#Создание таблицы продуктов
sql.execute('CREATE TABLE IF NOT EXISTS products'
            '(id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'pr_name TEXT, pr_des TEXT, pr_count INTEGER, pr_price REAL,'
            'pr_photo TEXT);')
#Создание таблицы корзины
sql.execute('CREATE TABLE IF NOT EXISTS cart'
            '(user_id INTEGER, user_product TEXT, product_quantity INTEGER,'
            'total REAL);')

##Методы для пользователя##
#Регистрация
def register(id, name, num, loc):
    sql.execute('INSERT INTO users VALUES(?,?,?,?);', (id, name, num, loc))
    #Фиксируем изменения
    connection.commit()

#Проверка на наличие юзера в БД
def checker(id):
    check = sql.execute('SELECT id FROM users WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False


##Методы для продуктов##
#Добавление
def add_pr(name, des, count, price, photo):
    sql.execute('INSERT INTO products(pr_name, pr_des, pr_count, pr_price, pr_photo) '
                'VALUES(?, ?, ?, ?, ?);', (name, des, count, price, photo))
    #Фиксируем изменения
    connection.commit()
#Удаление
def del_pr(id):
    sql.execute('DELETE FROM products WHERE id=?;', (id,))
    #Фиксируем изменения
    connection.commit()
#Найти продукт по id
def check_pr(id):
    checker = sql.execute('SELECT id FROM products WHERE id=?;', (id,))
    if checker:
        return True
    else:
        return False

#Вывод названий продуктов с их id
def get_pr_id():
    return sql.execute('SELECT id, pr_name, pr_count, pr_price FROM products;').fetchall()
def get_pr_name_id():
    products = sql.execute('SELECT id, pr_name, pr_count FROM products;').fetchall()
    #Отсортировали продукты, кол-во которых больше 0
    sorted_prods = [i[0] for i in products if i[2] > 0]
    return sorted_prods
#Вывести всю информацию о конкретном продукте
def get_pr(id):
    return sql.execute('SELECT pr_name, pr_des, pr_count, pr_price, pr_photo '
                       'FROM products WHERE id=?;', (id,)).fetchone()


#Проверка на наличие продуктов в базе
def check_products():
    checker = sql.execute('SELECT * FROM products;')
    if checker:
        return True
    else:
        return False


##Методы для корзины##
#Добавление продукта в корзину
def add_to_cart(user_id, user_product, pr_quantity, total):
        sql.execute('INSERT INTO cart VALUES(?, ?, ?, ?);',
                    (user_id, user_product, pr_quantity, total))
        #Фиксируем изменения
        connection.commit()
        #Алгоритм убывания товара
        amount = sql.execute('SELECT pr_count FROM products WHERE pr_name=?;',
                             (user_product,)).fetchone()
        sql.execute(f'UPDATE products SET pr_count={amount[0] - pr_quantity} '
                    f'WHERE pr_name=?;', (user_product,))
        # Фиксируем изменения
        connection.commit()

#Удаление из корзины
def clear_cart(user_id):
    pr_name = sql.execute('SELECT user_product FROM cart WHERE user_id=?;', (user_id,)).fetchone()
    amount = sql.execute('SELECT pr_count FROM products WHERE pr_name=?;',
                         (pr_name[0],)).fetchone()[0]
    pr_quantity = sql.execute('SELECT product_quantity FROM cart WHERE user_id=?;',
                              (user_id,)).fetchone()[0]
    sql.execute(f'UPDATE products SET pr_count={amount + pr_quantity} WHERE pr_name=?;',
                (pr_name[0],))
    # Фиксируем изменения
    connection.commit()
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))
    # Фиксируем изменения
    connection.commit()

#Отображение корзины
def show_cart(user_id):
    return sql.execute('SELECT user_product, product_quantity, total FROM cart WHERE '
                       'user_id=?;', (user_id,))

def ordered(user_id):
    sql.execute('DELETE FROM cart WHERE user_id=?;', (user_id,))
    # Фиксируем изменения
    connection.commit()