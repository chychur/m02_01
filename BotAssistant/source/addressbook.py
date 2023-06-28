from source.cls import RecordType, ModuleType, Name, Phone, Birthday, Email, Address
from datetime import datetime

import pickle


class AddressRecord(RecordType):

    def __init__(
            self,
            name: Name,
            phone: Phone | None = None,
            birthday: Birthday | None = None,
            email: Email | None = None,
            address: Address | None = None
    ):

        self.name = name
        self.birthday = birthday
        self.phones = set()
        self.add_unique_item(phone)
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
        return f'Record (Name:"{self.name}", Phone(s):"{self.show_unique_items()}", Birthday:"{self.birthday or "Empty"}", Email:"{self.email or "Empty"}", Address:"{self.address or "Empty"}")'

    def __str__(self) -> str:
        return f'Record (Name:"{self.name}", Phone(s):"{self.show_unique_items()}", Birthday:"{self.birthday or "Empty"}", Email:"{self.email or "Empty"}", Address:"{self.address or "Empty"}")'

    def add_unique_item(self, phone):  # add_phone
        if isinstance(phone, str):
            phone = Phone(phone)
        self.phones.add(phone)

    def show_unique_items(self):  # show_phone
        if self.phones:
            list_phones = [str(p) for p in self.phones]
            return ", ".join(list_phones)
        return 'Empty'

    @property
    def record(self):
        return {
            'name': self.name.value,
            'phones': self.show_unique_items(),
            'birthday': self.birthday.value if self.birthday.value != '' else 'Empty',
            'email': self.email.value if self.email.value != '' else 'Empty',
            'address': self.address.value if self.address.value != '' else 'Empty'
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

    def create_and_add_record(self,
                              name: str,
                              phone: str,
                              birthday: str | None = None,
                              email: str | None = None,
                              address: str | None = None):
        record = AddressRecord(Name(name),
                               Phone(phone),
                               Birthday(birthday),
                               Email(email),
                               Address(address))
        self.add_record(record)

        return f"Added contact {record}"

    def add_item_s(self, name, phone: str):
        for record in self.data:
            if record.name.value == name:
                record.phones.add(Phone(phone))

    def del_item_s(self, name, phone):
        for record in self.data:
            if record.name.value == name:
                record.phones.discard(Phone(phone))

    def change_item_s(self, name: str, old_phone: str, phone: str):  # зміна телефону
        """
        Change phone(s) number of specify AddressBook record
        Arguments:
            name: string
            old_phone: string
            phone: string
        Returns:
            String.
        """
        old_phone_title = Phone(old_phone)
        for record in self.data:
            if record.name.value == name:
                if record.phones:
                    self.add_item_s(name, phone)
                    self.del_item_s(name, old_phone)

                return (
                    f'For user [ {record.name.value} ] had been changed phone number! \n'
                    f' Old phone number: {old_phone_title.value} \n'
                    f' New phone number: {record.phones}'
                )
        return f'Not found contact for name {name}'

    def item(self, name: str):  # показати номер телефону
        """
        Show phone(s) number of specify AddressBook record
        Arguments:
            name: string
        Returns:
            String.
        """
        for record in self.data:
            if record.name.value == name:
                return f"Phone(s) of {name} is: {record.phones}"
        return f"Phone for user {name} not found"

    def record_table_maker(self, counter: int, record: AddressRecord):
        row_table = '|{:^6}|{:<15}|{:^38}|{:^12}|{:^25}|{:^40}|\n'.format(counter, record.name.value, record.show_unique_items(
        ), record.birthday.value if record.birthday.value != '' else 'Emty', record.email.value if record.email.value != '' else 'Emty', record.address.value if record.address.value != '' else 'Emty')
        return row_table

    def header_table_maker(self):
        return '='*143 + '\n' + '|{:^6}|{:<15}|{:^38}|{:^12}|{:^25}|{:^40}|\n'.format('No.', 'Name', 'Phone(s)', 'Birthday', 'Email', 'Address') + '='*143 + '\n'

    def foter_table_maker(self):
        return '='*143 + '\n'

    def show_all(self):
        """
        Show all records of AddressBook
        Arguments:

        Returns:
            The table with columns of fields. Each row is unique record.
        """
        self.step = 0
        result = ''
        header = self.header_table_maker()
        foter = self.foter_table_maker()
        counter = 0
        for record in self.data:
            counter += 1
            result += self.record_table_maker(counter, record)
        counter = 0
        result_tbl = header + result + foter

        return result_tbl

    def show_n(self, n: int):
        """
        Show number of records of AddressBook
        Arguments:
            n: integer
        Returns:
            The table with columns of fields. Each row is unique record. "n" is a step of showing rows
        """
        n = int(n)
        if n > 0:
            if len(self.data) - self.step >= n:

                result = ''
                header = self.header_table_maker()
                foter = self.foter_table_maker()
                counter = 0
                for record in self.data[self.step:self.step+n]:
                    self.step += 1
                    counter += 1
                    result += self.record_table_maker(counter, record)
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

            result = f' {self.current_value + 1} | Name: {self.data[self.current_value].name.value}, Phone(s):{self.data[self.current_value].phones}, Birthday: {self.data[self.current_value].birthday or "Empty"}, Email: {self.data[self.current_value].email or "Empty"}, Address: {self.data[self.current_value].address or "Empty"}'
            self.current_value += 1
            return result

        raise StopIteration

    def search(self, pattern: str):
        """
        Show all records of AddressBook wtat find pattern
        Arguments:
            pattern: string
        Returns:
            The table wit columns of fields. Each row is unique record.
        """
        pattern_searched = str(pattern.strip().lower().replace(' ', ''))
        result = ''
        header = self.header_table_maker()
        foter = self.foter_table_maker()
        counter = 0

        for record in self.data:
            counter += 1

            for field in record.__dict__.values():
                value = str(field).strip().lower().replace(' ', '')
                if value.find(pattern_searched) != -1:
                    result += self.record_table_maker(counter, record)
                    break

        counter = 0
        result_tbl = header + result + foter
        return result_tbl

    def save(self):
        """
        Save all new editings of records of AddressBook
        Arguments:

        Returns:
            Nothing.
        """
        with open(self.file_name_save, 'wb') as file:
            pickle.dump(self.data, file)

    def load(self):
        """
        Load the records of AddressBook
        Arguments:

        Returns:
            Nothing.
        """
        with open(self.file_name_save, 'rb') as file:
            self.data = pickle.load(file)
        return self.data


if __name__ == "__main__":
    pass
