from typing import Any
from abc import ABC, abstractmethod
from collections import UserList, UserDict
import csv
from datetime import datetime

import re


class Field:

    def __init__(self, value: Any) -> None:
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        return f'{self.value}'

    def __repr__(self) -> str:
        return f'{self.value}'


class Name(Field):

    def __init__(self, value: str) -> None:
        super().__init__(value)


class Phone(Field):

    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if re.match('^\\+38\d{10}$', value) or value == '':
            Field.value.fset(self, value)
        else:
            raise ValueError(
                'Incorrect phone number format! '
                'Please provide correct phone number format.'
            )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if not value:
            Field.value.fset(self, '')
        elif re.match('^\d{2}/\d{2}/\d{4}$', value):
            Field.value.fset(self,
                             datetime.strptime(value, "%d/%m/%Y").date()
                             )
        else:
            raise ValueError(
                'Incorrect date! Please provide correct date format.')


class Email(Field):

    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if not value:
            Field.value.fset(self, '')
        elif re.match('^\S+@\S+\.\S+$', value):
            Field.value.fset(self, value)
        else:
            raise ValueError(
                'Incorrect email! Please provide correct email format.')


class Address(Field):

    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if not value:
            Field.value.fset(self, '')
        elif value:
            Field.value.fset(self, value)
        else:
            raise ValueError(
                'Incorrect address! Please provide correct address format.')


class Tag(Field):

    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if not value:
            Field.value.fset(self, '')
        elif value:
            Field.value.fset(self, value)
        else:
            raise ValueError(
                'Incorrect tag format! '
                'Please provide correct tag format.'
            )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)


class Note(Field):

    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if not value:
            Field.value.fset(self, '')
        elif value:
            Field.value.fset(self, value)
        else:
            raise ValueError(
                'Incorrect note! Please provide correct note format.')


# =============================== Adstract Classes =====================


class RecordType(ABC, UserDict):

    def __init__(self):
        self.data = None

        self.name = None
        self.birthday = None
        self.phones = set()
        self.tags = set()
        self.email = None
        self.address = None
        self.note = None

    @abstractmethod
    def days_to_birthday(self):
        pass

    @abstractmethod
    def add_unique_item(self):
        pass

    @abstractmethod
    def show_unique_items(self):
        pass


class ModuleType(ABC, UserList):

    def __init__(self) -> None:
        self.data = None
        self.current_value = 0
        self.step = 0
        self.file_name_save = None
        record = None
        self.add_record(record)

    @abstractmethod
    def create_and_add_record(self):
        pass

    def add_record(self, record: object):
        self.data.append(record)

    @abstractmethod
    def add_item_s(self):
        pass

    @abstractmethod
    def del_item_s(self):
        pass

    @abstractmethod
    def change_item_s(self):
        pass

    @abstractmethod
    def item(self):
        pass

    @abstractmethod
    def record_table_maker(self):
        pass

    @abstractmethod
    def header_table_maker(self):
        pass

    @abstractmethod
    def foter_table_maker(self):
        pass

    @abstractmethod
    def show_all(self):
        pass

    @abstractmethod
    def show_n(self):
        pass

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass


if __name__ == "__main__":
    pass
