import json
from typing import Optional


# функция-обработчик
def callback(key: str, word: str) -> None:
    """
        Функция-обработчик для пары значений: ключ и слово.

        :param key: Название поля JSON, содержащего слово
        :param word: Слово, найденное в поле JSON
        :return: None
    """
    print(f'{key}: {word}')


def parse_json(json_str: str,
               required_fields: Optional[list[str]] = None,
               keywords: Optional[list[str]] = None,
               keyword_callback=callback) -> None:
    """
        Функция принимает на вход строку в упрощенном формате JSON
        (где поле: str, значение: str), проходится по всем полям,
        переданным в required_fields (если required_fields не передано,
        то по всем полям JSON), и ищет совпадения. Если поле есть в
        переданном JSON, то происходит поиск слов в строке-значении,
        и для найденных слов пара значений (поле, слово) передаётся
        на вход функции-обработчику. Слова для поиска передаются в
        параметре keywords. Если слова для поиска не предоставлены,
        то используются все слова в строке-значении. Предполагается,
        что слова в строках разделены пробелами и ничем больше.

    :param json_str: Строка, в которой содержится json
    :param required_fields: Поля JSON, в которых необходимо производить поиск
    :param keywords: Ключевые слова, которые надо найти
    :param keyword_callback: Функция-обработчик, которая должна обработать пару
            значений: поле и слово
    :return: None
    """
    # если функция-обработчик не передана, то ничего не делаем
    if keyword_callback is None:
        raise TypeError('Функция-обработчик не может быть None')

    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as exc:
        raise ValueError('Передана невалидная JSON-строка') from exc

    # Если ключи-фильтры не переданы, то проходимся по всем ключам
    if not required_fields:
        required_fields = data.keys()

    for field in required_fields:
        # Если ключа нет в json'е, идём на следующую итерацию
        if field not in data:
            continue

        # Если ключевые слова не переданы, то обрабатываем все слова в строке
        if keywords:
            for word in filter(lambda w: w in keywords, data[field].split()):
                keyword_callback(field, word)
        else:
            for word in data[field].split():
                keyword_callback(field, word)
