from collections import UserDict
from datetime import date, datetime
import pickle

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)

class Name(Field):

    @Field.value.setter
    def value(self, value: str):
        if len(value) < 3:
            # print("Имя не менее 3 знаков")
            raise ValueError("Имя не менее 3 знаков")

        if not value.isalpha():
            # print("Имя должно состоять только из букв")
            raise TypeError("Имя должно состоять только из букв")

        self._value = value

class Phone(Field):

    @Field.value.setter
    # def valid_phone(self, phone: str):
    def value(self, value: str):
        if len(value) != 10:
            # print("Номер не 10 знаков")
            raise ValueError("Номер не 10 знаков")
        if not value.isdigit():
            # print("Номер долен состоять только из цифр")
            raise TypeError("Номер долен состоять только из цифр")
        self._value = value

class Birthday(Field):

    @Field.value.setter
    def value(self, value: str):
        if not value.find('.'):
            raise ValueError('Формат дати: DD.MM.YYYY')
        date_b = value.split('.')
        if len(date_b) != 3:
            raise ValueError('Формат дати: DD.MM.YYYY')
        try:
            birthday_date = date(year=int(date_b[2]), month=int(date_b[1]), day=int(date_b[0]))
        except ValueError:
            raise ValueError("Введіть коректну дату")
        else: self._value = value


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
            if tel.value == item.phone:
                self.phones.remove(item)

    def edit_phone(self, phone_old, phone_new):
        tel_new = Phone(phone_new)
        for item in self.phones:
            if phone_old == item.value:
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
            if tel.value == item.value:
                return item


    def days_to_birthday(self):
        if not self.birthday:
            raise ValueError("Дата народження не задана")

        def is_leap_year(year):
            return True if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else False

        date_b = self.birthday.value.split('.')
        birthday_date = date(year=int(date_b[2]), month=int(date_b[1]), day=int(date_b[0]))
        birthday = birthday_date
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
            if _name.value == key:
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

    def save_to_file(self):
        with open("addr_book.bin", "wb") as fh:
            fh.write(pickle.dumps(self))

    def load_from_file(self):
        with open("addr_book.bin", "rb") as fh:
            return pickle.loads(fh.read())




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
    jane_record.add_birthday("31.12.2000")
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
    book.save_to_file()

    # Завантаження об'єктів із файлу в новий об'єкт
    book_recovered = book.load_from_file()


    book_recovered.delete("Jane")

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == '__main__':
    main()
