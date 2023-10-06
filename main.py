from collections import UserDict
from datetime import date, datetime
import pickle

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)
        if self.valid_name(name) == None:
            self.name = ''
        else:
            self.name = name

    def valid_name(self, name: str):
        if len(name) < 3:
            print("Имя не менее 3 знаков")
            return
        if not name.isalpha():
            print("Имя должно состоять только из букв")
            return
        return name

class Phone(Field):
    # реалізація класу
    def __init__(self, phone: str):
        super().__init__(phone)
        # self.phone = self.valid_phone(phone)
        self._phone = phone


    @property
    def phone(self):
        return self._phone

    @phone.setter
    def valid_phone(self, phone: str):
        if len(phone) != 10:
            print("Номер не 10 знаков")
            raise ValueError
        if not phone.isdigit():
            print("Номер долен состоять только из цифр")
            raise ValueError
        self._phone = phone

class Birthday(Field):
    def __init__(self, birthday):
        super().__init__(birthday)
        self.birthday_date = None
        self._birthday = birthday

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, day: str):
        print("find")
        if not day.find('.'):
            print("find")
            print('Формат дати: DD.MM.YYYY')
            raise ValueError
        date_b = day.split('.')
        if len(date_b) != 3:
            print('Формат дати: DD.MM.YYYY')
            raise ValueError
        try:
            self.birthday_date = date(year=int(date_b[2]), month=int(date_b[1]), day=int(date_b[0]))
            print(day)
        except ValueError:
            print("Введіть коректну дату")
        else: self._birthday = day


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_phone(self, phone):
        tel = Phone(phone)
        # if tel.valid_phone(phone):
        self.phones.append(tel)

    def add_birthday(self, birthday):
        day = Birthday(birthday)
        self.birthday = day

    def remove_phone(self, phone):
        tel = Phone(phone)
        for item in self.phones:
            if tel.phone == item.phone:
                self.phones.remove(item)

    def edit_phone(self, phone_old, phone_new):
        tel_new = Phone(phone_new)
        for item in self.phones:
            if phone_old == item.phone:
                idx = self.phones.index(item)
                self.phones.remove(item)
                self.phones.insert(idx, tel_new)
                return
            else:
                print("Номер не знайдено")
                raise ValueError

    def find_phone(self, phone):
        tel = Phone(phone)
        for item in self.phones:
            if tel.phone == item.phone:
                return item


    def days_to_birthday(self, date_b: str):
        Date = Birthday(date_b)

        def is_leap_year(year):
            return True if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else False

        birthday = Date.birthday_date
        today = date.today()
        year = datetime.now().year
        next_birthday = birthday.replace(year=today.year + 1)
        # print(f"Сегодня: {today}   ДР: {birthday}  Следующий ДР: {next_birthday} {year}")
        count_day = (next_birthday - today).days
        if count_day > 366 and is_leap_year(year + 1):
            count_day = count_day - 366
        if count_day > 365 and not is_leap_year(year + 1):
            count_day = count_day - 365

        return count_day

    def verify_birthday(self, birthday: str):
        Date_b = Birthday(birthday)
        if Date_b.birthday_date == None:
            print("Дата не валідна")
            raise ValueError
        print("Дата валідна")

    def verify_phone(self, phone: str):
        Phone_v = Phone(phone)
        if Phone_v.phone == None:
            print("Номер не валідний")
            raise ValueError
        print("Номер валідний")


    def __str__(self):
        if self.birthday:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, Birthday: {self.birthday}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def __init__(self):
        self.data = dict()
        self.current_value = 0

    def add_record(self, obj):
        self.data[str(obj.name)] = obj
        print(f"Ключ {obj.name} со значением {obj.phones} добавлено")

    def find(self, name):
        _name = Name(name)
        for key, val in self.data.items():
            if _name.name == key:
                result = val
                return result

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            print(f'{name} видалено')
        else:
            print(f'{name} не знайдено')

    def __next__(self):
        max_value = len(self.data)
        keys = list(self.data.keys())
        if self.current_value < max_value:
            self.current_value += 1
            return self.data[keys[self.current_value-1]]
        raise StopIteration

    # def __getstate__(self):
    #     attributes = self.__dict__.copy()
    #     attributes['fh'] = None
    #     return attributes
    #
    # def __setstate__(self, value):
    #     self.__dict__ = value
    #     self.fh = open(value['file'])
    #     self.fh.seek(value['position'])


def main():

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_birthday("21.07.2000")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("331-13-2000")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Збереження об'єктів у файл
    with open("addr_book.bin", "wb") as fh:
        fh.write(pickle.dumps(book))
    # Завантаження об'єктів із файлу
    with open("addr_book.bin", "rb") as fh:
        book2 = pickle.loads(fh.read())

    book2.delete("Jane")

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == '__main__':
    main()
    # book = AddressBook()
    # ph = Phone('1234567800')
    # print(ph.phone)
    #
    # bb = 'ddkh'
    # imm = Name(bb)
    # print(imm.name)
    #
    # john_record = Record("John")
    # john_record.add_phone("1234567890")
    # john_record.add_phone("5555555555")
    # print(john_record.name)
    # print(john_record.phones)
    # book.add_record(john_record)
    # print("="*30)
    # john = book.find("John")
    # print(john)
    #
    # book.delete("вв")
    #
    # # ddk = Record(imm.name)
    # # ddk.add_phone(ph.phone)
    # # print(ddk.phones)