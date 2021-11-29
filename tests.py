import unittest
import requests
from requests.auth import HTTPBasicAuth
from cli import get_ticket


print('---------------------------------------')
print('Welcome to Zendesk Ticket Viewer Tests!')
print('---------------------------------------')
print('A valid subdomain, email, and access token are required to perform unit tests.')
print('')

while True:
    print('Please enter the subdomain you would like to access.')
    print(
        'Example: if the URL were students.zendesk.com, you would enter \'students\' as the subdomain.')
    subdomain = input()
    print('')

    # Test the subdomain to see if it exists. If it does not exist,
    # the request should return a status code of 404 (not found).
    # If it does exist, we get a status code of 401 (not authenticated).
    url = f'https://{subdomain}.zendesk.com/api/v2/requests'
    response = requests.get(url)
    if response.status_code == 401:
        print('Please enter the email associated with this account.')
        email = input()
        print('')

        print('Please enter an access token for this account.')
        print(
            'If you do not have an access token, you can create one using the Zendesk agent under Admin > API.')
        token = input()
        print('')

        # Test the email and token for the given subdomain.
        response = requests.get(
            url, auth=HTTPBasicAuth(f'{email}/token', token))
        if response.status_code == 200:
            print('Successfully authenticated you! Proceeding with unit tests...')
            print('-------------------------------------------------------------')
            print('')
            break
        else:
            print(
                'Oops! Could not authenticate you. Please make sure your email and token are correct for this subdomain and try again...')
    else:
        print('Oops! That subdomain does not exist. Please try again...')


class TestGetTicket(unittest.TestCase):

    def test_get_ticket_nonexisting_ticket_id(self):
        print('Testing get_ticket() with nonexisting ticket ID...')
        self.assertIsNone(get_ticket(
            subdomain, email, token, '-1'))
        print('Test passed!')
        print('')

    def test_get_ticket_no_ticket_id(self):
        print('Testing get_ticket() with empty string and None type ticket ID...')
        self.assertIsNone(get_ticket(
            subdomain, email, token, ''))
        self.assertIsNone(get_ticket(
            subdomain, email, token, None))
        print('Test passed!')
        print('')

    def test_get_all_tickets(self):
        print('Testing get_ticket() to get all tickets...')
        self.assertIsNotNone(get_ticket(
            subdomain, email, token))
        print('Test passed!')
        print('')


if __name__ == '__main__':
    unittest.main()
