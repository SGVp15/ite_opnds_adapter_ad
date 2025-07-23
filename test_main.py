from unittest import TestCase

from parser import get_domain_from_group


class Test(TestCase):
    def test_get_server_from_group(self):
        for i in range(10):
            print(i, get_domain_from_group('CN=VM-AD-MSK-1,OU=Domain Controllers,DC=ITExpert,DC=ru,DC=local', i))
