from peewee import *

db = PostgresqlDatabase(
    database="postgres",
    user="postgres",
    password="1337",
    host="localhost",
)


class BaseModel(Model):
    class Meta:
        database = db


class Cars(BaseModel):
    vin = PrimaryKeyField(column_name='vin')
    brand = CharField(column_name='brand')
    model = CharField(column_name='model')
    body = CharField(column_name='body')
    year_of_production = IntegerField(column_name='year_of_production')
    engine_type = CharField(column_name='engine_type')

    class Meta:
        table_name = 'cars'


class Engines(BaseModel):
    engine_serial = PrimaryKeyField(column_name='engine_serial')
    type = CharField(column_name='type')
    power = IntegerField(column_name='power')
    cylinders = IntegerField(column_name='cylinders')
    volume = FloatField(column_name='volume')

    class Meta:
        table_name = 'engines'


class Prices(BaseModel):
    vin = ForeignKeyField(Cars, column_name='vin', to_field='vin')
    price = IntegerField(column_name='price')

    class Meta:
        table_name = 'cars_prices'


def request_01():
    result = Cars.select(Cars.brand, Cars.model, Cars.year_of_production).\
        where(Cars.year_of_production <= 1970)
    for row in result.namedtuples():
        print("{:^30}{:^30}{:^30}".format(row.brand, row.model, row.year_of_production))


def request_02():
    result = Cars.select(Cars.vin, Cars.brand, Cars.model, Prices.price).\
        join(Prices, on=(Cars.vin == Prices.vin)).\
        where(Prices.price > 25000000)
    for row in result.namedtuples():
        print("{:^30}{:^30}{:^30}{:^30}".format(row.vin, row.brand, row.model, row.price))


def print_cars():
    print("\nCars:")
    result = Cars.select(Cars.vin, Cars.brand, Cars.model, Cars.body, Cars.year_of_production, Cars.engine_type)
    for row in result.namedtuples():
        print("{:^30}{:^30}{:^30}{:^30}{:^30}{:^30}".format(row.vin, row.brand, row.model, row.body,
                                                            row.year_of_production, row.engine_type))


def print_engines():
    print("\nEngines:")
    result = Engines.select(Engines.engine_serial, Engines.type, Engines.power, Engines.cylinders,
                            Engines.volume)
    for row in result.namedtuples():
        print("{:^30}{:^30}{:^30}{:^30}{:^30}".format(row.engine_serial, row.type, row.power, row.cylinders,
                                                      row.volume))


def adding(vin, brand, model, body, year_of_production, engine_type):
    try:
        Cars.create(vin=vin, brand=brand, model=model, body=body, year_of_production=year_of_production,
                    engine_type=engine_type)
        print("Added!")
    except Exception as exc:
        print(exc)


def updating(brand, year):
    try:
        cars = Cars.select().where(Cars.brand == brand)
        for car in cars:
            car.year_of_production = year
            car.save()
        print("Updated!")
    except Exception as exc:
        print(exc)


def deleting(engine_type):
    try:
        engine = Engines.get(type=engine_type)
        engine.delete_instance()
        print("Deleted!")
    except Exception as exc:
        print(exc)


def request_03():
    print("-- Добавление в таблицу")
    vin = input("VIN:")
    brand = input("Марка авто: ")
    model = input("Модель авто: ")
    body = input("Тип кузова: ")
    year_of_production = int(input("Год производства: "))
    engine_type = input("Тип двигателя: ")
    adding(vin, brand, model, body, year_of_production, engine_type)
    print_cars()

    print("-- Обновление таблицы")
    brand = input("Марка авто: ")
    year = int(input("Год производства (от 1800 до 2024): "))
    while year < 1800 or year > 2024:
        year = int(input("Год производства (ОТ 1800 ДО 2024): "))
    updating(brand, year)
    print_cars()
    input()

    print("-- Удаление из таблицы")
    engine_type = 'Electro'
    print_engines()
    input()
    deleting(engine_type)
    print_engines()


def request_04():
    try:
        cursor = db.cursor()
        print("Увеличение цены автомобилей заданного бренда на заданный процент")
        cursor.execute("call UpdatePriceForBrand(1, 'Bentley')")
        print_cars()
    except Exception as exc:
        print(exc)


def task_3():
    print("1. Все автомобили до 1970 года выпуска:")
    request_01()
    input()

    print("2. Автомобили дороже 25 млн. рублей:")
    request_02()
    input()

    print("3. 3 запроса")
    request_03()
    input()

    print("4. Получение доступа к данным с помоью хранимой процедуры")
    request_04()
    input()


if __name__ == "__main__":
    task_3()
