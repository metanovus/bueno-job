import streamlit as st
from utils.resume_loader import load_resume_from_file
from utils.qdrant_client import QdrantClient, save_to_qdrant, search_qdrant
from utils.hh_api import get_vacancies, find_vacations
from utils.vectorizer import SentenceTransformer

st.title("BuenoJob - Умный поиск вакансий")

resume_file = st.file_uploader("Загрузите резюме (формат .txt)", type=["txt"])

if resume_file is not None:
    resume_text = load_resume_from_file(resume_file)
    model = SentenceTransformer('DeepPavlov/rubert-base-cased-sentence')
    resume_vector = model.encode(resume_text).tolist()
    st.write(f"Резюме загружено. Длина текста: {len(resume_text)} символов.")
else:
    st.warning('Загрузите резюме для продолжения.')

qdrant_url = st.text_input('Введите ссылку на Qdrant')
qdrant_api_key = st.text_input('Введите токен API от Qdrant')
collection_name = st.text_input('Введите название коллекции')

total_vacancies = st.number_input(
    'Введите количество вакансий для парсинга (чтобы вывести все, оставьте поле пустым)',
    min_value=0,
    step=1,
    value=0
)

hh_areas = {
    1: "Москва", 2: "Санкт-Петербург", 3: "Новосибирск", 4: "Екатеринбург",
    5: "Нижний Новгород", 6: "Казань", 7: "Челябинск", 8: "Самара", 9: "Омск",
    10: "Ростов-на-Дону", 11: "Уфа", 12: "Красноярск", 13: "Воронеж", 14: "Пермь",
    15: "Волгоград", 16: "Краснодар", 17: "Саратов", 18: "Тюмень", 19: "Тольятти", 113: "Россия (все регионы)"
}

areas = st.multiselect("Выберите локации", options=[area for area in hh_areas.values()])
specialization = st.text_input('Введите название специальности (например, "аналитик данных")', 'аналитик данных')
top_k = st.selectbox("Количество вакансий в топе", [5, 10, 20, 30, 50, 100, 200], index=1)

if st.button('Поиск вакансий'):
    qdrant_client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)

    find_vacations(text=specialization, areas=areas, total_vacancies=total_vacancies, qdrant_client=qdrant_client,
                   collection_name=collection_name, hh_area=hh_area)

    similarities = search_qdrant(qdrant_client, collection_name, resume_vector, top_k)

    if similarities:
        similarities_df = pd.DataFrame(similarities)
        st.write(f"Топ-{top_k} похожих вакансий:")
        st.dataframe(similarities_df)
    else:
        st.warning("Нет похожих вакансий.")
