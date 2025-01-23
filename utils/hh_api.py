import requests
from typing import List, Dict, Optional
import re


BASE_URL = "https://api.hh.ru/vacancies"

def get_vacancies(
    text: str = "аналитик данных",
    experience: str = "noExperience",
    area: int = 113,
    page: int = 0,
    per_page: int = 10
) -> Optional[Dict]:
    """
    Получает список вакансий с hh.ru.

    :param text: Ключевые слова для поиска вакансий.
    :param experience: Уровень опыта работы (например, "noExperience").
    :param area: Регион поиска вакансий.
    :param page: Номер страницы для пагинации.
    :param per_page: Количество вакансий на странице.
    :return: JSON-объект с вакансиями или None в случае ошибки.
    """
    params = {
        "text": text,
        "experience": experience,
        "area": area,
        "page": page,
        "per_page": per_page
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        vacancies = response.json()

        for item in vacancies['items']:
            vacancy_response = requests.get(f"https://api.hh.ru/vacancies/{item['id']}")
            vacancy_response.raise_for_status()
            item['full_description'] = re.sub(r'<\w+>|<\/\w+>|&quot', '', vacancy_response.json()['description'])
        return vacancies
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
    except:
        print('Произошла ошибка')
        return None


def find_vacations(
        hh_area: Dict[int, str],
        text: str = 'Аналитик данных',
        experience: str = "noExperience",
        areas: List[int] = [113],
        total_vacancies=None
) -> None:
    """
    Загружает вакансии с hh.ru, векторизует их и сохраняет в Qdrant.

    :param hh_area: Словарь с регионами (формат: целое число - наименование региона)
    :param per_page: Количество вакансий на странице.
    :param text: Ключевые слова для поиска вакансий.
    :param total_pages: Количество страниц для загрузки вакансий.
    :param experience: Уровень опыта работы.
    :param area: Регион поиска вакансий.
    :param total_vacancies: Сколько всего вакансий загружать (вместе взятых со всех городов)
    """
    total_vacancies_loaded = 0
    total_vacancies_per_area = total_vacancies

    for area in areas:
        if total_vacancies_loaded >= 1000:
            break
        print(f"Processing area {hh_areas[area]}...")

        total_vacancies = total_vacancies_per_area

        if total_vacancies is None:
            total_vacancies = get_total_vacancies(text, experience,
                                                  area)  # если число вакансий 0, смотрим, сколько всего у нас может быть
        else:
            total_vacancies_check = get_total_vacancies(text, experience,
                                                        area)  # если указан не 0, проверяем, сколько вообще вакансий есть
            if total_vacancies_check < total_vacancies and total_vacancies_check > 0:
                print(f"Found only {total_vacancies_check} vacancies in area {hh_areas[area]}...")
                total_vacancies = total_vacancies_check  # если число найденных вакансий меньше введённых, то парсим число найденных
            elif total_vacancies_check == 0:
                print(f"No vacancies in area {hh_areas[area]}...")
                break

        per_page = determine_pages_per_view(total_vacancies)
        total_pages = (total_vacancies + per_page - 1) // per_page

        print('per_page:', per_page, 'total_pages:', total_pages, 'total_vacancies:', total_vacancies)

        for page in range(total_pages):
            print(f"Fetching page {page + 1} for area {hh_areas[area]}...")
            if page == total_pages - 1:
                per_page = total_vacancies % per_page or per_page
                print('per_page:', per_page)

            vacancies = get_vacancies(text=text, per_page=per_page, page=page, experience=experience, area=area)
            if not vacancies:
                print(f"No vacancies found for area {hh_areas[area]}, page {page + 1}.")
                break

            print(f"Vectorizing vacancies for area {hh_areas[area]}, page {page + 1}...")
            descriptions = [item['full_description'] for item in vacancies['items'] if item['full_description']]
            vacancies_vectors = model.encode(descriptions)

            print(f"Saving vacancies for area {hh_areas[area]}, page {page + 1} to Qdrant...")
            save_to_qdrant(vacancies_vectors, vacancies, qdrant_client, collection_name)

            total_vacancies_loaded += per_page

            if total_vacancies_loaded >= 1000:
                break

            print('total_vacancies_loaded:', total_vacancies_loaded)

        print(f"Finished processing area {hh_areas[area]}.\n")