import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


REQUESTS_URL = 'https://zccgreghosking.zendesk.com/api/v2/requests'
EMAIL = 'hoskinggregory@gmail.com'
TOKEN = '0jprlJiLQxMcfepuKLADbwwQF7F0N8f85FFMyH4G'
TICKETS_PER_PAGE = 25


def get_ticket(id: str, email: str = EMAIL, token: str = TOKEN):
    """
    Calls the Zendesk Ticket API to get a ticket of a given ID as a string. 
    The function also accepts 'ALL' as an ID and gets ALL tickets.
    """
    # Guard against empty ids.
    if not id or id == '':
        print('Oops! Could not find a ticket with that ID. Please try again...')
        return

    try:
        if id == 'ALL':
            response = requests.get(
                REQUESTS_URL, auth=HTTPBasicAuth(f'{email}/token', token))
            # Check for any exceptions from the response.
            response.raise_for_status()
            # If no exceptions were thrown, return the tickets JSON.
            return response.json()['requests']
        else:
            response = requests.get(
                f'{REQUESTS_URL}/{id}', auth=HTTPBasicAuth(f'{email}/token', token))
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

    # Guard against empty strings.
    if not ticket_json:
        return

    subject = ticket_json['subject']
    requester_id = ticket_json['requester_id']

    # Parse date and time for created_at field.
    # Example: 2021-11-26T17:22:43Z -> Fri Nov 26, 2021 at 05:22:43PM...
    created_at = ticket_json['created_at'][:-1]
    date_time_created_at_str = datetime.fromisoformat(created_at)
    date_time_created_at_obj = datetime.strftime(
        date_time_created_at_str, '%a %b %d, %Y at %I:%M:%S%p')

    print(
        f'\'{subject}\' opened by {requester_id} on {str(date_time_created_at_obj)}')


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

            n_tickets = len(tickets)
            n_pages = n_tickets // TICKETS_PER_PAGE
            if n_tickets % TICKETS_PER_PAGE != 0:
                n_pages += 1

            page_num = 0
            while page_num < n_pages:
                print(f'Page {page_num + 1} of {n_pages}')
                print('-------------------------------------')
                for ticket_num in range(TICKETS_PER_PAGE):
                    ticket_index = ticket_num + (page_num * TICKETS_PER_PAGE)
                    if ticket_index >= n_tickets:
                        break

                    print(ticket_index + 1, end=' ')
                    print_ticket(tickets[ticket_index])
                print('')

                while True:
                    print('Please select one of the following options:')
                    print('-------------------------------------------')
                    # If on the last page, the user should only be able to
                    # page backward or return to the menu.
                    if page_num == n_pages - 1:
                        print('[1] View the previous page')
                        print('[3] Return to the menu')
                    # If on the first page, the user should only be able to
                    # page forward.
                    elif page_num == 0:
                        print('[2] View the next page')
                        print('[3] Return to the menu')
                    else:
                        print('[1] View the previous page')
                        print('[2] View the next page')
                        print('[3] Return to the menu')
                    user_input = input()
                    print('')

                    # Handle user input to view previous page, if allowed.
                    if user_input == '1' and page_num > 0:
                        page_num -= 1
                        break
                    # Handle user input to view next page, if allowed.
                    elif user_input == '2' and page_num < n_pages - 1:
                        page_num += 1
                        break
                    # Handle user input to return to menu.
                    elif user_input == '3':
                        page_num = n_pages
                        break
                    # Handle unrecognized user input.
                    else:
                        print('That was not an option...')

                    # Print a newline after processing user input (for clean console).
                    print('')

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
