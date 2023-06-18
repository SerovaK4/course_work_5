import psycopg2
from src.config import config


class DBManager:
    """
    класс будет подключаться к базе данных Postgres и получать статистику по вакансиям и работодателям
    """
    def __init__(self, name):
        db = config()
        self.host = db["host"]
        self.database = name
        self.user = db["user"]
        self.password = db["password"]
        self.conn = psycopg2.connect(database=self.database, user=self.user, host=self.host, password=self.password)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        query = 'select employees.name, count(*) from employees left join vacancies using(employee_id) group by employees.name'
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
        data_dict = [{"name": d[0], "count": d[1]} for d in data]
        return data_dict

    def get_all_vacancies(self):
            """
            Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
            """
            query = 'select employees.name, vacancies.name, salary_to, salary_from, vacancies.url from vacancies  left join employees using(employee_id)'

            conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
            with conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    data = cur.fetchall()
            data_dict = [{"name": d[0], "vacancy": d[1], "salary_to": d[2], "salary_from": d[3], "url": d[4]} for d in data]
            return data_dict

    @staticmethod
    def create_database(database_name: str, params: dict):
        """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях."""

        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE employees (
                            employee_id int PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            url VARCHAR(255),
                            vacancies_url VARCHAR(255),
                            area INTEGER,
                            description TEXT
                        )
                    """)

        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE vacancies (
                            vacancy_id int PRIMARY KEY,
                            employee_id INT REFERENCES employees(employee_id),
                            name VARCHAR NOT NULL,
                            url VARCHAR(255),
                            area varchar(50),
                            salary_to INTEGER,
                            salary_from INTEGER,
                            requirements TEXT
                        )
                    """)

        conn.commit()
        conn.close()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям

        """
        query = 'select (avg(salary_to) + avg(salary_from))/2  from vacancies  where salary_to !=0 or salary_from !=0'
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
        data_dict = [{"salary_avg": d[0]} for d in data]
        return data_dict

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        query = 'select name, salary_to, salary_from from vacancies group by name, salary_to, salary_from having (select (avg(salary_to) + avg(salary_from))/2  from vacancies  where salary_to !=0 or salary_from !=0)  < salary_to or (select (avg(salary_to) + avg(salary_from))/2  from vacancies  where salary_to !=0 or salary_from !=0) < salary_from'
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
        data_dict = [{"vacancies": d[0]} for d in data]
        return data_dict

    def get_vacancies_with_keyword(self, word):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова
        """
        keyword = "'" + '%' + word + '%' + "'"
        query = f'select name, requirements from vacancies where name like {keyword} or requirements like {keyword}'
        conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
        data_dict = [{"vacancies": d[0]} for d in data]
        return data_dict


