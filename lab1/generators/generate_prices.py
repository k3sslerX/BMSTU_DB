import random


def generate_prices(cars, car_engines, engines):
    prices = []
    for car in cars:
        car_vin = car['car_vin']
        car_engine = None
        car_engine_data = None
        for tmp_car_engine in car_engines:
            if tmp_car_engine['car_vin'] == car_vin:
                car_engine = tmp_car_engine['car_engine_serial']
        for tmp_car_engine_data in engines:
            if tmp_car_engine_data['engine_serial'] == car_engine:
                car_engine_data = tmp_car_engine_data
        price = random.randint(1000000, 5000000)
        price += int(car_engine_data['engine_power']) * random.randint(1000, 5000)
        if car_engine_data['engine_type'] != 'Electro':
            price += int(float(car_engine_data['engine_volume']) * random.randint(100000, 500000))
            price += int(car_engine_data['engine_cylinders']) * random.randint(200000, 1000000)
        else:
            price += random.randint(2000000, 10000000)
        prices.append({'car_vin': car_vin, 'car_price': price})
    return prices
