import json
import unittest
from unittest.mock import patch, MagicMock

from faker import Faker

from json_parser import parse_json


class TestJsonParser(unittest.TestCase):
    @patch('json_parser.callback')
    def test_valid_json(self, callback_mock: MagicMock):
        simple_json = '{"key1": "Word1 word2", "key2": "word2 word3"}'

        parse_json(simple_json, ['key1'], ['word2'], callback_mock)
        callback_mock.assert_called_once_with('key1', 'word2')

        parse_json(simple_json, ['key2'], ['word2'], callback_mock)
        callback_mock.assert_called_with('key2', 'word2')

    def test_invalid_callback(self):
        with self.assertRaises(TypeError) as context:
            parse_json('{"key1": "string"}',
                       keyword_callback=None)
            self.assertTrue('Функция-обработчик не может быть None'
                            in context.exception)

    def test_invalid_json(self):
        with self.assertRaises(ValueError) as context:
            parse_json('{"key1": string"}')
            self.assertTrue('Передана невалидная JSON-строка'
                            in context.exception)

    @patch('json_parser.callback')
    def test_empty_json(self, callback_mock: MagicMock):
        parse_json('{}')
        callback_mock.assert_not_called()

    @patch('json_parser.callback')
    def test_no_match_in_json(self, callback_mock: MagicMock):
        fake = Faker(locale='RU_ru')
        data = {
            'поле_1': fake.sentence(),
            'поле_2': fake.sentence(),
            'поле_3': fake.sentence(),
            'поле_4': fake.sentence(),
            'поле_5': fake.sentence()
        }

        json_data_str = json.dumps(data)

        # вызываем с полем, которого нет в JSON,
        # но со словами, которые есть
        parse_json(json_data_str,
                   required_fields=['поле_0'],
                   keywords=data['поле_1'].split(),
                   keyword_callback=callback_mock)

        callback_mock.assert_not_called()

        # вызываем с полями, которые есть в JSON,
        # но со словами, которых в них нет
        # (англ. слов в тексте точно не будет, так как
        # в Faker() установлена российская локализация)

        parse_json(json_data_str,
                   required_fields=['поле_1', 'поле_2'],
                   keywords=['not_russian_word'],
                   keyword_callback=callback_mock)

        callback_mock.assert_not_called()

    @patch('json_parser.callback')
    def test_without_keywords(self, callback_mock: MagicMock):
        fake = Faker(locale='RU_ru')
        data = {
            'поле_1': fake.sentence(),
            'поле_2': fake.sentence()
        }

        parse_json(json.dumps(data),
                   required_fields=['поле_2'],
                   keyword_callback=callback_mock)

        # проверим, что функция вызывается столько раз,
        # сколько слов в строке
        self.assertEqual(callback_mock.call_count,
                         len(data['поле_2'].split()))

    @patch('json_parser.callback')
    def test_without_req_fields(self, callback_mock: MagicMock):
        fake = Faker(locale='RU_ru')
        data = {
            'поле_1': fake.sentence(),
            'поле_2': fake.sentence(),
            'поле_3': fake.sentence(),
            'поле_4': fake.sentence(),
            'поле_5': fake.sentence()
        }

        parse_json(json.dumps(data),
                   keywords=[
                       data['поле_1'].split()[0],
                       data['поле_2'].split()[0],
                   ],
                   keyword_callback=callback_mock)

        expected_calls = [
            unittest.mock.call("поле_1", data['поле_1'].split()[0]),
            unittest.mock.call("поле_2", data['поле_2'].split()[0])
        ]
        self.assertEqual(expected_calls, callback_mock.call_args_list)

    @patch('json_parser.callback')
    def test_without_any_filtration(self, callback_mock: MagicMock):
        fake = Faker(locale='RU_ru')
        data = {
            'поле_1': fake.sentence(),
            'поле_2': fake.sentence()
        }

        parse_json(json.dumps(data),
                   keyword_callback=callback_mock)

        # проверим, что функция вызывается столько раз,
        # сколько слов во всех строках
        expected_nb_of_calls = 0
        for value in data.values():
            expected_nb_of_calls += len(value.split())

        self.assertEqual(callback_mock.call_count,
                         expected_nb_of_calls)
