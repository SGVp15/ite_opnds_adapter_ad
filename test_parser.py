import os
import re
from unittest import TestCase

from config import DIR_OUT
from main import save_users_csv
from parser import parser_users


class Test(TestCase):
    def test_parser_users(self):
        for i in range(1):
            with open('./input_test/out2.txt', 'r', encoding='utf-8') as f:
                s = f.read()
            o = parser_users(s)
            print(o)

        for i in range(1):
            with open('./input_test/out_user.txt', 'r', encoding='utf-8') as f:
                s = f.read()
            users = parser_users(s)
            save_users_csv(users_data=users, csv_filename=str(os.path.join(DIR_OUT, 'out_user.txt')))
