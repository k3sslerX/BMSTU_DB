-- 1. Инструкция SELECT, использующая предикат сравнения
-- Суперкары дороже 10 миллионов
SELECT *
from cars as c join cars_prices as p on c.vin = p.vin
where c.body = 'Supercar'
    and p.price > 10000000;

-- 2. Инструкция SELECT, использующая предикат BETWEEN
-- Машины, выпущенные с 2020 по 2024 год
SELECT *
from cars as c
where c.year_of_production BETWEEN 2020 AND 2024;

-- 3. Инструкция SELECT, использующая предикат LIKE
-- Все автомобили марки Porsche модели 911
SELECT *
from cars as c
where c.brand = 'Porsche' and c.model LIKE '%911%';

-- 4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом.
-- Автомобили с гибридным типом двигателя, мощностью более 1000 л.с.
SELECT c.vin, c.brand, c.model, e.type, e.power
from cars as c join cars_engines as c_e on c.vin = c_e.vin join engines as e on e.engine_serial = c_e.engine_serial
where c.vin in (select vin from cars_engines as c_e join engines as e on c_e.engine_serial = e.engine_serial
                where e.type = 'Hybrid' and e.power > 1000);

-- 5. Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом.
-- Все гибридные двигатели
SELECT e.engine_serial, e.type, e.power
from engines as e
where exists (select * from engines
              where type = 'Hybrid');

-- 6. Инструкция SELECT, использующая предикат сравнения с квантором.
-- Двигатели мощнее всех электродвигателей
SELECT e.engine_serial, e.type, e.power
from engines as e
where e.power > all(select power from engines
                    where type = 'Electro');

-- 7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов.
-- Средняя мощность бензиновых двигателей
SELECT e.engine_serial, e.type, avg(e.power) as avg_power
from engines as e
group by e.type;

-- 8. Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов.
-- Средняя старость седанов
SELECT c.vin, c.brand, c.model, c.body, (select avg(year_of_production) from cars where body = 'Sedan') as avg_year
from cars as c
where body = 'Sedan';

--  9. Инструкция SELECT, использующая простое выражение CASE.
-- Определить вид топлива
SELECT e.engine_serial, e.type,
    case e.type
        when 'Petrol' then 'Бензин'
        when 'Electro' then 'Зарядка'
        when 'Hybrid' then 'Специальная заправка'
    end as energy
from engines as e;

-- 10. Инструкция SELECT, использующая поисковое выражение CASE.
-- Определение класса стоимости машины
SELECT c.vin, c.brand, c.model, c.body, p.price,
    case
        when p.price < 5000000 then 'Average'
        when p.price < 10000000 then 'Expencive'
        else 'Very Expencive'
    end as price_class
from cars as c join cars_prices as p on c.vin = p.vin;

-- 11. Создание новой временной локальной таблицы из результирующего набора данных инструкции SELECT.
-- Создание таблицы двигатель - цена машины
CREATE temp table if not exists engine_prices as
select ce.vin, ce.engine_serial, p.price
from cars_engines as ce join cars_prices as p on ce.vin = p.vin;

select *
from engine_prices;

-- 12. Инструкция SELECT, использующая вложенные коррелированные подзапросы в качестве производных таблиц в предложении FROM.
-- Автомобили, которые продаются только в 1 салоне
SELECT *
from cars_engines_showrooms as ces1
where ces1.vin not in (
    select ces2.vin
    from cars_engines_showrooms as ces2
    where ces1.ogrn <> ces2.ogrn);

-- 13. Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3.
-- Машшины продюащиеся в салонах LTD
SELECT *
from cars as c
where c.vin in (
    select vin
    from cars_engines_showrooms as ces
    where ogrn in (
        select ogrn from showrooms as s
        where name LIKE '%Ltd%'))

-- 14. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY, но без предложения HAVING.
-- Максимальная и минимальная мощность каждой модели
SELECT c.brand, c.model, min(e.power) as min_power, max(e.power) as max_power
from cars as c join cars_engines as c_e on c.vin = c_e.vin join engines as e on e.engine_serial = c_e.engine_serial
group by c.brand;

-- 15. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY и предложения HAVING.
-- Машины дороже средней цены
SELECT c.brand, c.model, avg(p.price) as avg_price
from cars as c join cars_prices as p on c.vin = p.vin
group by c.brand
having avg(p.price) > (select avg(price) from cars_prices);

-- 16. Однострочная инструкция INSERT, выполняющая вставку в таблицу одной строки значений.
--
INSERT INTO showrooms (ogrn, name) values
('1111111111111', 'k3ssler motors');

-- 17. Многострочная инструкция INSERT, выполняющая вставку в таблицу результирующего набора данных вложенного подзапроса.
--


-- 18. Простая инструкция UPDATE.
-- Скидка 10 % на автомобили дороже 10 миллионов
UPDATE cars_prices
SET price = price / 100 * 90
WHERE price > 100000000;

-- 19. Инструкция UPDATE со скалярным подзапросом в предложении SET.
--
UPDATE engines
SET power = (select max(power)
            from engines
            where cylinders = 8)
where cylinders = 8
returning *;

-- 20. Простая инструкция DELETE.
-- Удалить все LTD салоны
DELETE from showrooms
where name like '%Ltd%';

-- 21. Инструкция DELETE с вложенным коррелированным подзапросом в предложении WHERE.
-- Удаление всех 12-ти цилиндровых двигателей
DELETE from engines
where engine_serial in (select engine_serial
                        from engines
                        where cylinders = 12)
returning *;

-- 22. Инструкция SELECT, использующая простое обобщенное табличное выражение
-- Бренды, машин которых больше чем в средем
with num_brands (brand, number) as (
    select brand, count(*)
    from cars
    group by brand
)
select *
from num_brands
where number > (select avg(number) from num_brands);

-- 24.  Оконные функции. Использование конструкций MIN/MAX/AVG OVER()
-- Средняя, минимальная и максимальная цена машин по брендам
SELECT c.brand, c.model, c.price,
    avg(p.price) over (partition by c.brand) as avg_brand_price,
    min(p.price) over (partition by c.brand) as min_brand_price,
    max(p.price) over (partition by c.brand) as max_brand_price
FROM cars as c join cars_prices as p on c.vin = p.vin;

-- 25. Оконные функции для устранения дублей
-- Дублирование цен, больших чем 10 мильенов
INSERT INTO prices VALUES (vin, price)
select vin, price
from prices
where price > 10000000;

-- Удаление дублей
with double_price (id, vin, price, r_n) as (
    select *,
    row_number() over (partition by vin, price, order by id) as r_n
    from prices
)

delete from prices
where id in (select id
    from double_price
    where double_price.r_n != 1)
    and id > 3000;