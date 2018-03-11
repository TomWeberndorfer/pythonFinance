from unittest import TestCase

from Utils.common_utils import send_email


class TestUtils(TestCase):
    def test_calc_avg_vol(self):
        self.assertEqual(1,1)


    def test_send_email(self):
        result = send_email(from_addr='python.trading.framework@gmail.com',
                  to_addr_list=['weberndorfer.thomas@gmail.com'],
                  cc_addr_list=[],
                  subject='Aktien',
                  message='Test',
                  login='python.trading.framework',
                  password='8n6Qw8YoJe8m')

        self.assertEqual(len(result), 0)
