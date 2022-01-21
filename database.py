import psycopg2, time


def measure_working_time(func):
    def wrapper(*args):
        start = time.time()
        f = func(*args)
        end = time.time()-start
        print(func.__name__ + ' worked for', end)
        return f
    return wrapper


# Connect to your postgres DB
conn = psycopg2.connect(
host='localhost', port='5432', database='filestorage',
user='alex', password='postgres')


@measure_working_time
def add_to_db(creation_time, filename):
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS filestorage(
                    id SERIAL PRIMARY KEY,
                    access_time text,
                    link_to_source text,
                    link_to_output_arch text);""")
        cur.execute(f"""INSERT INTO filestorage(access_time, link_to_source, link_to_output_arch)
                    VALUES ('{creation_time[:-7]}', 'source-{filename}.txt', '{filename}.zip');""")
        conn.commit()
    return 'DONE'


def delete_excessive_entries():
    pass

@measure_working_time
def select_from_db():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM filestorage ORDER BY id DESC LIMIT 20")
        result = cur.fetchall()
        return result


# Close connection
# conn.close()

# print(add_to_db('54564561564561', 'asdasfadsfsd'))
# print(select_from_db())
