import psycopg2
import psycopg2.extras

def fetch_records(conn_str, query):
    records = []

    with psycopg2.connect(conn_str) as conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        for row in cursor.fetchall():
            records.append(dict(row))

    return records