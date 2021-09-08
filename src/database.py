import psycopg2
import psycopg2.extras

def fetch_records(conn_str, query):
    '''
    Query à base de dados, ligado pela conn_str

    Params:
        (str) conn_str    ->  string para conexão à base de dados
        (str) query       ->  query pretendida

    Return:
        (list) records     ->  lista de dicionarios com valores da query [{atributo1: valor1, atributo2: valor2}, ...]

    '''

    records = []

    with psycopg2.connect(conn_str) as conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(query)
        for row in cursor.fetchall():
            records.append(dict(row))

    return records