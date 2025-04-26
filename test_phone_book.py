import pytest
import os
from dataclasses import dataclass
from typing import Dict


@dataclass
class Contact:
    name: str
    phone: str
    comment: str

    def join(self, separator: str = ' ') -> str:
        data = [self.name, self.phone, self.comment]
        return separator.join(data)

    def compre(self, other: 'Contact') -> None:
        self.name = other.name if other.name else self.name
        self.phone = other.phone if other.phone else self.phone
        self.comment = other.comment if other.comment else self.comment


class PhoneBook:
    def __init__(self, path: str, separator: str = ';'):
        self.path = path
        self.separator = separator
        self.phone_book: Dict[int, Contact] = {}

    def _next_id(self) -> int:
        if self.phone_book:
            return max(self.phone_book) + 1
        return 1

    def open_file(self) -> None:
        with open(self.path, 'r', encoding='utf-8') as file:
            data = list(map(lambda x: x.strip().split(self.separator), file.readlines()))
            for entry in data:
                self.phone_book[self._next_id()] = Contact(
                    name=entry[0],
                    phone=entry[1],
                    comment=entry[2],
                )

    def seve_file(self) -> None:
        with open(self.path, 'w', encoding='utf-8') as file:
            data = [entry.join(self.separator) for entry in self.phone_book.values()]
            file.write('\n'.join(data))

    def new_contact(self, new_contact: list[str]) -> None:
        current_id = self._next_id()
        self.phone_book[current_id] = Contact(
            name=new_contact[0],
            phone=new_contact[1],
            comment=new_contact[2],
        )

    def edit_contact(self, edit_id: str, edited_contact: list[str]) -> None:
        contact = self.phone_book[int(edit_id)]
        edited_contact = Contact(
            name=edited_contact[0],
            phone=edited_contact[1],
            comment=edited_contact[2],
        )
        contact.compre(edited_contact)
        self.phone_book[int(edit_id)] = contact

    def find_contact(self, key_word: str) -> Dict[int, Contact]:
        result = {}
        for idx, contact in self.phone_book.items():
            if key_word.lower() in contact.join().lower():
                result[idx] = contact
        return result

    def delete_contact(self, delete_id: str) -> Contact:
        return self.phone_book.pop(int(delete_id))


# Tests for Contact class
def test_contact_join():
    contact = Contact("John", "12345", "Friend")
    assert contact.join() == "John 12345 Friend"
    assert contact.join(';') == "John;12345;Friend"


def test_contact_compre():
    contact1 = Contact("John", "12345", "Friend")
    contact2 = Contact("", "67890", "Colleague")
    contact1.compre(contact2)
    assert contact1.name == "John"
    assert contact1.phone == "67890"
    assert contact1.comment == "Colleague"


# Tests for PhoneBook class
@pytest.fixture
def sample_phonebook(tmp_path):
    # Create a test file
    file_path = tmp_path / "test_contacts.txt"
    file_content = "John;12345;Friend\nAlice;67890;Work"
    file_path.write_text(file_content, encoding='utf-8')

    # Create PhoneBook instance
    pb = PhoneBook(str(file_path))
    pb.open_file()
    return pb


def test_phonebook_open_file(sample_phonebook):
    assert len(sample_phonebook.phone_book) == 2
    assert sample_phonebook.phone_book[1].name == "John"
    assert sample_phonebook.phone_book[2].phone == "67890"


def test_phonebook_save_file(tmp_path, sample_phonebook):
    # Modify a contact
    sample_phonebook.phone_book[1].comment = "Best friend"

    # Save to a new file
    new_path = tmp_path / "new_contacts.txt"
    sample_phonebook.path = str(new_path)
    sample_phonebook.seve_file()

    # Verify saved content
    with open(new_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "John;12345;Best friend" in content
    assert "Alice;67890;Work" in content


def test_phonebook_new_contact(sample_phonebook):
    sample_phonebook.new_contact(["Bob", "55555", "Family"])
    assert len(sample_phonebook.phone_book) == 3
    assert sample_phonebook.phone_book[3].name == "Bob"


def test_phonebook_edit_contact(sample_phonebook):
    sample_phonebook.edit_contact("1", ["Johnny", "", "Best friend"])
    assert sample_phonebook.phone_book[1].name == "Johnny"
    assert sample_phonebook.phone_book[1].phone == "12345"  # Not changed
    assert sample_phonebook.phone_book[1].comment == "Best friend"


def test_phonebook_find_contact(sample_phonebook):
    # Search by name
    result = sample_phonebook.find_contact("john")
    assert len(result) == 1
    assert 1 in result

    # Search by phone
    result = sample_phonebook.find_contact("678")
    assert len(result) == 1
    assert 2 in result

    # Search by comment
    result = sample_phonebook.find_contact("work")
    assert len(result) == 1
    assert 2 in result


def test_phonebook_delete_contact(sample_phonebook):
    deleted = sample_phonebook.delete_contact("1")
    assert deleted.name == "John"
    assert len(sample_phonebook.phone_book) == 1
    assert 1 not in sample_phonebook.phone_book


def test_phonebook_next_id():
    pb = PhoneBook("test.txt")
    assert pb._next_id() == 1

    pb.phone_book = {1: Contact("a", "1", "a"), 3: Contact("b", "2", "b")}
    assert pb._next_id() == 4


def test_phonebook_empty_file(tmp_path):
    # Test with empty file
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("", encoding='utf-8')

    pb = PhoneBook(str(empty_file))
    pb.open_file()
    assert len(pb.phone_book) == 0