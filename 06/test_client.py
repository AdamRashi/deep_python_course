import unittest

from unittest.mock import patch

from client import Client


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = Client("urls.txt", 2)

    @patch("builtins.open")
    def test_get_url(self, mock_open):
        """
        Проверяем, что файл читается корректно
        """
        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.__iter__.return_value = iter(
            ["http://google.com", "http://wikipedia.org"]
        )

        urls = list(self.client._get_url())

        self.assertEqual(urls, ["http://google.com", "http://wikipedia.org"])
        mock_open.assert_called_once_with("urls.txt", "r")

    @patch("client.Thread")
    def test_send_urls(self, mock_thread):
        """
        Проверяем то, что потоки создались корректно и с нужными аргументами
        """
        self.client.send_urls()

        self.assertEqual(mock_thread.call_count, 2)
        self.assertEqual(
            mock_thread.call_args_list[0][1]["target"], self.client._send_url
        )
        self.assertEqual(mock_thread.call_args_list[0][1]["name"], "T0")
        self.assertEqual(
            mock_thread.call_args_list[1][1]["target"], self.client._send_url
        )
        self.assertEqual(mock_thread.call_args_list[1][1]["name"], "T1")
