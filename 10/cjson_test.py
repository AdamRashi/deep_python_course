import json
import unittest
import cjson


class CJsonTestCase(unittest.TestCase):
    def test_loads(self):
        json_str = '{"hello": 10, "world": "value"}'
        expected = {"hello": 10, "world": "value"}
        result = cjson.loads(json_str)
        self.assertEqual(result, expected)

    def test_dumps(self):
        json_dict = {"hello": 10, "world": "value"}
        expected = '{"hello": 10, "world": "value"}'
        result = cjson.dumps(json_dict)
        self.assertEqual(result, expected)

    def test_validity(self):
        json_str = '{"hello": 10, "world": "value"}'
        json_doc = json.loads(json_str)
        cjson_doc = cjson.loads(json_str)
        assert json_doc == cjson_doc

    def test_errors(self):
        with self.assertRaises(ValueError):
            cjson.loads('')

        with self.assertRaises(ValueError):
            cjson.loads(' abc')

        with self.assertRaises(TypeError):
            cjson.loads(7345)


if __name__ == "__main__":
    unittest.main()