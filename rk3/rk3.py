import psycopg2
from datetime import datetime
from peewee import *

con = PostgresqlDatabase(
    database='postgres',
    user='postgres',
    password='1337',
    host='localhost',
    port='5432'
)
cur = con.cursor()


class BaseModel(Model):
    class Meta:
        database = con


class Satellite(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField()
    date = DateField()
    country = TextField()


class Flight(BaseModel):
    satellite_id = ForeignKeyField(Satellite, constraint_name='satellite_id', backref='satellite')
    day = DateField()
    launch_date = DateField()
    launch_time = DateField()
    type2 = IntegerField()


def str_to_date(str_date: str) -> datetime.date:
    return datetime.strptime(str_date, '%Y-%m-%d').date()


def query_1():
    countries = Satellite.select(Satellite.country).where(Satellite.date.month == 5)

    print("Query 1 ORM result:")
    for country in countries:
        print(f'    {country.country}')
    print()

    cur.execute("select country from satellite where date_part('month', satellite.date) = 5")

    print("Query 1 SQL result:")
    print(cur.fetchall())
    print()


def query_2():
    satellites = (Satellite.select(Satellite.name).join(
        Flight, on=(Satellite.id == Flight.satellite_id)).where(
        Flight.launch_date.year == 2050).order_by(Flight.launch_date.desc(), Flight.launch_time.desc()).limit(1))

    print("Query 2 ORM result:")
    for satellite in satellites:
        print(f'    {satellite.name}')
    print()

    cur.execute("select s.name from satellite s join flight f on s.id = f.satellite_id "
                "where date_part('year', launch_date) = 2050 order by launch_date desc, launch_time desc limit 1")

    print("Query 2 SQL result:")
    print(cur.fetchall())
    print()


def query_3():
    satellites = (Satellite.select(Satellite.name, Flight.launch_date, Flight.launch_time, Flight.type2).join(
        Flight, on=(Satellite.id == Flight.satellite_id)).order_by(Flight.launch_date.desc()))
    launch_dates = []
    land_dates = []
    satellites_out = []
    for satellite in satellites:
        if satellite.flight.type2 == 1:
            launch_dates.append([satellite.name, satellite.flight.launch_date])
        else:
            land_dates.append([satellite.name, satellite.flight.launch_date])
    for i in range(len(land_dates)):
        first = True
        for j in range(len(land_dates)):
            if launch_dates[i][0] == land_dates[j][0]:
                if first:
                    first = False
                    timedelta = land_dates[j][1] - launch_dates[i][1]
                    if timedelta.days >= (365 * 7):
                        satellites_out.append(launch_dates[i][0])

    print("Query 3 ORM result:")
    for satellite in satellites_out:
        print(f'    {satellite.name}')
    print()

    cur.execute("""
    with FlightPeriods as (
    select 
        satellite_id,
        MIN(launch_date) AS first_launch,
        MAX(launch_date) AS last_launch
    from
        flight
    where
        type2 = 1
    group by 
        satellite_id
    ),
    ContinuousWork AS (
    select
        fp.satellite_id,
        fp.first_launch,
        fp.last_launch,
        EXTRACT(YEAR FROM AGE(fp.last_launch, fp.first_launch)) AS years_of_work
    from 
        FlightPeriods fp
    left join 
        flight f ON f.satellite_id = fp.satellite_id
           AND f.type2 = 0 -- исключаем "прилет"
    group by
        fp.satellite_id, fp.first_launch, fp.last_launch
    having
        COUNT(f.satellite_id) = 0 AND  -- отсутствие событий "прилет"
        EXTRACT(YEAR FROM AGE(fp.last_launch, fp.first_launch)) >= 7 -- минимум 7 лет работы
    )

    select distinct
        s.name
    from
        satellite s
    join 
        ContinuousWork cw ON s.id = cw.satellite_id
    """)

    print('Query 3 SQL result:')
    print(cur.fetchall())
    print()


if __name__ == "__main__":
    query_1()
    query_2()
    query_3()
