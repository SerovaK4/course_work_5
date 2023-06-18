from src.API import HeadHunterAPI
from src.DBManager import DBManager
from src.create_insert_db import create_db, insert_db


def main():
    is_create = input("Для создания новой базы данных введите 'yes': ")
    name_db = input("Введите имя базы данных: ")
    if is_create.lower() == 'yes':
        create_db(name_db)
        db_manager = DBManager(name_db)

        api = HeadHunterAPI(1)

        insert_db(db_manager, api)
        print(f"Создана база данных {name_db}. С сайта Head hunter загружены вакансии и работодатели")
    else:
        db_manager = DBManager(name_db)

    if db_manager:
        print("Для вывода статистики по вакансиям, выберите опции: ")
        print()
        print("1- для получения списка всех компаний и количества вакансий у каждой компании")
        print("2- для получения списока всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
        print("3- для получения средней зарплаты по вакансиям")
        print("4- для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям")
        print("5- для получения списка всех вакансий, в названии которых содержатся переданные в метод слова, например “python”")

        print("0 - для выхода из программы")
        option = input("Введите опции: ")
        while option != "0":
            if option == '1':
                data1 = db_manager.get_companies_and_vacancies_count()
                for item in data1:
                    print(f"В компании {item['name']}: {item['count']} вакансий")
            elif option == '2':
                data1 = db_manager.get_all_vacancies()
                for item in data1:
                    print(f"В компании: {item['name']}, вакансия: {item['vacancy']}, зарплата: {item['salary_to']}, ссылка: {item['url']} ")
            elif option == '3':
                data1 = db_manager.get_avg_salary()
                for item in data1:
                    print(f"Средняя зарплата по вакансиям: {int(item['salary_avg'])}")
            elif option == '4':
                data1 = db_manager.get_vacancies_with_higher_salary()
                for item in data1:
                    print(f" {item['vacancies']}")
            elif option == '5':
                word = input("Введите слово для фильтрации: ")
                data1 = db_manager.get_vacancies_with_keyword(word)
                for item in data1:
                    print(f" {item['vacancies']}")
            option = input("Введите опции: ")


if __name__ == '__main__':
    main()