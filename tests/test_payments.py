import unittest
from unittest.mock import Mock
from bot.payments import handle_payment

class TestPayments(unittest.TestCase):

    def setUp(self):
        self.update = Mock()
        self.context = Mock()

    def test_handle_payment(self):
        handle_payment(self.update, self.context)
        self.assertTrue(self.context.bot.send_message.called)
        self.assertEqual(self.context.bot.send_message.call_count, 1)

if __name__ == '__main__':
    unittest.main()
