from generators import generate_car, generate_engine, generate_prices, generate_showrooms, csv_proc


def generate_db():
    cars_amount = 3000
    engines_amount = 1000
    showrooms_amount = 1000
    cars_in_single_showroom = 200

    cars_dict = generate_car.generate_cars(cars_amount)
    engines_dict = generate_engine.generate_engines_data(engines_amount)
    cars_engines_dict = generate_engine.generate_engines(cars_dict, engines_dict)
    prices_dict = generate_prices.generate_prices(cars_dict, cars_engines_dict, engines_dict)
    showrooms_dict = generate_showrooms.generate_showrooms_data(showrooms_amount)
    cars_engines_showrooms_dict = generate_showrooms.generate_showrooms(showrooms_dict,
                                                                        cars_engines_dict, cars_in_single_showroom)

    cars = []
    engines = []
    cars_engines = []
    prices = []
    showrooms = []
    cars_engines_showrooms = []

    for car in cars_dict:
        cars.append([car['car_vin'], car['car_brand'], car['car_name'], car['car_body'], car['car_year'], car['car_engine']])
    for engine in engines_dict:
        engines.append([engine['engine_serial'], engine['engine_type'], engine['engine_power'],
                        engine['engine_cylinders'], engine['engine_volume']])
    for car_engine in cars_engines_dict:
        cars_engines.append([car_engine['car_vin'], car_engine['car_engine_serial']])
    for price in prices_dict:
        prices.append([price['car_vin'], price['car_price']])
    for showroom in showrooms_dict:
        showrooms.append([showroom['ogrn'], showroom['name']])
    for car_engine_showroom in cars_engines_showrooms_dict:
        cars_engines_showrooms.append([car_engine_showroom['ogrn'], car_engine_showroom['car'],
                                       car_engine_showroom['engine']])

    csv_proc.get_csv(cars, 'cars.csv')
    csv_proc.get_csv(engines, 'engines.csv')
    csv_proc.get_csv(cars_engines, 'cars_engines.csv')
    csv_proc.get_csv(prices, 'prices.csv')
    csv_proc.get_csv(showrooms, 'showrooms.csv')
    csv_proc.get_csv(cars_engines_showrooms, 'cars_engines_showrooms.csv')


if __name__ == '__main__':
    generate_db()
