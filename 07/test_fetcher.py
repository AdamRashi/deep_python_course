import asyncio
import unittest
from unittest.mock import patch, AsyncMock, MagicMock

import aiohttp

from fetcher import fetch_url, url_gen


class TestFetcher(unittest.TestCase):
    def setUp(self) -> None:
        self.urls = ["http://google.com", "http://change.org", "http://vk.com"]

    @patch("aiohttp.ClientSession.get")
    async def test_fetch_url(self, mock_response: MagicMock):
        # мокаем используемые методы, в том числе методы
        # контекстного менеджера
        mock_response.read = AsyncMock(return_value=b"TEST html text TEST")
        mock_response.__aexit__ = AsyncMock()
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)

        # создаём mock сессии, чтобы передать его в функцию
        mock_session = MagicMock()
        mock_session.get = AsyncMock(return_value=mock_response)

        # Вызываем fetch_url с замоканной клиентской сессией
        result = asyncio.run(fetch_url("test_url", mock_session))

        self.assertTrue(len(result) == 2)
        self.assertEqual(result[0], "test_url")
        self.assertEqual(result[1], [("TEST", 2)])

        mock_response.read.side_effect = aiohttp.ClientError
        mock_session = AsyncMock(return_value=mock_response)
        result = asyncio.run(fetch_url("test_url", mock_session))

        self.assertTrue(len(result) == 1)
        self.assertEqual(result, "test_url")

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
