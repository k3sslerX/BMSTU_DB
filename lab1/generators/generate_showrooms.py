import random

from faker import Faker
from random import choice, randint


def generate_unique_ogrn(number):
    ogrn_list = []
    fake_ru = Faker('ru_RU')
    for _ in range(number):
        ogrn = fake_ru.businesses_ogrn()
        i = 0
        while i < len(ogrn_list):
            if ogrn == ogrn_list[i]:
                ogrn = fake_ru.businesses_ogrn()
                i = 0
            i += 1
        ogrn_list.append(ogrn)
    return ogrn_list


def generate_showrooms_data(amount):
    showrooms = []
    fake = Faker()
    ogrn_list = generate_unique_ogrn(amount)
    for i in range(amount):
        ogrn = ogrn_list[i]
        name = fake.company()
        # address = fake.address()
        showrooms.append({'ogrn': ogrn, 'name': name})
    print("List of showrooms - Successfully")
    return showrooms


def generate_showrooms(showrooms, car_engines, capacity):
    cars_showrooms = []
    for showroom in showrooms:
        for i in range(capacity):
            car_engine = random.choice(car_engines)
            cars_showrooms.append({'ogrn': showroom['ogrn'], 'car': car_engine['car_vin'],
                                   'engine': car_engine['car_engine_serial']})
    print("List of showrooms cars engines - Successfully")
    return cars_showrooms
