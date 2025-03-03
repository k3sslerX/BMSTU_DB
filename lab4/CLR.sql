create extension plpython3u;

-- 1. Определяемая пользователем скалярная функция CLR
-- Разбиение автомобилей по количеству дверей, в зависимости от кузова
drop function if exists auto_doors_count;

create or replace function auto_doors_count(body text)
returns INT as
$$
    if body == 'Supercar' or body == 'Coupe' or body == 'Cabriolet' or body == 'Hypercar':
        return 2
    elif body == 'Sedan' or body == 'Crossover' or body == 'Hatchback' or body == 'Pickup track':
        return 4
$$ language plpython3u;

select brand, model, body, auto_doors_count(body)
from cars;


-- 2. Пользовательская агрегатная функция CLR
-- Получить среднюю мощность машин заданного бренда
drop function if exists avg_power_brand;

create or replace function avg_power_brand(name text)
returns float as
$$
	plan = plpy.prepare("select power from cars as c join cars_engines as c_e on c.vin = c_e.vin join engines as e on c_e.engine_serial = e.engine_serial where c.brand = $1", ['text'])
	result = plpy.execute(plan, [name])
	count = 0
	avg_power = 0
	print(result)
	if result is not None:
		for i in result:
			count += 1
			avg_power += i['power']
	return avg_power / count
$$ language plpython3u;

select avg_power_brand('Porsche');


-- 3. Определяемая пользователем табличная функция CLR
-- Автомобили с заданной мощностью
drop function if exists autos_with_power;

create or replace function autos_with_power(num int)
returns table (brand text, model text, power int) as
$$
	plan = plpy.prepare("select c.brand, c.model, e.power from cars as c join cars_engines as c_e on c.vin = c_e.vin join engines as e on c_e.engine_serial = e.engine_serial where e.power = $1", ['int'])
	result = plpy.execute(plan, [num])
	table = list()
	if result is not None:
		for i in result:
			table.append(i)
	return table
$$ language plpython3u;

select * from autos_with_power(243);


-- 4. Хранимая процедура CLR
-- Увелчение мощности двигателя заданного типа
drop procedure if exists update_power_for_type;

create or replace procedure update_power_for_type(proc int, br text) as
$$
    plan = plpy.prepare("update engines set power = power + $1 where type = $2;", ["int", "text"])
    plpy.execute(plan, [proc, br])
$$ language plpython3u;

select *
from engines
where type = 'Hybrid';

call update_power_for_type(-10, 'Hybrid');


-- 5. Триггер CLR
-- Пишем в консоль об изменении
drop function if exists update_trigger_CLR cascade;

create or replace function update_trigger_CLR()
returns trigger
as $$
    plpy.notice("--------------------------------")
    plpy.notice("New: {}".format(TD["new"]))
    plpy.notice("Old: {}".format(TD["old"]))
    plpy.notice("--------------------------------")
$$ language plpython3u;

-- Создаем триггер
create trigger update_CLR
after update on cars
for each row
execute procedure update_trigger_CLR();

-- Запрос, после которого сработает триггер
update cars
set brand = 'Beast'
where brand like '%Bugatti%';

update cars
set brand = 'Bugatti'
where brand like '%Beast%';

-- Проверка наличия калин
select *
from cars
where brand like '%Beast%' or brand like 'Bugatti';


-- 6. Определяемый пользователем тип данных CLR
drop type if exists price_brands cascade ;

create type price_brands as
(
    brand TEXT,
    model TEXT,
    year_of_production INT,
    price INT
);

-- Инфа об автосалонах дилерах заданного бренда
drop function if exists brand_prices;

create or replace function brand_prices(br text)
returns setof price_brands as
$$
	plan = plpy.prepare("select c.brand, c.model, c.year_of_production, p.price from cars as c join cars_prices as p on c.vin = p.vin	where brand = $1;", ["text"])
	res = plpy.execute(plan, [br])
	if res is not None:
		return res
$$ language plpython3u;

select * from brand_prices('Porsche');
