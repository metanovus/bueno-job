def load_resume_from_file(file: str) -> str:
    """
    Загрузка текста резюме из файла.

    :param file: Загруженный файл.
    :return: Содержимое файла в виде строки.
    """
    return file.read().decode('utf-8').replace('\n\n', ' ').replace('\n', ' ')