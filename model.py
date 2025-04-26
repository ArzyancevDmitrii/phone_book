from dataclasses import dataclass

@dataclass
class Contact:

    name: str
    phone: str
    comment: str


    def join(self, separator: str = ' '):
        data = [self.name, self.phone, self.comment]
        return separator.join(data)

    def compre(self, other: 'Contact'):
        self.name = other.name if other.name else self.name
        self.phone = other.phone if other.phone else self.phone
        self.comment = other.comment if other.comment else self.comment




class PhoneBook:
    def __init__(self, path: str, separator: str = ';'):
        self.path = path
        self.separator = separator
        self.phone_book: dict[int, Contact] =  {}

    def _next_id(self):
        if self.phone_book:
            return max(self.phone_book) + 1
        return 1


    def open_file(self):
            with open(self.path, 'r', encoding='utf-8') as file:
                data = list(map(lambda x: x.strip().split(self.separator), file.readlines()))
                for entry in data:
                    self.phone_book[self._next_id()] = Contact(
                        name=entry[0],
                        phone=entry[1],
                        comment=entry[2],
                    )
                print(self.phone_book)

    def seve_file(self):
        with open(self.path, 'w', encoding='utf-8') as file:
            data = [entry.join(self.separator) for entry in self.phone_book.values()]
            file.write('\n'.join(data))



    def new_contact(self, new_contact: list[str]):
        current_id = self._next_id()
        self.phone_book[current_id] = Contact(
            name=new_contact[0],
            phone=new_contact[1],
            comment=new_contact[2],
        )

    def edit_contact(self, edit_id: str, edited_contact: list[str]):
        contact = self.phone_book[int(edit_id)]
        edited_contact = Contact(
            name=edited_contact[0],
            phone=edited_contact[1],
            comment=edited_contact[2],
        )
        contact.compre(edited_contact)
        self.phone_book[int(edit_id)] = contact


    def find_contact(self, key_word: str) -> dict[int, Contact]:
        result = {}
        for idx, contact in self.phone_book.items():
            if key_word.lower() in contact.join().lower():
                result[idx] = contact
        return result

    def delete_contact(self, delete_id: str) -> Contact:
        contact = self.phone_book.pop(int(delete_id))
        return contact