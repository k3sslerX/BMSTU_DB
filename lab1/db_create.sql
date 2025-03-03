CREATE TABLE IF NOT EXISTS cars(
    vin TEXT,
    brand TEXT,
    model TEXT,
    body TEXT,
    year_of_production INT,
    engine_type TEXT
);

CREATE TABLE IF NOT EXISTS engines(
    engine_serial TEXT,
    type TEXT,
    power INT,
    cylinders INT,
    volume FLOAT
);

CREATE TABLE IF NOT EXISTS showrooms(
    ogrn TEXT,
    name TEXT
);

CREATE TABLE IF NOT EXISTS cars_engines(
    vin TEXT,
    engine_serial TEXT
);

CREATE TABLE IF NOT EXISTS cars_prices(
    vin TEXT,
    price INT
);

CREATE TABLE IF NOT EXISTS cars_engines_showrooms(
    ogrn TEXT,
    vin TEXT,
    engine_serial TEXT
);