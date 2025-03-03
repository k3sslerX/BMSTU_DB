import json
import psycopg2
from linq_to_obj import Car


def get_json_automobiles(con):
    cursor = con.cursor()
    cursor.execute("copy (select row_to_json(c) from cars as c) to 'C:/DB/json_files/automobiles.json';")
    print("Создание JSON для таблицы cars - success!")
    cursor.close()


def data_output(data, keys):
    for key in keys:
        print("{:^30}".format(str(data[key])), end='')
    print()


def read_json(filename):
    file = open(filename, 'r')
    for line in file:
        data = json.loads(line)
        keys = data.keys()
        data_output(data, keys)
    file.close()


def update_json(filename, brand, model, year):
    file = open(filename, 'r')
    data = list()
    for line in file:
        data.append(json.loads(line))
    keys = data[0].keys()
    for elem in data:
        if elem['brand'] == brand and elem['model'] == model:
            data_output(elem, keys)
            elem['year_of_production'] = year
            data_output(elem, keys)
    file.close()
    file = open(filename, 'w')
    for elem in data:
        file.write(json.dumps(elem, ensure_ascii=False) + '\n')
    file.close()


def insert_into_json(filename, data):
    file = open(filename, 'a')
    file.write(json.dumps(data, ensure_ascii=False) + '\n')
    file.close()


def task_2():
    con = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="1337",
        host="localhost",
    )

    get_json_automobiles(con)
    filename = "../json_files/cars.json"

    print("1. Чтение файла JSON")
    read_json(filename)

    print("2. Обновление JSON документа (установка года производства для автомобилей определенной модели)")
    brand = input("Марка авто: ")
    model = input("Модель авто: ")
    year = int(input("Год производства (от 1800 до 2024): "))
    while year < 1800 or year > 2024:
        year = int(input("Год производства (ОТ 1800 ДО 2024): "))
    update_json(filename, brand, model, year)

    print("3. Добавление в JSON документ")
    vin = input("VIN:")
    brand = input("Марка авто: ")
    model = input("Модель авто: ")
    body = input("Тип кузова: ")
    year_of_production = int(input("Год производства: "))
    engine_type = input("Тип двигателя: ")
    insert_into_json(filename,
                     Car(vin, brand, model, body, year_of_production, engine_type).get())
    read_json(filename)
    con.close()


if __name__ == '__main__':
    task_2()