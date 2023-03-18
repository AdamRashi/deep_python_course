import unittest
from unittest.mock import patch
from predictions import SomeModel, predict_message_mood


class TestPredictions(unittest.TestCase):

    def setUp(self) -> None:
        self.model = SomeModel()

    @patch('predictions.SomeModel.predict')
    def test_bad_vibe(self, predict_mock):
        predict_mock.return_value = 0.1

        result = predict_message_mood('Чувствую себя великолепно', self.model)
        self.assertEqual(result, 'неуд')

    @patch('predictions.SomeModel.predict')
    def test_good_vibe(self, predict_mock):
        predict_mock.return_value = 0.8

        result = predict_message_mood('Чувствую себя великолепно', self.model)
        self.assertEqual(result, 'отл')

    @patch('predictions.SomeModel.predict')
    def test_norm_vibe(self, predict_mock):
        predict_mock.return_value = 0.4

        result = predict_message_mood('Чапаев и Пустота', self.model)
        self.assertEqual(result, 'норм')

    def test_equal_thresholds(self):
        with self.assertRaises(ValueError) as context:
            predict_message_mood('А непонятно какое настроение',
                                 self.model,
                                 bad_thresholds=0.5,
                                 good_thresholds=0.5)
            self.assertTrue('Good threshold should be higher than bad threshold'
                            in context.exception)

    def test_incorrect_thresholds(self):
        with self.assertRaises(ValueError) as context:
            predict_message_mood('Ни туда ни сюда',
                                 self.model,
                                 bad_thresholds=0.6,
                                 good_thresholds=0.4)
            self.assertTrue('Good threshold should be higher than bad threshold'
                            in context.exception)

    def test_too_big_thresholds(self):
        self.assertRaises(ValueError)
        with self.assertRaises(ValueError) as context:
            predict_message_mood('ОООЧЧЕНННЬ ХОРОШО',
                                 self.model,
                                 good_thresholds=1.3)
            self.assertTrue('Both thresholds should be in interval [0; 1]'
                            in context.exception)

    def test_too_small_thresholds(self):
        with self.assertRaises(ValueError) as context:
            predict_message_mood('ОООЧЧЕННЬ ПЛОХО',
                                 self.model,
                                 bad_thresholds=-1.3)
            self.assertTrue('Both thresholds should be in interval [0; 1]'
                            in context.exception)
