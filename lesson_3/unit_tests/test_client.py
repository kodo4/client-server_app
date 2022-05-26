import sys
import os
import unittest
sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ENCODING, ACTION, PRESENCE, \
    USER, ACCOUNT_NAME, TIME, ERROR
from client import create_presence, process_ans


class TestClass(unittest.TestCase):
    """
    Класс с тестами
    """
    ok_message = {RESPONSE: 200}
    err_message = {RESPONSE: 400,
                   ERROR: 'Bad Request'}

    def test_def_pressense(self):
        """Тест корректного запроса"""
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION:PRESENCE,
                                TIME: 1.1,
                                USER: {
                                    ACCOUNT_NAME: 'Guest'
                                }})

    def test_200_ans(self):
        self.assertEqual(process_ans(self.ok_message), '200: OK')

    def test_400_ans(self):
        self.assertEqual(process_ans(self.err_message), '400: Bad Request')

    def test_no_response_in_message(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
