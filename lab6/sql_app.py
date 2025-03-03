import psycopg2

con = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="1337",
    host="localhost"
)

print("Successed connection!")


def format_output(output):
    for note in output:
        for var in note:
            if var is not None:
                print("|{:^30}".format(var), end='')
        print('|')
        print(("-" * 31) * len(note))


# Выполнить скалярный запрос
# Список машин, выпущенных в период с 2020 по 2024 год
def task_1():
    print("Список машин, выпущенных в период с 2020 по 2024 год")
    cursor = con.cursor()
    cursor.execute("select * from cars where year_of_production between 2020 and 2024")
    format_output(cursor.fetchall())


# Выполнить запрос с несколькими соединениями (JOIN)
# Список автомобилей марки Porsche, мощность их двигателей и цена
def task_2():
    print("Список автомобилей марки Porsche, мощность их двигателей и цена")
    cursor = con.cursor()
    cursor.execute("select c.brand, c.model, e.power, p.price "
                   "from cars as c "
                   "join cars_engines as c_e on c.vin = c_e.vin "
                   "join engines as e on c_e.engine_serial = e.engine_serial "
                   "join cars_prices as p on c.vin = p.vin "
                   "where brand = 'Porsche'")
    format_output(cursor.fetchall())


# Выполнить запрос с ОТВ(CTE) и оконными функциями
# Вывод средних, минимальных и максимальных значений цены по различным группам
def task_3():
    print("Вывод средних, минимальных и максимальных значений цены по различным группам")
    cursor = con.cursor()
    cursor.execute("select c.brand, c.model, p.price, "
                   "avg(p.price) over (partition by brand) as avg_brand_price,"
                   "min(p.price) over (partition by brand order by model) as min_brand_price,"
                   "max(p.price) over (partition by model) as max_model_price "
                   "from cars as c join cars_prices as p on c.vin = p.vin")

    format_output(cursor.fetchall())


# Выполнить запрос к метаданным
# Вывод данных о таблице cars
def task_4():
    print("Вывод данных о таблице cars")
    cursor = con.cursor()
    cursor.execute("select column_name, data_type "
                   "from information_schema.columns "
                   "where table_name = 'cars'")
    format_output(cursor.fetchall())


# Вызвать скалярную функцию (написанную в третьей лабораторной работе)
# Значение цены с примением указанной скидки
def task_5():
    print("Значение цены с примением указанной скидки")
    cursor = con.cursor()
    cursor.execute("select c.brand, c.model, p.price, PriceSale(p.price, 25) "
                   "from cars as c join cars_prices as p on c.vin = p.vin")
    format_output(cursor.fetchall())


# Вызвать многооператорную или табличную функцию (написанную в третьей лабораторной работе)
# Автомобили заданного бренда или заданного года производства
def task_6():
    print("Автомобили марки BMW или автмобили 2024 года выпуска")
    cursor = con.cursor()
    cursor.execute("select * from GetAutosByBrandOrProdYear('BMW', 2024)")
    format_output(cursor.fetchall())


# Вызвать хранимую процедуру (написанную в третьей лабораторной работе)
# Обновление цены на заданный процент у указанного бренда
def task_7():
    print("Повышение цены на 1% у автомобилей марки Mercedes-Benz")
    cursor = con.cursor()
    cursor.execute("call UpdatePriceForBrand(1, 'Mercedes-Benz')")
    cursor.execute("select * "
                   "from cars "
                   "where brand = 'Mercedes-Benz'")
    format_output(cursor.fetchall())


# Вызвать системную функцию или процедуру
# Имя пользователя в текущем контексте выполнения
def task_8():
    print("Имя пользователя в текущем контексте выполнения")
    cursor = con.cursor()
    cursor.execute("select * from current_user")
    format_output(cursor.fetchall())


# Создать таблицу в базе данных, соответствующую тематике БД
# Создание таблицы страны производителя для марок
def task_9():
    print("Создание таблицы страны производителя для марок")
    cursor = con.cursor()
    try:
        cursor.execute("drop table if exists brand_countries;")
        cursor.execute("create table brand_countries("
                       "brand TEXT not null, "
                       "country TEXT not null)")
        con.commit()
    except Exception:
        print("Ошибка создания таблицы")
        con.rollback()
    else:
        print("Таблица успешно создана")


# Выполнить вставку данных в созданную таблицу с использованием инструкции INSERT или COPY
# Заполнение таблицы brand_countries
def task_10():
    try:
        print("Вставить данные в таблицу brand_countries")
        cursor = con.cursor()
        cursor.execute("insert into brand_countries(brand, country) values "
                       "('BMW', 'Germany'), "
                       "('Mercedes-Benz', 'Germany'), "
                       "('Audi', 'Germany'), "
                       "('Tesla', 'USA'), "
                       "('Porsche', 'Germany'), "
                       "('Lamborghini', 'Italy'), "
                       "('Ferrari', 'Italy'), "
                       "('Rolls-Royce', 'UK'), "
                       "('Koenigsegg', 'Sweden'), "
                       "('Lotus', 'UK'), "
                       "('Bugatti', 'France'), "
                       "('Bentley', 'UK');"
                       "select * from brand_countries;")
        format_output(cursor.fetchall())
        con.commit()
        cursor.execute("select * from brand_countries")
        format_output(cursor.fetchall())
    except Exception:
        print("Ошибка заполнения таблицы")
        con.rollback()


def print_menu():
    print("1. Выполнить скалярный запрос")
    print("2. Выполнить запрос с несколькими соединениями (JOIN)")
    print("3. Выполнить запрос с ОТВ(CTE) и оконными функциями")
    print("4. Выполнить запрос к метаданным")
    print("5. Вызвать скалярную функцию (написанную в третьей лабораторной работе)")
    print("6. Вызвать многооператорную или табличную функцию (написанную в третьей лабораторной работе)")
    print("7. Вызвать хранимую процедуру (написанную в третьей лабораторной работе)")
    print("8. Вызвать системную функцию или процедуру")
    print("9. Создать таблицу в базе данных, соответствующую тематике БД")
    print("10. Выполнить вставку данных в созданную таблицу с использованием инструкции INSERT или COPY")
    print("0. Выход")
    print("----------------------------------------")


mode = -1
while mode != 0:
    print_menu()
    try:
        mode = int(input('Введите действие: '))
    except ValueError:
        print("Введено неверное значение. Попрообуйте снова.")
        mode = -1
    else:
        if 0 > mode > 10:
            print('Введено неверное значение. Попробуйте снова.')
        else:
            if mode == 1:
                task_1()
            elif mode == 2:
                task_2()
            elif mode == 3:
                task_3()
            elif mode == 4:
                task_4()
            elif mode == 5:
                task_5()
            elif mode == 6:
                task_6()
            elif mode == 7:
                task_7()
            elif mode == 8:
                task_8()
            elif mode == 9:
                task_9()
            elif mode == 10:
                task_9()
                task_10()
            elif mode == 0:
                print('Выход.')
            input('Нажмите Enter для выхода.')
