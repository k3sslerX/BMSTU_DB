select *
from cars join cars_prices on cars.vin = cars_prices.vin;

-- Скалярная функция
-- Применить скидку ко всем автомобилям
create or replace function PriceSale(price int, sale int)
returns int as $$
begin
    return price * (1 - sale::real / 100);
end;
$$ language plpgsql;

select brand, model, price, PriceSale(price, 25)
from cars join cars_prices on cars.vin = cars_prices.vin;


-- Подставляемая табличная функция
-- Автомобили с двигателем заданной мощности
create or replace function MakeTableAuEng(pw int)
returns table (brand TEXT, model TEXT, power int, volume FLOAT) as $$
begin
    return query
    select c.brand, c.model , e.power, e.volume
    from cars as c join cars_engines as c_e on c.vin = c_e.vin join engines as e on c_e.engine_serial = e.engine_serial
    where e.power = pw;
end;
$$ language plpgsql;

select *
from MakeTableAuEng(150);


-- Многооператорная табличная функция
-- Автомобили заданного бренда или заданного года производства
create or replace function GetAutosByBrandOrProdYear(str varchar(30), num int)
returns table (vin TEXT, brand TEXT, model TEXT, prod_year int) as $$
begin
    return query
    select c.vin, c.brand, c.model, c.year_of_production
    from cars as c
    where c.brand = $1;

    return query
    select c.vin, c.brand, c.model, c.year_of_production
    from cars as c
    where c.year_of_production = $2;
end;
$$ language plpgsql;

select *
from GetAutosByBrandOrProdYear('BMW', 2000);


-- Рекурсивная функция или функция с рекурсивным ОТВ
-- Общая цена первых n автомобилей
create or replace function PriceSum(sum int, n int, amount int)
returns int as $$
declare
     sum int;
begin
    if n > amount then
        return 0;
    end if;
    select price
    into sum
    from cars_prices
    LIMIT 1 OFFSET n - 1;
    return sum + PriceSum(sum, n + 1, amount);
end;
$$ language plpgsql;

select *
from PriceSum(0, 1, 100);


-- Хранимая процедура
-- Обновление цены на заданный процент у указанного бренда
create or replace procedure UpdatePriceForBrand(proc int, br TEXT)
as $$
begin
    update cars_prices
    set price = price * (1 + proc::real / 100)
    where exists (
        select vin
        from cars
        where brand = br);
end;
$$ language plpgsql;

call UpdatePriceForBrand(20, 'BMW');

select *
from cars join cars_prices on cars.vin = cars_prices.vin
where brand = 'BMW';


-- Рекурсивная хранимая процедура
-- Вывод кол-ва автомобилей произведенных в указанный период
create or replace procedure CountCarsBetweenYears(startYear int, endYear int, in count int)
as $$
declare
    num int;
begin
    if startYear > endYear then
        raise notice '%', count;
        return;
    end if;

    select count(*) into num
    from cars
    where year_of_production = startYear;
    count := count + num;
    call CountCarsBetweenYears(startYear + 1, endYear, count);
end;
$$ language plpgsql;

-- Вывод
create or replace procedure CountCarsBetweenYearsPrint(startYear int, endYear int)
as $$
begin
    raise notice 'Cars been produced between % and % years: ', startYear, endYear;
    call CountCarsBetweenYears(startYear, endYear, 0);
end;
$$ language plpgsql;

call CountCarsBetweenYearsPrint(2020, 2024);


-- Хранимая процедура с курсором
-- Названия моделей, имеющих заданную подстроку
create or replace procedure FindModel(input_text TEXT)
as $$
declare
	m_name varchar(50);
    myCursor cursor
	for
        select model
		from cars
		where model like input_text;
begin
    open myCursor;
    loop
        fetch myCursor
        into m_name;
        exit when not found;
        raise notice 'Model =  %', m_name;
    end loop;
    close myCursor;
end
$$ language plpgsql;

call FindModel('%1%');


-- Хранимая процедура доступа к метаданным
-- Информация о типах полей заданной таблицы
create or replace procedure metaData(tablename varchar(100))
as $$
declare
	c_name varchar(50);
	d_type varchar(50);
    myCursor cursor
	for
        select column_name, data_type
		from information_schema.columns
        where table_name = tablename;
begin
    open myCursor;
    loop
		fetch myCursor
        into c_name, d_type;
		exit when not found;
        raise notice 'column = %; dtype = %', c_name, d_type;
    end loop;
	close myCursor;
end;
$$ language plpgsql;

call metaData('engines');


-- Триггер AFTER
-- Создаем log таблицу
create table upd_info(
    updated_vin varchar(17),
    last_date timestamp,
    last_user text);

-- Создаем функцию для триггера
create or replace function UpdateTrigger()
returns trigger
as $$
begin
	raise notice 'New =  %', new;
    raise notice 'Old =  %', old;
	insert into upd_info(updated_vin, last_date, last_user)
    values(new.vin, current_timestamp, current_user);
	return new;
end
$$ language plpgsql;

-- Создаем триггер
create trigger update_my
after update on cars
for each row
execute procedure updateTrigger();

-- Запрос, после которого сработает триггер
update cars
set model = 'Beast'
where model like '%Bolide%';

update automobiles
set model = 'Bugatti'
where model like '%Bolide%';

-- Проверка наличия калин
select *
from automobiles
where model like '%Bolide%' or model like 'Beast';

select *
from upd_info;

drop table upd_info;


-- Тригер INSTEAD OF
-- Сделать поле с инфой об удалении
alter table cars add column deleted bool;

-- Создаем представление
create view cars_view as
select *
from cars;

--Создаем функцию для триггера
create or replace function DeleteAutos()
returns trigger
as $$
begin
    update cars_view
    set deleted = true
    where cars_view.vin = old.vin;
    return new;
end
$$ language plpgsql;

--Создаем триггер
create trigger deleteAutosTrigger
instead of delete on cars_view
for each row
execute procedure DeleteAutos();

--Пытаемся удалить кортеж по условию
delete from cars_view
where year_of_production = 2003;

select *
from cars_view
where year_of_production = 2003;

select *
from cars
where year_of_production = 2003;


-- Защита
create or replace function getCarsFromShowroom(showroom TEXT)
returns table (vin TEXT, brand TEXT, model TEXT, name TEXT) as $$
begin
	return query
	select c.vin, c.brand, c.model, s.name
	from cars as c join cars_engines_showrooms as ces on c.vin = ces.vin join showrooms as s on s.ogrn = ces.ogrn
	where s.name = $1;
end;
$$ language plpgsql;

select *
from getCarsFromShowroom('Smith LLC');
