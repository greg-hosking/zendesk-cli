import unittest
from cli import get_ticket


class TestGetTicket(unittest.TestCase):

    def test_get_exsiting_ticket_id(self):
        self.assertEqual(
            get_ticket('1')['subject'], 'Sample ticket: Meet the ticket')

    def test_get_nonexisting_ticket_id(self):
        self.assertIsNone(get_ticket(''), None)

    def test_get_all_tickets(self):
        self.assertEqual(len(get_ticket('ALL')), 100)

    def test_get_ticket_incorrect_email(self):
        self.assertIsNone(get_ticket('1', ''))

    def test_get_ticket_incorrect_token(self):
        self.assertIsNone(get_ticket('1', 'hoskinggregory@gmail.com', ''))


if __name__ == '__main__':
    unittest.main()
