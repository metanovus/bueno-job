# BuenoJob - Умный поиск вакансий на основе резюме 🧑‍💻📄
Стадия проекта: *Альфа-версия (от 23.01.2025)*

Этот проект предоставляет решение для поиска вакансий на платформе hh.ru, которые наиболее похожи на резюме пользователя. С помощью модели машинного обучения (SentenceTransformer) и векторизации текста, мы создаём рекомендации для пользователя, основываясь на его резюме. Результаты поиска сохраняются в Qdrant, который используется для быстрого поиска схожих вакансий.

## Архитектура 🏗️ 
- **Сбор данных**: API-интеграция сайта hh.hu для получения данных вакансий, сохранение в векторной базе Qdrant.
- **Векторизация**: Векторизация резюме и описания вакансий с помощью модели 🤗 [rubert-base-cased-sentence](https://huggingface.co/DeepPavlov/rubert-base-cased-sentence).
- **Анализ**: Использование косинусной близости для поиска топ-k релевантных вакансий согласно вектору резюме.
- **Визуализация**: Выполнена с использованием фреймворка Streamlit.

## Технологии 🛠️
<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img src="https://go-skill-icons.vercel.app/api/icons?i=linux,python,pycharm,huggingface,qdrant,streamlit,pandas&theme=dark"/>
  </a>
</p>

## Описание 🌟
Веб-приложение позволяет пользователю:
- 📥 Загрузить резюме в формате `.txt`.
- 🔍 Ввести параметры для поиска вакансий (ключевые слова, локации, количество вакансий).
- 📈 Получить топ-результаты вакансий, похожих на резюме.

## Структура проекта 🗂️

```
bueno-job/
│
├── app.py                  # Главный файл запуска Streamlit
├── notebooks/
│   └── buenojob-notebook.ipynb     # Ноутбук проекта без визуализации
├── utils/
│   ├── __init__.py         # Инициализация пакета
│   ├── resume_loader.py    # Функции для загрузки и обработки резюме
│   ├── qdrant_client.py    # Функции для работы с Qdrant
│   ├── hh_api.py           # Функции для работы с API hh.ru
│   └── vectorizer.py       # Функции для векторизации текста
├── requirements.txt        # Список зависимостей для установки
└── README.md               # Документация
```

### Описание файлов 📄

1. **app.py**:
   Главный файл приложения, в котором реализован интерфейс Streamlit. Содержит формы для загрузки резюме, ввода данных о поиске вакансий и отображения результатов.

2. **utils/resume_loader.py**:
   Содержит функцию для загрузки текста резюме из загруженного файла.

3. **utils/qdrant_client.py**:
   Содержит функции для взаимодействия с Qdrant — хранения вакансий и выполнения поиска.

4. **utils/hh_api.py**:
   В этом файле находятся функции для работы с API hh.ru: получения списка вакансий по заданным критериям.

5. **utils/vectorizer.py**:
   Содержит функцию для векторизации текста с использованием модели Sentence-BERT.

6. **requirements.txt**:
   Содержит все зависимости, необходимые для работы проекта. Для установки зависимостей используйте команду:
   ```bash
   pip install -r requirements.txt
   ```

## Установка и запуск 🚀

1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:metanovus/bueno-job.git
   cd bueno-job
   ```

2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Запустите приложение:
   ```bash
   streamlit run app.py
   ```

   Перейдите в браузер по адресу, который будет указан в терминале, чтобы использовать приложение.

## Использование 📋

1. 📥 Загрузите файл с вашим резюме в формате `.txt`.
2. 🔎 Введите параметры для поиска вакансий, такие как:
   - Ключевые слова для поиска (например, "аналитик данных").
   - Локации для поиска вакансий (выберите один или несколько городов).
   - Количество вакансий для парсинга.
3. Нажмите кнопку **Поиск вакансий** и получите результаты — список вакансий, схожих с вашим резюме.
