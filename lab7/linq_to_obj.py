from py_linq import *


class Car():
    vin = str()
    brand = str()
    model = str()
    body = str()
    year_of_production = int()
    engine_type = str()

    def __init__(self, vin, brand, model, body, year_of_production, engine_type):
        self.vin = vin
        self.brand = brand
        self.model = model
        self.body = body
        self.year_of_production = int(year_of_production)
        self.engine_type = engine_type

    def get(self):
        return {'vin': self.vin, 'brand': self.brand, 'model': self.model,
                'body': self.body, 'year_of_production': self.year_of_production, 'engine_type': self.engine_type}


def check_cars_constraints(elem):
    if elem[4] < 1800 or elem[4] > 2024:
        return False
    if elem[5] != 'Hybrid' and elem[5] != 'Petrol' and elem[5] != 'Electro':
        return False
    return True


def get_cars_array(filename):
    file = open(filename, 'r')
    cars = []
    for line in file:
        elem = line.split(';')
        if check_cars_constraints(elem):
            cars.append(Car(elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]).get())
    return cars


class Engine():
    engine_serial = str()
    engine_type = str()
    power = int()
    cylinders = int()
    volume = float()

    def __init__(self, engine_serial, engine_type, power, cylinders, volume):
        self.engine_serial = engine_serial
        self.engine_type = engine_type
        self.power = int(power)
        self.cylinders = int(cylinders)
        self.volume = float(volume)

    def get(self):
        return {'engine_serial': self.engine_serial, 'type': self.engine_type, 'power': self.power,
                'cylinders': self.cylinders, 'volume': self.volume}


def check_engines_constraints(elem):
    if elem[1] != 'Hybrid' and elem[2] != 'Petrol' and elem[2] != 'Electro':
        return False
    if elem[2] < 100 or elem[3] > 1500:
        return False
    if elem[3] < 0 or elem[3] > 12:
        return False
    if elem[4] < 0 or elem[4] > 7:
        return False
    return True


def get_engines_array(filename):
    file = open(filename, 'r')
    engines = []
    for line in file:
        elem = line.split(';')
        if check_engines_constraints(elem):
            engines.append(Engine(elem[0], elem[1], elem[2], elem[3], elem[4]).get())
    return engines


class Price():
    vin = str()
    price = int()

    def __init__(self, vin, price):
        self.vin = vin
        self.price = int(price)

    def get(self):
        return {'vin': self.vin, 'price': self.price}


def check_prices_constraints(elem):
    if elem[1] < 0 or elem[1] > 30000000:
        return False
    return True


def get_prices_array(filename):
    file = open(filename, 'r')
    prices = []
    for line in file:
        elem = line.split(';')
        if check_prices_constraints(elem):
            prices.append(Price(elem[0], elem[1]).get())
    return prices


def request_01(cars):
    return cars.select(lambda x: {x['model']})


def request_02(cars):
    return cars.where(lambda x: x['year_of_production'] > 2012).select(lambda x: {x['brand'], x['model'],
                                                                                  x['year_of_production']})


def request_03(cars):
    return cars.group_by(key_names=['brand'], key=lambda x: x['brand']).select(lambda g: {'key': g.key.brand,
                                                                                          'count': g.count()})


def request_04(cars, prices):
    return cars.join(prices, lambda с: с['vin'], lambda p: p['vin'], lambda result: result)


def request_05(engines):
    return engines.where(lambda x: x['type'] == 'Electro').select(lambda x: x['power']).max()


def print_linq_list_amount(linq_lst, amount):
    for i in range(amount):
        print(*linq_lst[i])
    print()


def task_1():
    cars = Enumerable(get_cars_array("../lab1/csv_files/cars.csv"))
    engines = Enumerable(get_engines_array("../lab1/csv_files/engines.csv"))
    prices = Enumerable(get_prices_array("../lab1/csv_files/prices.csv"))

    print("1. Вывод нескольких моделей авто")
    print_linq_list_amount(request_01(cars).to_list(), 10)

    print("2. Автомобили, выпущенные после 2012")
    print_linq_list_amount(request_02(cars).to_list(), 10)

    print("3. Количество авто каждой марки")
    req3_res = request_03(cars).to_list()
    for elem in req3_res:
        print(f"{elem['key']} - {elem['count']}")
    print()

    print("4. Join таблицы авто и цен")
    print_linq_list_amount(request_04(cars, prices).to_list(), 10)

    print("5. Самый мощный электродвигатель\n", request_05(engines))


if __name__ == '__main__':
    task_1()
