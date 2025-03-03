-- create database rk3

create table if not exists satellite (
    id serial primary key ,
    name varchar not null,
    date date not null ,
    country varchar not null
);

create table if not exists flight (
    satellite_id int references satellite(id),
    launch_date date not null ,
    launch_time time not null ,
    day varchar not null,
    type2 int check (type2 in (0, 1)) not null
);

insert into satellite values (1, 'SIT-2086', '2050-01-01', 'Россия'),
                                 (2, 'Шицзян 16-02', '2049-12-01', 'Китай');

insert into flight values (1, '2050-05-11', '9:00', 'Среда', 1),
                              (1, '2051-06-14', '23:05', 'Среда', 0),
                              (1, '2051-10-10', '23:50', 'Вторник', 1),
                              (2, '2050-05-11', '15:15', 'Среда', 1),
                              (1, '2052-01-01', '12:15', 'Понедельник', 0);

select * from satellite;

-- 1. Кол-во полетов каждого спутника по убыванию
explain
select count(*) as cnt from flight f
group by satellite_id
order by cnt desc;

-- 2. Спутники, которые прилетели и улетели в том же месяце, что и были произведены
explain
select * from flight f
join (select date_trunc('month', date) as month from satellite s
	group by date_trunc('month', date))
on date_trunc('month', launch_date) = month;
