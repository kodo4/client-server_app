import copy
import sys
import os
import unittest
sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ENCODING, ACTION, PRESENCE, \
    USER, ACCOUNT_NAME, TIME, ERROR
from server import process_client_message as pcl


class TestCase(unittest.TestCase):
    """Класс тестов сервера"""
    msg_ok = {
        ACTION: PRESENCE,
        TIME: 1.1,
        USER: {
            ACCOUNT_NAME: 'Guest'
        }
    }

    send_msg_ok = {RESPONSE: 200}

    send_msg_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_pcl(self):
        self.assertEqual(pcl(self.msg_ok), self.send_msg_ok)

    def test_pcl_no_action(self):
        new_msg_ok = copy.deepcopy(self.msg_ok)
        del new_msg_ok[ACTION]
        self.assertEqual(pcl(new_msg_ok), self.send_msg_err)

    def test_pcl_wrong_name(self):
        new_msg_ok = copy.deepcopy(self.msg_ok)
        new_msg_ok[USER][ACCOUNT_NAME] = 'test_user'
        self.assertEqual(pcl(new_msg_ok), self.send_msg_err)

    def test_pcl_no_time(self):
        new_msg_ok = copy.deepcopy(self.msg_ok)
        del new_msg_ok[TIME]
        self.assertEqual(pcl(new_msg_ok), self.send_msg_err)

    def test_pcl_no_user(self):
        new_msg_ok = copy.deepcopy(self.msg_ok)
        del new_msg_ok[USER]
        self.assertEqual(pcl(new_msg_ok), self.send_msg_err)


if __name__ == '__main__':
    unittest.main()