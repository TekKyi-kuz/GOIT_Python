from collections import UserDict
import re
class AddressBook(UserDict):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def add_record(self,record):
        self.data [record.name.value] = record
     

class Record:
    def __init__(self, name):
        self.phones = list()
        self.name = Name(name)
    def add_phone(self,phone):
        if type(phone)!= type(Phone("")):
            phone = Phone(phone)
        self.phones.append(phone)
    def del_phone(self,phone):
        if type(phone) != type(Phone("")):
            phone = Phone(phone)
        self.phones = list(filter(lambda x: x.value!=phone.value, self.phones))
    def edit_phone(self,phone, new_phone):
        if type(phone)!=type(Phone("")):
            phone = Phone(phone)
        if phone.value in [x.value for x in self.phones]:
            self.del_phone(phone)
            self.add_phone(new_phone)
class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        print(f"{self.__dict__}")
class Name(Field):
    def __init__(self, name):
        self.value = name
class Phone(Field):
    def __init__(self, phone):
        if re.search('\+\d{12}', phone) != None:
            self.value = phone
        
r = Record('Tetiana Oliinyk')
r.add_phone(Phone('+380972248800'))
r.add_phone('+380976706960')
r.edit_phone('+380976706960','+380681085720')
print(type(Phone('+380972248800')))
print(r.name.value)
for p in r.phones:
    print(p.value)

a = AddressBook("Work telephones")
a.add_record(r)
print(a.data[r.name.value].phones)