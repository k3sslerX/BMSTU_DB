import random


def generate_vin():
    vin = ""
    vin_letters = [1, 2, 3, 4, 5, 6, 7, 8, 0, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                   'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for i in range(17):
        vin = f"{vin}{vin_letters[random.randint(0, len(vin_letters) - 1)]}"
    return vin


def check_vin_unique(vin, vin_list):
    for el in vin_list:
        if vin == el:
            # print(f"Match!\n{el}\n{vin}")
            return False
    return True


def generate_cars(amount):
    cars_templates = []
    cars = []
    with open("data/cars.txt") as file:
        brend = None
        for string in file:
            string = string[:-1]
            if brend is None:
                brend = string
            elif string == '---':
                brend = None
            else:
                car_data = string.split(sep=' | ')
                if len(car_data) == 5:
                    car_name = car_data[0]
                    car_body = car_data[1]
                    car_year_start = int(car_data[2])
                    if car_data[3] == '-':
                        car_data[3] = '2024'
                    car_year_stop = int(car_data[3])
                    car_engine = car_data[4]
                    cars_templates.append({'car_brand': brend, 'car_name': car_name, 'car_body': car_body, 'car_year_start': car_year_start,
                                           'car_year_stop': car_year_stop, 'car_engine': car_engine})
    for i in range(amount):
        vin_list = []
        car_vin = generate_vin()
        while not check_vin_unique(car_vin, vin_list):
            car_vin = generate_vin()
        vin_list.append(car_vin)
        car_template = cars_templates[random.randint(0, len(cars_templates) - 1)]
        car_brend = car_template['car_brand']
        car_name = car_template['car_name']
        car_body = car_template['car_body']
        car_year = random.randint(car_template['car_year_start'], car_template['car_year_stop'])
        car_engine = car_template['car_engine']
        cars.append({'car_vin': car_vin, 'car_brand': car_brend, 'car_name': car_name, 'car_body': car_body,
                     'car_year': car_year,
                     'car_engine': car_engine})
    print("Cars - Successfully")
    return cars
