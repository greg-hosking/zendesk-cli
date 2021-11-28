import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

REQUESTS_URL = 'https://zccgreghosking.zendesk.com/api/v2/requests'
EMAIL = 'hoskinggregory@gmail.com'
TOKEN = '0jprlJiLQxMcfepuKLADbwwQF7F0N8f85FFMyH4G'
PAGE_LIMIT = 25

def get_ticket(id: str):
    try:
        if id == 'ALL':
            response = requests.get(
                REQUESTS_URL, auth=HTTPBasicAuth(f'{EMAIL}/token', TOKEN))
            # Check for any exceptions from the response.
            response.raise_for_status()
            # If no exceptions were thrown, return the tickets JSON.
            return response.json()['requests']
        else:
            response = requests.get(
                f'{REQUESTS_URL}/{id}', auth=HTTPBasicAuth(f'{EMAIL}/token', TOKEN))
            # Check for any exceptions from the response.
            response.raise_for_status()
            # If no exceptions were thrown, return the ticket JSON.
            return response.json()['request']

    # Handle the exception thrown if the user could not be authenticated or
    # if no ticket exists with the given ID.
    except requests.exceptions.HTTPError:
        if response.status_code == 401:
            print(
                'Oops! Could not authenticate you. Please make sure your email and token are correct and try again...')
        elif response.status_code == 404:
            print('Oops! Could not find a ticket with that ID. Please try again...')

    # Handle the exception thrown if the user could not connect to the API.
    except requests.exceptions.ConnectionError:
        print('Oops! Could not connect to the Zendesk Tickets API. Please check your connection and try again...')
        print('If this continues to happen, then something is wrong on our side. Sorry for the inconvenience.')

    # Handle the exception thrown if the request timed out.
    except requests.exceptions.Timeout:
        print('Oops! The request timed out. Please check your connection and try again...')

    # Handle any other exceptions...
    except requests.exceptions.RequestException:
        print('Oops! Something went wrong. Please try again...')


def print_ticket(ticket_json: str):

    subject = ticket_json['subject']
    requester_id = ticket_json['requester_id']

    # Parse date and time for created_at field.
    # Example: 2021-11-26T17:22:43Z -> Fri Nov 26, 2021 at 05:22:43PM...  
    created_at = ticket_json['created_at'][:-1]
    date_time_created_at_str = datetime.fromisoformat(created_at)
    date_time_created_at_obj = datetime.strftime(
        date_time_created_at_str, '%a %b %d, %Y at %I:%M:%S%p')

    print(f'\'{subject}\' opened by {requester_id} on {str(date_time_created_at_obj)}')


if __name__ == '__main__':

    print('-------------------------------------')
    print('Welcome to the Zendesk Ticket Viewer!')
    print('-------------------------------------')
    print()

    while True:
        print('Please select one of the following options:')
        print('-------------------------------------------')
        print('[1] View all tickets')
        print('[2] View a ticket')
        print('[3] Exit')
        user_input = input()
        print('')

        # Handle user input to request all tickets.
        if user_input == '1':
            tickets = get_ticket('ALL')
            for ticket in tickets:
                print_ticket(ticket)

        # Handle user input to request a specific ticket.
        elif user_input == '2':
            print('Enter a ticket ID: ')
            id = input()
            
            ticket = get_ticket(id)
            if ticket:
                print_ticket(ticket)

        # Handle user input to exit the viewer.
        elif user_input == '3':
            break

        # Handle unrecognized user input.
        else:
            print('That was not an option....')

        # Print a newline after processing user input (for clean console).
        print('')

    print('----------------------------------------------')
    print('Thank you for using the Zendesk Ticket Viewer!')
    print('----------------------------------------------')
