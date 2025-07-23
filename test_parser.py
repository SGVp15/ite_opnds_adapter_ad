import re
from unittest import TestCase

from parser import parser_users


class Test(TestCase):
    def test_parser_users(self):
        for i in range(1):
            with open('out2.txt', 'r', encoding='utf-8') as f:
                s = f.read()
            o = parser_users(s)
            print(o)

        for i in range(1):
            with open('out_user.txt', 'r', encoding='utf-8') as f:
                s = f.read()
            o = parser_users(s)
            print(o)
