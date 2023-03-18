import unittest
import os
from generator import filter_lines

TEST_FILE_NAME = 'test_file.txt'


class TestFilterLines(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """
        Создаем единожды файл с текстом, который будет использоваться
        практически во всех тестах
        """
        with open(TEST_FILE_NAME, 'w', encoding='utf-8') as file:
            file.write('Do you want an apple\n')
            file.write('Sweet one\n')
            file.write('And a banana\n')
            file.write('From Panama\n')

    @classmethod
    def tearDownClass(cls) -> None:
        """
        После выполнения всех тестов, удаляем созданный файл
        """
        os.remove(TEST_FILE_NAME)

    def test_several_matches(self, ):
        """
        Случай, когда должны найтись совпадения
        """
        filter_words = ['apple', 'sweet', 'banana']
        expected_result = [
            'Do you want an apple',
            'Sweet one',
            'And a banana'
        ]
        result = list(filter_lines(TEST_FILE_NAME, filter_words))
        self.assertEqual(result, expected_result)

    def test_no_match(self):
        """
        Случай, когда совпадений нет
        """
        filter_words = ['there', 'is', 'no', 'such', 'words']
        result = list(filter_lines(TEST_FILE_NAME, filter_words))
        self.assertEqual(result, [])

    def test_empty_file(self):
        """
        Случай, когда файл пустой
        """

        file_name = 'empty_file.txt'
        filter_words = ['apple', 'sweet', 'banana']
        with open(file_name, 'w', encoding='utf-8'):
            pass
        results = list(filter_lines(file_name, filter_words))
        os.remove(file_name)

        self.assertEqual(results, [])

    def test_almost_matches(self):
        """
        Случай, когда слова "почти" совпадают со словами в тексте
        """
        filter_words = ['appel', 'sweetie', 'abanana']
        result = list(filter_lines(TEST_FILE_NAME, filter_words))
        self.assertEqual(result, [])

    def test_no_filter_words(self):
        """
        Случай, когда не переданы слова для фильтрации
        """
        result = list(filter_lines(TEST_FILE_NAME, []))
        self.assertEqual(result, [])

    def test_not_matching_case(self):
        """
        Случай, когда регистры слов для поиска и слов в тексте не совпадают
        """

        filter_words = ['aPpLe', 'SWEET', 'banana']
        expected_result = [
            'Do you want an apple',
            'Sweet one',
            'And a banana'
        ]
        result = list(filter_lines(TEST_FILE_NAME, filter_words))

        self.assertEqual(result, expected_result)
