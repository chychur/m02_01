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
        if re.match('^\S+@\S+\.\S+$', value) or value == '':
            Field.value.fset(self, value)
        else:
            raise ValueError(
                'Incorrect email format! '
                'Please provide correct email format.'
            )


class Address(Field):

    def __init__(self, value) -> None:
        super().__init__(value)


class Tag(Field):

    def __init__(self, value) -> None:
        super().__init__(value)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)


class Note(Field):

    def __init__(self, value) -> None:
        super().__init__(value)


class RecordType(ABC):

    def __init__(self):
        self.name = None

    @abstractmethod
    def days_to_birthday(self):
        pass

    @abstractmethod
    def add_phone(self):
        pass

    @abstractmethod
    def show_phones(self):
        pass


class ModuleType(ABC, UserList):

    def __init__(self) -> None:
        self.data = None
        self.current_value = 0
        self.step = 0
        self.file_name_save = None

    @abstractmethod
    def create_and_add_record(self):
        pass

    @abstractmethod
    def add_record_handler(self):
        pass

    @abstractmethod
    def add_phone_handler(self):
        pass

    @abstractmethod
    def del_phone_handler(self):
        pass

    @abstractmethod
    def change_handler(self):
        pass

    @abstractmethod
    def phone_handler(self):
        pass

    # @abstractmethod
    # def __record_table_maker(self):
    #     pass

    # @abstractmethod
    # def __header_table_maker(self):
    #     pass

    # @abstractmethod
    # def __foter_table_maker(self):
    #     pass

    @abstractmethod
    def show_all_handler(self):
        pass

    @abstractmethod
    def show_n_handler(self):
        pass

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def autosave(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def log(self, log_message: str, prefix: str | None = None):
        pass


if __name__ == "__main__":
    pass
