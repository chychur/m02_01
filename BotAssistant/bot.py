from datetime import datetime
from source.addressbook import AddressBook
from source.notebook import NoteBook
from source.scripts.sorter import Sorter


class Bot:

    def __init__(self):
        self.file_name_log = 'BotAssistant/storage/logs.txt'
        self.adressbook = AddressBook()
        self.notebook = NoteBook()
        self.sorter = Sorter()

    def parse_input(self, user_input):
        command, *args = user_input.split()
        command = command.lstrip()

        handler = self.get_bot_commands().get(command.lower())
        if handler:
            return handler,
        handler = self.get_modules_commands().get(command.lower())
        if handler is None:
            if args:
                command = command + ' ' + args[0]
                args = args[1:]
                handler = self.get_modules_commands().get(command.lower())
                return handler,
            else:
                return self.unknown_command, user_input
        return handler, *args

    def unknown_command(self, command):
        return f"{command} not persist"

    def hello_command(self):
        command_bot = '\n'.join(self.get_bot_commands().keys())
        command_book = '\n'.join(self.get_modules_commands().keys())
        message = (
            f"How can I help you?\n "
            f"Available command:\n"
            f"{command_bot}"
            f"{command_book}"
        )
        return message

    def exit_command(self):
        return 'EXIT'

    def get_bot_commands(self):
        return {
            'help': self.hello_command,                              # привітання
            'exit': self.exit_command,                               # вихід
            'goodbye': self.exit_command,                            # вихід
            'close': self.exit_command                               # вихід
        }

    def get_modules_commands(self):
        return {
            # Addressbook
            'add-contact': self.adressbook.create_and_add_record,    # додавання запису
            'add-phone': self.adressbook.add_item_s,                 # додавання телефону
            'del-phone': self.adressbook.del_item_s,                 # видалення телефону
            'change-phone': self.adressbook.change_item_s,           # зміна телефону
            'all-contacts': self.adressbook.show_all,                # показати всі записи
            'n-contacts': self.adressbook.show_n,                    # показати N-записів
            'phone': self.adressbook.item,                           # показати телефон
            'search-contact': self.adressbook.search,                # пошук по запису
            # NoteBook
            'add-note': self.notebook.create_and_add_record,         # додавання запису
            'add-tag': self.notebook.add_item_s,                     # додавання телефону
            'del-tag': self.notebook.del_item_s,                     # видалення телефону
            'change-tag': self.notebook.change_item_s,               # зміна телефону
            'all-notes': self.notebook.show_all,                     # показати всі записи
            'n-notes': self.notebook.show_n,                         # показати N-записів
            'tag': self.notebook.item,                               # показати телефон
            'search-note': self.notebook.search,                     # пошук по запису
            # Sorter
            'sort': self.sorter.sort                                 # сортувальник
        }

    def loader(self):
        self.adressbook.load()
        self.notebook.load()
        self.log(
            f"{self.__class__.__name__} has been loaded!")

    def autosaver(self):
        self.adressbook.save()
        self.notebook.save()
        self.log(
            f"{self.__class__.__name__} has been saved!")

    def log(self, log_message: str, prefix: str | None = None):
        current_time = datetime.strftime(datetime.now(), '%H:%M:%S')
        prefixes = {
            'com': f'[{current_time}] [Module] USER INPUT : {log_message}',
            'res': f'[{current_time}] BOT RESULT : \n{log_message}\n',
            'err': f'[{current_time}] !!! === ERROR MESSAGE === !!! {log_message}\n',
            None: f'[{current_time}] {log_message}'
        }

        message = prefixes[prefix]

        with open(self.file_name_log, 'a') as file:
            file.write(f'{message}\n')

    def run(self):
        while True:

            # self.adressbook.load()
            self.loader()
            user_input = input('Please enter command and args: ')
            self.log(user_input, prefix='com')
            handler, *data = self.parse_input(user_input)
            try:
                result = handler(*data)

                if result == 'EXIT':
                    print('Good bye!')
                    break
                print(result)
                self.log(result, prefix='res')
                self.autosaver()
                # self.adressbook.autosave()
            except (ValueError, IndexError, TypeError) as exp:
                print(exp)
                self.log(exp, prefix='err')
                continue


if __name__ == "__main__":
    my_bot = Bot()
    my_bot.run()
