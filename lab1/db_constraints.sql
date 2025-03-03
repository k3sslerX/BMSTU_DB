ALTER TABLE cars
    ALTER COLUMN vin SET NOT NULL,
    ALTER COLUMN brand SET NOT NULL,
    ALTER COLUMN model SET NOT NULL,
    ALTER COLUMN body SET NOT NULL,
    ALTER COLUMN year_of_production SET NOT NULL,
    ALTER COLUMN engine_type SET NOT NULL,
    ADD CONSTRAINT CK_vin_pk PRIMARY KEY (vin),
    ADD CONSTRAINT CK_year_of_production CHECK (year_of_production BETWEEN 1800 AND 2024),
    ADD CONSTRAINT CK_type1 CHECK (engine_type = 'Petrol' OR engine_type = 'Electro' OR engine_type = 'Hybrid');

ALTER TABLE engines
    ALTER COLUMN engine_serial SET NOT NULL,
    ALTER COLUMN type SET NOT NULL,
    ALTER COLUMN power SET NOT NULL,
    ALTER COLUMN cylinders SET NOT NULL,
    ALTER COLUMN volume SET NOT NUlL,
    ADD CONSTRAINT CK_engine_serial_pk PRIMARY KEY (engine_serial),
    ADD CONSTRAINT CK_type2 CHECK (type = 'Petrol' OR type = 'Electro' OR type = 'Hybrid'),
    ADD CONSTRAINT CK_power CHECK (power BETWEEN 100 AND 1500),
    ADD CONSTRAINT CK_cylinders CHECK (cylinders BETWEEN 0 AND 12),
    ADD CONSTRAINT CK_volume CHECK (volume BETWEEN 0 AND 7);

ALTER TABLE showrooms
    ALTER COLUMN ogrn SET NOT NULL,
    ALTER COLUMN name SET NOT NULL,
    ADD CONSTRAINT CK_ogrn_pk PRIMARY KEY (ogrn);

ALTER TABLE cars_engines
    ALTER COLUMN vin SET NOT NULL,
    ALTER COLUMN engine_serial SET NOT NULL,
    ADD CONSTRAINT CK_vin_fk1 FOREIGN KEY (vin) REFERENCES cars(vin) ON DELETE CASCADE,
    ADD CONSTRAINT CK_engine_fk1 FOREIGN KEY (engine_serial) REFERENCES engines(engine_serial) ON DELETE CASCADE;

ALTER TABLE cars_prices
    ALTER COLUMN vin SET NOT NULL,
    ALTER COLUMN price SET NOT NULL,
    ADD CONSTRAINT CK_price CHECK (price BETWEEN 0 AND 30000000),
    ADD CONSTRAINT CK_vin_fk2 FOREIGN KEY (vin) REFERENCES cars(vin) ON DELETE CASCADE;

ALTER TABLE cars_engines_showrooms
    ALTER COLUMN vin SET NOT NULL,
    ALTER COLUMN engine_serial SET NOT NULL,
    ALTER COLUMN ogrn SET NOT NULL,
    ADD CONSTRAINT CK_vin_fk3 FOREIGN KEY (vin) REFERENCES cars(vin) ON DELETE CASCADE,
    ADD CONSTRAINT CK_engine_fk2 FOREIGN KEY (engine_serial) REFERENCES engines(engine_serial) ON DELETE CASCADE,
    ADD CONSTRAINT CK_ogrn_fk FOREIGN KEY (ogrn) REFERENCES showrooms(ogrn) ON DELETE CASCADE;
