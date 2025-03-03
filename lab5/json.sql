-- 1. Выгрузить данные из таблиц в JSON
select row_to_json(c) from cars c;
select row_to_json(s) from showrooms s;
select row_to_json(e) from engines e;
select row_to_json(c_e) from cars_engines c_e;
select row_to_json(p) from cars_prices p;
select row_to_json(c_e_s) from cars_engines_showrooms c_e_s;

-- Загружаем данные в файл
copy (select row_to_json(c) from cars c)
to '/Users/k3ssler/BMSTU/DB/lab5/json_files/cars.json';
copy (select row_to_json(s) from showrooms s)
to '/Users/k3ssler/BMSTU/DB/lab5/json_files/showrooms.json';
copy (select row_to_json(e) from engines e)
to '/Users/k3ssler/BMSTU/DB/lab5/json_files/engines.json';
copy (select row_to_json(c_e) from cars_engines c_e)
to '/Users/k3ssler/BMSTU/DB/lab5/json_files/cars_engines.json';
copy (select row_to_json(p) from cars_prices p)
to '/Users/k3ssler/BMSTU/DB/lab5/json_files/prices.json';
copy (select row_to_json(c_e_s) from cars_engines_showrooms c_e_s)
to '/Users/k3ssler/BMSTU/DB/lab5/json_files/cars_engines_showrooms.json';


-- 2. Создание таблицы по полученному JSON

-- Создаем таблицу со столбцом типа JSON
drop table if exists json_data;
create table json_data(data json);

-- Копируем данные JSON из файла в созданную таблицу
copy json_data(data)
from '/Users/k3ssler/BMSTU/DB/lab5/json_files/engines.json';

select *
from json_data;

-- Таблица-копия таблицы engines
drop table if exists engines_json;
create table engines_json(
    engine_serial TEXT not null primary key,
    type TEXT not null check (type = 'Petrol' OR type = 'Electro' OR type = 'Hybrid'),
    power INT not null check (power BETWEEN 100 AND 1500),
    cylinders INT not null check (cylinders BETWEEN 0 AND 12),
    volume FLOAT not null check (volume BETWEEN 0 AND 7)
);
select *
from engines_json;

-- Заполняем таблицу данными из таблицы с данными JSON
insert into engines_json(engine_serial, type, power, cylinders, volume)
select data->>'engine_serial',
       data->>'type',
       (data->>'power')::int,
       (data->>'cylinders')::int,
       (data->>'volume')::float
from json_data;


-- 3. Создать таблицу с атрибутами типа JSON (или добавить к существующей столбец)
alter table cars
add column if not exists json_data json;

-- Добавляем данные JSON
update cars
set json_data = '{"color":"black"}'
where brand = 'BMW';

update cars
set json_data = '{"color":"red"}'
where brand = 'Ferrari';

update cars
set json_data = '{"color":"Blue"}'
where brand = 'Bugatti';

update cars
set json_data = '{"color":"White"}'
where brand = 'Mercedes-Benz';

select *
from cars;


-- 4. Выполнить следующие действия:

-- Извлечь JSON фрагмент из JSON документа
-- Извлечь значения конкретных узлов или атрибутов JSON документа
drop table if exists temp_table;
create table if not exists temp_table(data json);

copy temp_table
from '/Users/k3ssler/BMSTU/DB/lab5/json_files/cars.json';

select *
from temp_table;

drop table if exists json_test;
create table json_test(
    brand TEXT,
    model TEXT
);

insert into json_test(brand, model)
select data->>'brand', data->>'model'
from temp_table
where data->>'brand' like '%Bugatti%';

select *
from json_test;

-- Изменить JSON документ
update json_test
set brand = 'Beast'
where model = 'Bolide';

-- Разделить JSON документ на несколько строк по узлам
drop table if exists json_test_2;
create table json_test_2(
    car TEXT,
    info json);

insert into json_test_2 (car, info)
values ('Koenigsegg Gemera', '[{"engine_amount": 5, "summary_power": 1775, "engine_type":"Hybrid"}, {"color":"green", "seats": 4, "doors": 2}]');

select *
from json_test_2;

select car, json_array_elements(info)
from json_test_2;
