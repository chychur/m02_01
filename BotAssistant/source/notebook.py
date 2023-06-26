from cls import RecordType, Name, Tag, Note
from collections import UserList
from datetime import datetime

import json
import re


class NoteRecord(RecordType):

    def __init__(self, name: Name, tag: Tag | None = None, note: Note | None = None):
        self.name = name

        self.tags = set()
        self.adder(tag)
        self.note = note

    def add_item(self, tag):
        if isinstance(tag, str):
            tag = Tag(tag)
        self.tags.add(tag)

    def show_item(self):
        if self.tags:
            list_tags = [str(t) for t in self.tags]
            return ", ".join(list_tags)
        return 'Empty'

    def __repr__(self) -> str:
        return f'Record (Name:"{self.name}", Phone:"{self.show_phones()}", Birthday:"{self.birthday}")'

    def __str__(self) -> str:
        return f'Name: {self.name}, Phone:{self.show_phones()}, Birthday:{self.birthday or "Empty"}'

    @property
    def record(self):
        return {
            'name': self.name.value,
            'phones': self.show_phones(),
            'birthday': self.birthday.value if self.birthday else 'Empty'
        }

    def __getitem__(self, item: str):
        return self.record.get(item)


class NoteBook(UserList):

    def __init__(self) -> None:
        self.data: list[NoteRecord] = []
        self.current_value = 0
        self.step = 0
        self.file_name_save = '/BotAssistant/storage/NoteBookStorage.json'

    def __getitem__(self, index):
        return self.data[index]

    def create_and_add_record(self, name, tag: str | None = None, note: str | None = None):
        record = NoteRecord(Name(name), Tag(tag), Note(note))
        self.add_record_handler(record)

        return f"Added contact {record}"

    def add_record_handler(self, record: NoteRecord):
        self.data.append(record)

    def add_tag_handler(self, name, tag: str):
        for record in self.data:
            if record.name.value == name:
                record.tags.add(Tag(tag))

    def del_phone_handler(self, name, phone):
        for record in self.data:
            if record.name.value == name:
                record.phones.discard(Phone(phone))

    def change_handler(self, name: str, old_phone: str, phone: str):  # зміна телефону
        old_phone_title = Phone(old_phone)
        for record in self.data:
            if record.name.value == name:
                if record.phones:
                    self.add_phone_handler(name, phone)
                    self.del_phone_handler(name, old_phone)

                return (
                    f'For user [ {record.name.value} ] had been changed phone number! \n'
                    f' Old phone number: {old_phone_title.value} \n'
                    f' New phone number: {record.phones}'
                )
        return f'Not found contact for name {name}'

    def phone_handler(self, name: str):  # показати номер телефону
        for record in self.data:
            if record.name.value == name:
                return f"Phone(s) of {name} is: {record.phones}"
        return f"Phone for user {name} not found"

    def show_all_handler(self):
        self.step = 0
        result = ''
        header = '='*51 + '\n' + \
            '|{:^5}|{:<12}|{:^15}|{:^14}|\n'.format(
                'No.', 'Name', 'Phone(s)', 'Birthday') + '='*51 + '\n'
        foter = '='*51 + '\n'
        counter = 0
        for record in self.data:
            counter += 1
            result += '|{:^5}|{:<12}|{:^15}|{:^14}|\n'.format(
                counter, record.name.value, record.show_phones(), record.birthday.value if record.birthday else 'Empty')
        counter = 0
        result_tbl = header + result + foter
        return result_tbl

    def show_n_handler(self, n: int):
        n = int(n)
        if n > 0:
            if len(self.data) - self.step >= n:

                result = ''
                header = '='*51 + '\n' + \
                    '|{:^5}|{:<12}|{:^15}|{:^14}|\n'.format(
                        'No.', 'Name', 'Phone(s)', 'Birthday') + '='*51 + '\n'
                foter = '='*51 + '\n'

                for record in self.data[self.step:self.step+n]:
                    self.step += 1
                    result += '|{:^5}|{:<12}|{:^15}|{:^14}|\n'.format(
                        self.step, record.name.value, record.show_phones(), record.birthday.value if record.birthday else 'Empty')

                result_tbl = header + result + foter
                return result_tbl
            else:
                return (
                    f'Curent AdressBook volume is {len(self.data)} records'
                    f'Now you are in the end of AdressBook'
                )
        else:
            raise ValueError('Wrong value! the number must be greater than 0')

    def __iter__(self):
        return self

    def __next__(self):

        if self.current_value < len(self.data):

            result = f' {self.current_value + 1} | Name: {self.data[self.current_value].name.value}, Phone(s):{self.data[self.current_value].phones}, Birthday: {self.data[self.current_value].birthday or "Empty"}'
            self.current_value += 1
            return result

        raise StopIteration

    def search(self, pattern):
        pattern_searched = str(pattern.strip().lower().replace(' ', ''))
        result = ''
        header = '\n' + f'  RESULT of searching with your request: "{pattern}"' + '\n' + '='*45 + '\n' + \
            '|{:<12}|{:^15}|{:^14}|\n'.format(
                'Name', 'Phone(s)', 'Birthday') + '='*45 + '\n'
        foter = '='*45 + '\n'
        for record in self.data:
            for phone in record.phones:
                if str(phone).find(pattern_searched) != -1:
                    result += '|{:<12}|{:^15}|{:^14}|\n'.format(
                        record.name.value, record.phones, record.birthday.value)
            if str(record.name.value.find(pattern_searched)) != -1:
                result += '|{:<12}|{:^15}|{:^14}|\n'.format(
                    record.name.value, record.phones, record.birthday.value)
            else:
                result = f'There was nothing found with your request: "{pattern}"'
                header = ''
                foter = ''
        result_tbl = header + result + foter
        return result_tbl

    def autosave(self):
        with open(self.file_name_save, 'w') as file:
            json.dump(self.data, file)
        self.log("Addressbook has been saved!")

    def load(self):
        with open(self.file_name_save, 'r') as file:
            self.data = json.load(file)
        self.log("Addressbook has been loaded!")
        return self.data

    def log(self, log_message: str, prefix: str | None = None):
        current_time = datetime.strftime(datetime.now(), '%H:%M:%S')
        if prefix == 'com':
            message = f'[{current_time}] USER INPUT : {log_message}'
        elif prefix == 'res':
            message = f'[{current_time}] BOT RESULT : \n{log_message}\n'
        elif prefix == 'err':
            message = f'[{current_time}] !!! === ERROR MESSAGE === !!! {log_message}\n'
        elif prefix == None:
            message = f'[{current_time}] {log_message}'
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n')
