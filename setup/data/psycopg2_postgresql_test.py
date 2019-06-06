import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user='app_user',
                                    password='password',
                                    host='127.0.0.1',
                                    port='5432',
                                    database='price_test')

    cursor = connection.cursor()

    create_table_query = '''CREATE TABLE test
            (ID INT PRIMARY KEY NOT NULL,
            CLOSE INT NOT NULL,
            DATE INT NOT NULL);'''

    cursor.execute(create_table_query)
    connection.commit()
    print('actually worked')

except (Exception, psycopg2.Error) as error:
    print('Error connecting to postgres', error)

finally:
    if(connection):
        cursor.close()
        connection.close()
        print('Postgres connection closed')
