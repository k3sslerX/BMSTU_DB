import time, datetime, json, random


def generate_serial():
    serial = ""
    serial_letters = [1, 2, 3, 4, 5, 6, 7, 8, 0, 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                      'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    for i in range(30):
        serial = f"{serial}{serial_letters[random.randint(0, len(serial_letters) - 1)]}"
    return serial


def check_serial_unique(serial, serial_list):
    for el in serial_list:
        if serial == el:
            print(f"Match!\n{el}\n{serial}")
            return False
    return True


def generate_engines_data(engines_amount):
    template_engines = []
    serials = []
    petrol = False
    electro = False
    hybrid = False
    for i in range(engines_amount):
        engine_serial = generate_serial()
        while not check_serial_unique(engine_serial, serials):
            engine_serial = generate_serial()
        serials.append(engine_serial)
        if not petrol:
            engine_type = 'Petrol'
            petrol = True
        elif not electro:
            engine_type = 'Electro'
            electro = True
        elif not hybrid:
            engine_type = 'Hybrid'
            hybrid = True
        else:
            engine_type = random.choice(['Petrol', 'Electro', 'Hybrid'])
        engine_power = random.randint(100, 1500)
        if engine_type != 'Electro':
            engine_volume = f"{random.randint(1, 6)}.{random.randint(0, 9)}"
            engine_cylinders = random.randint(4, 12)
            engine_cylinders += engine_cylinders % 2
        else:
            engine_volume = 0
            engine_cylinders = 0
        template_engines.append({'engine_serial': engine_serial, 'type': engine_type,
                                 'power': engine_power, 'cylinders': engine_cylinders,
                                 'volume': engine_volume})
    print('Engines data - Successfully')
    return template_engines


if __name__ == "__main__":
    number = 10
    count = 0
    while True:
        filename = f"./json_files/{count}-{datetime.datetime.now()}-engines.json"
        tablespace = "engines"
        engines_dict = generate_engines_data(number)
        with open(filename, 'w') as file:
            json.dump(engines_dict, file)
        count += 1
        time.sleep(300)
