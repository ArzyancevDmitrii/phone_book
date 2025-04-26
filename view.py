import text
from model import Contact, PhoneBook




def show_menu():
    for idx, row in enumerate(text.menu_items):
        if idx:
            print(f'\t{idx}. {row}')
        else:
            print(f'{row}')


def input_menu_item():
    while True:
        user_choice = input(f'\n{text.input_menu_item}')
        if user_choice.isdigit() and 0 < int(user_choice) < len(text.menu_items):
            return int(user_choice)
        print(text.input_menu_error)


def show_contacts(phone_book: dict[int, Contact], msg_error: str):
    if phone_book:
     for idx, contact in phone_book.items():
         print(f'{idx}. {contact.name:<20} {contact.phone:<20} {contact.comment:<20}')
    else:
        print_massage(msg_error)


def input_data(msg_to_input: list[str] | str) -> list[str] | str:
    if isinstance(msg_to_input, list):
        result = []
        for msg in msg_to_input:
            entry = input(msg)
            result.append(entry)
        return result
    result = input(msg_to_input)
    return result


def print_massage(msg: str):
    print('\n┏' + '━' * (len(msg) + 2) + '┓')
    print('┃' + f'{msg}' +    '┃')
    print('┗' + '━' * (len(msg) + 2) + '┛\n')
