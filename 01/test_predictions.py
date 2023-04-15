import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
from predictions import SomeModel, predict_message_mood


class TestPredictions(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SomeModel()

    # добавил тесты с изменением порогов предиктора и проверкой
    # аргументов при вызове замоканного предикта;
    # рассмотрел краевые случаи: когда значение предикта совпадает с порогами
    # и когда предикт возвращает None

    @patch("predictions.SomeModel.predict")
    def test_predict_calls(self, predict_mock: MagicMock):
        predict_mock.side_effect = 0.8, 0.5, 0.2

        self.assertEqual(
            predict_message_mood(
                "Ужасное настроение",
                self.model,
                bad_thresholds=0.9,
                good_thresholds=0.95,
            ),
            "неуд",
        )
        self.assertEqual(
            predict_message_mood("Хорошее настроение", self.model,
                                 bad_thresholds=0.4),
            "норм",
        )
        self.assertEqual(
            predict_message_mood(
                "Отличное настроение",
                self.model,
                bad_thresholds=0.1,
                good_thresholds=0.15,
            ),
            "отл",
        )

        expected_calls = [
            mock.call("Ужасное настроение"),
            mock.call("Хорошее настроение"),
            mock.call("Отличное настроение"),
        ]
        self.assertEqual(expected_calls, predict_mock.mock_calls)

        predict_mock.side_effect = TypeError("Message should be string")

        with self.assertRaises(TypeError) as ex:
            predict_message_mood(1, self.model)

        self.assertEqual(str(ex.exception), "Message should be string")

    @patch("predictions.SomeModel.predict")
    def test_edge_cases(self, predict_mock):
        predict_mock.side_effect = 0, 0.4, 0.5, 1, None

        self.assertEqual(predict_message_mood('', self.model), 'неуд')

        self.assertEqual(predict_message_mood('', self.model, bad_thresholds=0.4),
                         'норм')
        self.assertEqual(predict_message_mood('', self.model, good_thresholds=0.5),
                         'отл')
        self.assertEqual(predict_message_mood('', self.model), 'отл')

        self.assertEqual(predict_message_mood('', self.model),
                         None)

    @patch("predictions.SomeModel.predict")
    def test_bad_vibe(self, predict_mock):
        predict_mock.return_value = 0.1

        self.assertEqual(predict_message_mood("Чувствую себя великолепно", self.model),
                         "неуд")

    @patch("predictions.SomeModel.predict")
    def test_good_vibe(self, predict_mock):
        predict_mock.return_value = 0.8

        result = predict_message_mood("Чувствую себя великолепно", self.model)
        self.assertEqual(result, "отл")

    @patch("predictions.SomeModel.predict")
    def test_norm_vibe(self, predict_mock):
        predict_mock.return_value = 0.4

        result = predict_message_mood("Чапаев и Пустота", self.model)
        self.assertEqual(result, "норм")

    def test_equal_thresholds(self):
        with self.assertRaises(ValueError) as context:
            predict_message_mood(
                "А непонятно какое настроение",
                self.model,
                bad_thresholds=0.5,
                good_thresholds=0.5,
            )
            self.assertTrue(
                "Good threshold should be higher than bad threshold"
                in context.exception
            )

    def test_incorrect_thresholds(self):
        with self.assertRaises(ValueError) as context:
            predict_message_mood(
                "Ни туда ни сюда", self.model, bad_thresholds=0.6, good_thresholds=0.4
            )
            self.assertTrue(
                "Good threshold should be higher than bad threshold"
                in context.exception
            )

    def test_too_big_thresholds(self):
        self.assertRaises(ValueError)
        with self.assertRaises(ValueError) as context:
            predict_message_mood("ОООЧЧЕНННЬ ХОРОШО", self.model, good_thresholds=1.3)
            self.assertTrue(
                "Both thresholds should be in interval [0; 1]" in context.exception
            )

    def test_too_small_thresholds(self):
        with self.assertRaises(ValueError) as context:
            predict_message_mood("ОООЧЧЕННЬ ПЛОХО", self.model, bad_thresholds=-1.3)
            self.assertTrue(
                "Both thresholds should be in interval [0; 1]" in context.exception
            )
