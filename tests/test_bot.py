import unittest
from unittest.mock import Mock
from telegram import Update
from bot.handlers import setup_handlers

class TestBot(unittest.TestCase):

    def setUp(self):
        self.application = Mock()
        setup_handlers(self.application)

    def test_handlers_setup(self):
        self.assertTrue(self.application.add_handler.called)
        self.assertEqual(self.application.add_handler.call_count, 10)

    def test_webhook(self):
        update = Update.de_json({}, self.application.bot)
        self.application.update_queue.put(update)
        self.assertTrue(self.application.update_queue.put.called)

if __name__ == '__main__':
    unittest.main()
