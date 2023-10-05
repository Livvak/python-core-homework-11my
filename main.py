from collections import UserDict

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

        # self.phone = ''
        # self.phone_for_check = phone
        self.phone = self.valid_phone(phone)

        # if self.valid_phone(phone) == None:
        #     self.phone = ''

    def valid_phone(self, phone: str):
        if len(phone) != 10:
            print("Номер не 10 знаков")
            raise ValueError
        if not phone.isdigit():
            print("Номер долен состоять только из цифр")
            raise ValueError
        return phone

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []


    def add_phone(self, phone):
        tel = Phone(phone)
        if tel.valid_phone(phone):
            self.phones.append(tel)

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



    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def __init__(self):
        self.data = dict()

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

def main():

    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
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