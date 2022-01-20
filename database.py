import psycopg2


# Connect to your postgres DB
conn = psycopg2.connect(
host='localhost', port='5432', database='filestorage',
user='alex', password='postgres')


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


def select_from_db():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM filestorage ORDER BY id DESC LIMIT 20")
        result = cur.fetchall()
        return result


# Close connection
# conn.close()
# print(select_from_db())
# print(add_to_db('54564561564561', 'asdasfadsfsd'))
