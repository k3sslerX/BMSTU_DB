import psycopg2
import redis
import time
import json
import random
from threading import Thread, Lock
import matplotlib.pyplot as plt
import os
import string
from config import *

output_dir = "grhs"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def generate_random_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

conn = psycopg2.connect(
    dbname=DB_NAME, 
    user=DB_USER, 
    password=DB_PASS, 
    host=DB_HOST, 
    port=DB_PORT
)
cursor = conn.cursor()

r = redis.Redis(host='localhost', port=6379, db=0)

cache_durations = []
db_durations = []
ids = []

db_lock = Lock()
flag = True


def create_temp_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS redis_table
        (id INT,
        name TEXT,
        value BIGINT)""")
    for i in range(3000):
        cursor.execute(f"""
                    INSERT INTO redis_table (id, name, value)
                    VALUES (%s, %s, %s)
            """, (i, generate_random_string(), random.randint(0, 1000)))
        conn.commit()
        ids.append(i)


def get_top_data_from_db():
    cursor.execute("""
        SELECT id
        FROM redis_table
        ORDER BY value DESC
        LIMIT 10;
    """)
    try:
        return cursor.fetchall()
    except:
        return None


def cache_top_data():
    top_data = get_top_data_from_db()
    r.setex('top_data', 1800, json.dumps(top_data))


def get_top_data_from_cache():
    global flag
    cached_data = r.get('top_data')

    if cached_data and flag:
        return json.loads(cached_data)
    else:
        flag = True
        cache_top_data()
        return get_top_data_from_cache()


def insert_random_data():
    global flag
    new_id = len(ids)
    cursor.execute(f"""
            INSERT INTO redis_table (id, name, value)
            VALUES (%s, %s, %s)
    """, (new_id, generate_random_string(), random.randint(0, 1000)))
    conn.commit()
    ids.append(new_id)

    flag = False


def delete_random_data():
    rand_id = random.choice(ids)
    ids.remove(rand_id)
    cursor.execute(f"DELETE FROM redis_table WHERE id = {rand_id}")
    conn.commit()
    global flag
    flag = False


def update_random_data():
    cursor.execute("UPDATE redis_table SET name = %s WHERE id = %s",
                   (generate_random_string(), random.choice(ids)))
    conn.commit()
    global flag
    flag = False


def cache_query():
    for _ in range(QUERIES_COUNT):
        with db_lock:
            start_time = time.time()
            get_top_data_from_cache()
            duration = time.time() - start_time
            cache_durations.append(duration)
        time.sleep(DELAY // 2)


def db_query():
    for _ in range(QUERIES_COUNT):
        with db_lock:
            start_time = time.time()
            get_top_data_from_db()
            duration = time.time() - start_time
            db_durations.append(duration)
        time.sleep(DELAY // 2)


def data_insert():
    for _ in range(QUERIES_COUNT // 2):
        with db_lock:
            insert_random_data()
        time.sleep(DELAY)


def data_delete():
    for _ in range(QUERIES_COUNT // 2):
        with db_lock:
            delete_random_data()
        time.sleep(DELAY)


def data_update():
    for _ in range(QUERIES_COUNT // 2):
        with db_lock:
            update_random_data()
        time.sleep(DELAY)


def graph_insert():
    global cache_durations, db_durations, flag
    cache_durations, db_durations = [], []
    flag = True

    cache_thread = Thread(target=cache_query)
    db_thread = Thread(target=db_query)
    insert_thread = Thread(target=data_insert)

    cache_thread.start()
    db_thread.start()
    insert_thread.start()

    cache_thread.join()
    db_thread.join()
    insert_thread.join()

    avg_cache_duration = sum(cache_durations) / len(cache_durations)
    avg_db_duration = sum(db_durations) / len(db_durations)

    print("Среднее время выполнения запроса к кэшу:", avg_cache_duration)
    print("Среднее время выполнения запроса к базе данных:", avg_db_duration)

    labels = ['Кэш', 'БД']
    avg_durations = [avg_cache_duration, avg_db_duration]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, avg_durations, color=['blue', 'green'], edgecolor='black')

    plt.title('Среднее время выполнения запросов при вставке данных в БД')
    plt.ylabel('Время (сек)')
    plt.xlabel('Тип запроса')

    for i, value in enumerate(avg_durations):
        plt.text(i, value + 0.01, f'{value:.6f}', ha='center', va='bottom')

    plt.savefig(os.path.join(output_dir, 'insert.png'))
    plt.close()

    print(f"График сохранён в папку {output_dir} под именем 'insert.png'")


def graph_just():
    global cache_durations, db_durations, flag
    cache_durations, db_durations = [], []
    flag = True

    cache_thread = Thread(target=cache_query)
    db_thread = Thread(target=db_query)

    cache_thread.start()
    db_thread.start()

    cache_thread.join()
    db_thread.join()

    avg_cache_duration = sum(cache_durations) / len(cache_durations)
    avg_db_duration = sum(db_durations) / len(db_durations)

    print("Среднее время выполнения запроса к кэшу:", avg_cache_duration)
    print("Среднее время выполнения запроса к базе данных:", avg_db_duration)

    labels = ['Кэш', 'БД']
    avg_durations = [avg_cache_duration, avg_db_duration]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, avg_durations, color=['blue', 'green'], edgecolor='black')

    plt.title('Среднее время выполнения запросов')
    plt.ylabel('Время (сек)')
    plt.xlabel('Тип запроса')

    for i, value in enumerate(avg_durations):
        plt.text(i, value + 0.01, f'{value:.6f}', ha='center', va='bottom')

    plt.savefig(os.path.join(output_dir, 'just.png'))
    plt.close()

    print(f"График сохранён в папку {output_dir} под именем 'just.png'")


def graph_delete():
    global cache_durations, db_durations, flag
    cache_durations, db_durations = [], []
    flag = True

    cache_thread = Thread(target=cache_query)
    db_thread = Thread(target=db_query)
    delete_thread = Thread(target=data_delete)

    cache_thread.start()
    db_thread.start()
    delete_thread.start()

    cache_thread.join()
    db_thread.join()
    delete_thread.join()

    avg_cache_duration = sum(cache_durations) / len(cache_durations)
    avg_db_duration = sum(db_durations) / len(db_durations)

    print("Среднее время выполнения запроса к кэшу:", avg_cache_duration)
    print("Среднее время выполнения запроса к базе данных:", avg_db_duration)

    labels = ['Кэш', 'БД']
    avg_durations = [avg_cache_duration, avg_db_duration]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, avg_durations, color=['blue', 'green'], edgecolor='black')

    plt.title('Среднее время выполнения запросов при удалении данных в БД')
    plt.ylabel('Время (сек)')
    plt.xlabel('Тип запроса')

    for i, value in enumerate(avg_durations):
        plt.text(i, value + 0.01, f'{value:.6f}', ha='center', va='bottom')

    plt.savefig(os.path.join(output_dir, 'delete.png'))
    plt.close()

    print(f"График сохранён в папку {output_dir} под именем 'delete.png'")


def graph_update():
    global cache_durations, db_durations, flag
    cache_durations, db_durations = [], []
    flag = True

    cache_thread = Thread(target=cache_query)
    db_thread = Thread(target=db_query)
    update_thread = Thread(target=data_delete)

    cache_thread.start()
    db_thread.start()
    update_thread.start()

    cache_thread.join()
    db_thread.join()
    update_thread.join()

    avg_cache_duration = sum(cache_durations) / len(cache_durations)
    avg_db_duration = sum(db_durations) / len(db_durations)

    print("Среднее время выполнения запроса к кэшу:", avg_cache_duration)
    print("Среднее время выполнения запроса к базе данных:", avg_db_duration)

    labels = ['Кэш', 'БД']
    avg_durations = [avg_cache_duration, avg_db_duration]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, avg_durations, color=['blue', 'green'], edgecolor='black')

    plt.title('Среднее время выполнения запросов при обновлении данных в БД')
    plt.ylabel('Время (сек)')
    plt.xlabel('Тип запроса')

    for i, value in enumerate(avg_durations):
        plt.text(i, value + 0.01, f'{value:.6f}', ha='center', va='bottom')

    plt.savefig(os.path.join(output_dir, 'update.png'))
    plt.close()

    print(f"График сохранён в папку {output_dir} под именем 'update.png'")


if __name__ == '__main__':
    create_temp_table()
    graph_insert()
    graph_just()
    graph_delete()
    graph_update()
    cursor.execute("DROP TABLE IF EXISTS redis_table")
    conn.commit()
    cursor.close()
    conn.close()
