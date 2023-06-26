from source.cls import RecordType, ModuleType, Name, Phone, Birthday, Email, Address
from datetime import datetime

import pickle


class AddressRecord(RecordType):

    def __init__(self, name: Name, phone: Phone | None = None, birthday: Birthday | None = None, email: Email | None = None, address: Address | None = None):
        self.name = name

        self.birthday = birthday
        self.phones = set()
        self.add_phone(phone)
        self.email = email
        self.address = address

    def days_to_birthday(self):
        if not self.birthday:
            return
        now = datetime.now()
        if (self.birthday.value.replace(year=now.year) - now).days > 0:
            return (self.birthday.value.replace(year=now.year) - now).days
        return (self.birthday.value.replace(year=now.year) + 1).days

    def __repr__(self) -> str:
        return f'Record (Name:"{self.name}", Phone:"{self.show_phones()}", Email:"{self.email or "Empty"}", Birthday:"{self.birthday or "Empty"}", Address:"{self.address or "Empty"}")'

    def __str__(self) -> str:
        return f'Record (Name:"{self.name}", Phone:"{self.show_phones()}", Email:"{self.email or "Empty"}", Birthday:"{self.birthday or "Empty"}", Address:"{self.address or "Empty"}")'

    def add_phone(self, phone):
        if isinstance(phone, str):
            phone = Phone(phone)
        self.phones.add(phone)

    def show_phones(self):
        if self.phones:
            list_phones = [str(p) for p in self.phones]
            return ", ".join(list_phones)
        return 'Empty'

    @property
    def record(self):
        return {
            'name': self.name.value,
            'phones': self.show_phones(),
            'birthday': self.birthday.value if self.birthday else 'Empty'
        }

    def __getitem__(self, item: str):
        return self.record.get(item)


class AddressBook(ModuleType):

    def __init__(self) -> None:
        self.data: list[AddressRecord] = []
        self.current_value = 0
        self.step = 0
        self.file_name_save = 'BotAssistant/storage/AddressBookStorage.bin'

    def __getitem__(self, index):
        return self.data[index]

    def create_and_add_record(self, name, phone: str, birthday: str | None = None, email: str | None = None, address: str | None = None):
        record = AddressRecord(Name(name), Phone(phone), Birthday(
            birthday), Email(email), Address(address))
        self.add_record_handler(record)

        return f"Added contact {record}"

    def add_record_handler(self, record: AddressRecord):
        self.data.append(record)

    def add_phone_handler(self, name, phone: str):
        for record in self.data:
            if record.name.value == name:
                record.phones.add(Phone(phone))

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

    # def __record_table_maker(self, counter: int, record: AddressRecord):
    #     row_table = '|{:^6}|{:<15}|{:^38}|{:^25}|{:^12}|{:<40}|\n'.format(
    #         counter, record.name.value, record.show_phones(), record.email.value if record.email else 'Empty', record.birthday.value if record.birthday else 'Empty', record.address.value if record.address else 'Empty')
    #     return row_table

    # def __header_table_maker(self):
    #     return '='*143 + '\n' + '|{:^6}|{:<15}|{:^38}|{:^25}|{:^12}|{:<40}|\n'.format(
    #         'No.', 'Name', 'Phone(s)', 'Email', 'Birthday', 'Address') + '='*143 + '\n'

    # def __foter_table_maker(self):
    #     return '='*143 + '\n'

    def show_all_handler(self):
        self.step = 0
        result = ''
        header = '='*143 + '\n' + \
            '|{:^6}|{:<15}|{:^38}|{:^25}|{:^12}|{:^40}|\n'.format(
                'No.', 'Name', 'Phone(s)', 'Email', 'Birthday', 'Address') + '='*143 + '\n'
        foter = '='*143 + '\n'
        counter = 0
        for record in self.data:
            counter += 1
            result += '|{:^6}|{:<15}|{:^38}|{:^25}|\n'.format(
                counter, record.name.value, record.show_phones(), record.email.value if record.email != None else 'Emty')
        counter = 0
        result_tbl = header + result + foter
        return result_tbl

    def show_n_handler(self, n: int):
        n = int(n)
        if n > 0:
            if len(self.data) - self.step >= n:

                result = ''
                header = '='*143 + '\n' + '|{:^6}|{:<15}|{:^38}|{:^25}|{:^12}|{:<40}|\n'.format(
                    'No.', 'Name', 'Phone(s)', 'Email', 'Birthday', 'Address') + '='*143 + '\n'
                foter = '='*143 + '\n'
                counter = 0
                for record in self.data[self.step:self.step+n]:
                    self.step += 1
                    result += '|{:^6}|{:<15}|{:^38}|{:^25}|{:^12}|{:<40}|\n'.format(counter, record.name.value, record.show_phones(
                    ), record.email.value if record.email else 'Empty', record.birthday.value if record.birthday else 'Empty', record.address.value if record.address else 'Empty')
                    counter = 0
                result_tbl = header + result + foter
                return result_tbl
            else:
                return (
                    f'Curent {self.__class__.__name__} volume is {len(self.data)} records'
                    f'Now you are in the end of {self.__class__.__name__}'
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
        header = self.__header_table_maker()
        foter = self.__foter_table_maker()
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
        with open(self.file_name_save, 'wb') as file:
            pickle.dump(self.data, file)
        self.log(
            f"{self.__class__.__name__} storage ({self.file_name_save}) has been saved!")

    def load(self):
        with open(self.file_name_save, 'rb') as file:
            self.data = pickle.load(file)
        self.log(
            f"{self.__class__.__name__} ({self.file_name_save}) has been loaded!")
        return self.data

    def log(self, log_message: str, prefix: str | None = None):
        current_time = datetime.strftime(datetime.now(), '%H:%M:%S')
        prefixes = {
            'com': f'[{current_time}] [Module] USER INPUT : {log_message}',
            'res': f'[{current_time}] BOT RESULT : \n{log_message}\n',
            'err': f'[{current_time}] !!! === ERROR MESSAGE === !!! {log_message}\n',
            None: f'[{current_time}] {log_message}'
        }

        message = prefixes[prefix]

        with open('BotAssistant/storage/logs.txt', 'a') as file:
            file.write(f'{message}\n')


if __name__ == "__main__":
    my_book = AddressBook()
    name = Name('Andy')
    phone = Phone('+380674169297')
    neew_record = AddressRecord(name, phone)
    print(neew_record)
