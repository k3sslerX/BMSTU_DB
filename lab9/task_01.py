import psycopg2
import redis
from config import *
import json

conn = psycopg2.connect(
    dbname=DB_NAME, 
    user=DB_USER, 
    password=DB_PASS, 
    host=DB_HOST, 
    port=DB_PORT
)
cursor = conn.cursor()

r = redis.Redis(host='localhost', port=6379, db=0)


def get_top_engines():
    top_engines = r.get('top_engines')
    if top_engines:
        print("Данные из кэша.")
        return json.loads(top_engines)
    print('Запрос к БД.')
    query = '''
        SELECT e.engine_serial, e.type, e.power
        FROM engines as e
        ORDER BY e.power DESC
        LIMIT 10;
    '''
    cursor.execute(query)
    top_engines = cursor.fetchall()
    r.setex('top_engines', 60, json.dumps(top_engines))

    return top_engines


print(get_top_engines())
cursor.close()
conn.close()
