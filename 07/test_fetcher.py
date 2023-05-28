import unittest
from unittest.mock import patch
from unittest import IsolatedAsyncioTestCase

import aiohttp

from fetcher import fetch_url, url_gen


class TestFetchUrl(IsolatedAsyncioTestCase):
    async def test_fetch_url(self):
        urls = ["http://google.com", "http://change.org"]
        results = []

        async with aiohttp.ClientSession() as session:
            await fetch_url(session, iter(urls), results)

        # проверим что результаты записались в нужном количестве
        # и с нужными данными
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0][0], "http://google.com")
        self.assertEqual(results[1][0], "http://change.org")


class TestFetcherGenerator(unittest.TestCase):
    def setUp(self) -> None:
        self.urls = ["http://google.com", "http://change.org", "http://vk.com"]

    @patch("builtins.open")
    def test_url_gen(self, mock_open):
        # берем мок файла
        mock_file = mock_open.return_value.__enter__.return_value

        # мокаем чтение из файла
        mock_file.readline.side_effect = self.urls

        gen = url_gen("some_file")

        self.assertEqual(next(gen), self.urls[0])
        self.assertEqual(next(gen), self.urls[1])
        self.assertEqual(next(gen), self.urls[2])
