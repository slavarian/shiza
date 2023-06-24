
import psycopg2
from psycopg2 import Error

from psycopg2 import OperationalError

def create_database():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="admin",
                                      host="localhost",
                                      port="5432")
        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute("SELECT datname FROM pg_catalog.pg_database WHERE datname = 'mydata'")
        result = cursor.fetchone()

        if result is None:
            cursor.execute("CREATE DATABASE mydata")
            print("База данных успешно создана")
        else:
            print("База данных уже существует")
    except OperationalError as error:
        print("Ошибка при создании базы данных:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()

create_database()


class Create_table:
    try:
        

        connection = psycopg2.connect(user="postgres",
                                    password="admin",
                                    host="localhost",
                                    port="5432",
                                    database="mydata")

        cursor = connection.cursor()
        create_table_query = (
                    '''
                    CREATE TABLE IF NOT EXISTS users(
                        id SERIAL PRIMARY KEY,
                        login VARCHAR(50) NOT NULL UNIQUE,
                        email VARCHAR(50) NOT NULL UNIQUE,
                        password VARCHAR(50) NOT NULL,
                        password2 VARCHAR(50) NOT NULL,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        author VARCHAR(50) NOT NULL
                    );
                    CREATE TABLE IF NOT EXISTS articles(
                        id SERIAL PRIMARY KEY,
                        articles_author VARCHAR(50) NOT NULL,
                        article_title VARCHAR(50) NOT NULL,
                        articles_info VARCHAR(10000) NOT NULL,
                        total_rating INTEGER DEFAULT('0'),
                        vote_count INTEGER DEFAULT('0'),
                        datetime date DEFAULT CURRENT_DATE
                    );
                    CREATE TABLE IF NOT EXISTS comments(
                        id SERIAL PRIMARY KEY,
                        user_comment VARCHAR(40) NOT NULL,
                        articles_id INTEGER REFERENCES articles(id),
                        comment VARCHAR(200) NOT NULL,
                        datetime date DEFAULT CURRENT_DATE
                    );
                    '''
                )
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица успешно создана в PostgreSQL")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

Create_table()