from source.cls import RecordType, ModuleType, Name, Tag, Note

import pickle


class NoteRecord(RecordType):

    def __init__(
            self,
            name: Name,
            tag: Tag | None = None,
            note: Note | None = None
    ):

        self.name = name
        self.note = note
        self.tags = set()
        self.add_unique_item(tag)

    def __repr__(self) -> str:
        return f'Record (Name:"{self.name}", Tag(s):"{self.show_unique_items()}", Note:"{self.note or "Empty"}")'

    def __str__(self) -> str:
        return f'Record (Name:"{self.name}", Tag(s):"{self.show_unique_items()}", Note:"{self.note or "Empty"}")'

    def add_unique_item(self, tag):
        if isinstance(tag, str):
            tag = Tag(tag)
        self.tags.add(tag)

    def show_unique_items(self):
        if self.tags:
            list_tags = [str(t) for t in self.tags]
            return ", ".join(list_tags)
        return 'Empty'

    @property
    def record(self):
        return {
            'name': self.name.value,
            'tagss': self.show_unique_items(),
            'birthday': self.note.value if self.note.value != '' else 'Empty',
        }

    def __getitem__(self, item: str):
        return self.record.get(item)


class NoteBook(ModuleType):

    def __init__(self) -> None:
        self.data: list[NoteRecord] = []
        self.current_value = 0
        self.step = 0
        self.file_name_save = 'BotAssistant/storage/NoteBookStorage.bin'

    def __getitem__(self, index):
        return self.data[index]

    def create_and_add_record(self,
                              name: str,
                              tag: str,
                              note: str | None = None
                              ):
        record = NoteRecord(Name(name),
                            Tag(tag),
                            Note(note)
                            )
        self.add_record(record)

        return f"Added note {record}"

    def add_item_s(self, name, tag: str):
        for record in self.data:
            if record.name.value == name:
                record.tags.add(Tag(tag))

    def del_item_s(self, name, tag):
        for record in self.data:
            if record.name.value == name:
                record.tags.discard(Tag(tag))

    def change_item_s(self, name: str, old_tag: str, tag: str):  # зміна тегу
        old_tag_title = Tag(old_tag)
        for record in self.data:
            if record.name.value == name:
                if record.tags:
                    self.add_item_s(name, tag)
                    self.del_item_s(name, old_tag)

                return (
                    f'For note [ {record.name.value} ] had been changed tag! \n'
                    f' Old tag: {old_tag_title.value} \n'
                    f' New tag: {record.tags}'
                )
        return f'Not found tag for note: {name}'

    def item(self, name: str):  # показати тег
        for record in self.data:
            if record.name.value == name:
                return f'Tag(s) of the note "{name}" is: {record.show_unique_items()}'
        return f'Tag for note "{name}" not found'

    def record_table_maker(self, counter: int, record: NoteRecord):
        row_table = '|{:^6}|{:<25}|{:^40}|{:^40}|\n'.format(counter, record.name.value, record.show_unique_items(
        ), record.note.value if record.note.value != '' else 'Emty')
        return row_table

    def header_table_maker(self):
        return '='*116 + '\n' + '|{:^6}|{:<25}|{:^40}|{:^40}|\n'.format('No.', 'Name', 'Tag(s)', 'Note') + '='*116 + '\n'

    def foter_table_maker(self):
        return '='*116 + '\n'

    def show_all(self):
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

            result = f' {self.current_value + 1} | Name: {self.data[self.current_value].name.value}, Phone(s):{self.data[self.current_value].tags}, Birthday: {self.data[self.current_value].note or "Empty"}'
            self.current_value += 1
            return result

        raise StopIteration

    def search(self, pattern):
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
        with open(self.file_name_save, 'wb') as file:
            pickle.dump(self.data, file)

    def load(self):
        with open(self.file_name_save, 'rb') as file:
            self.data = pickle.load(file)
        return self.data

    # def log(self, log_message: str, prefix: str | None = None):
    #     current_time = datetime.strftime(datetime.now(), '%H:%M:%S')
    #     prefixes = {
    #         'com': f'[{current_time}] [Module] USER INPUT : {log_message}',
    #         'res': f'[{current_time}] BOT RESULT : \n{log_message}\n',
    #         'err': f'[{current_time}] !!! === ERROR MESSAGE === !!! {log_message}\n',
    #         None: f'[{current_time}] {log_message}'
    #     }

    #     message = prefixes[prefix]

    #     with open('BotAssistant/storage/logs.txt', 'a') as file:
    #         file.write(f'{message}\n')


if __name__ == "__main__":
    pass
