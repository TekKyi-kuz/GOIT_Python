from collections import UserDict
from datetime import datetime
from datetime import date
import math
import re


class AddressBook(UserDict):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.current_page = 0
        self.records_on_the_page = 2
    def add_record(self,record):
        self.data [record.name.value] = record

    def __iter__(self):
        return self

    def __next__(self):
        if  self.current_page < int(math.ceil(len(self.data)/self.records_on_the_page)) :
            keys = list(self.data.keys())
            r_list = []  
            for i in range(self.current_page*self.records_on_the_page ,min([(self.current_page+1)*self.records_on_the_page,len(self.data)])):
                a_dict = {}    
                a_dict["Name"] = keys[i]
                a_dict["Phones"]= [x.value for x in self.data[keys[i]].phones]
                if type(self.data[keys[i]].birthday)!=type(""):
                    a_dict["Birthday"]= str(self.data[keys[i]].birthday.value)
                    a_dict["Days to Birthday"] = self.data[keys[i]].days_to_birthday()
                r_list.append(a_dict)
            
            self.current_page+=1
            return r_list
        raise StopIteration
     

class Record:
    def __init__(self, name):
        self.phones = list()
        self.birthday = ""
        self.name = Name(name)
        
    def add_phone(self,phone):
        phone = Phone(phone)
        self.phones.append(phone)
        
    def del_phone(self,phone):
        phone = Phone(phone)
        self.phones = list(filter(lambda x: x.value!=phone.value, self.phones))

    def edit_phone(self,phone, new_phone):
        if phone in [x.value for x in self.phones]:
            self.del_phone(phone)
            self.add_phone(new_phone)
            
    def add_birthday(self,birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        date1 = datetime(datetime.now().timetuple().tm_yday, self.birthday.value.timetuple().tm_mon, self.birthday.value.timetuple().tm_mday)
        delta = date1.timetuple().tm_yday - datetime.now().timetuple().tm_yday
        if delta > 0:
            return delta
        else:
            date1 = datetime(datetime.now().timetuple().tm_year+1, self.birthday.value.timetuple().tm_mon, self.birthday.value.timetuple().tm_mday)
            date2 = datetime(datetime.now().timetuple().tm_year, datetime.now().timetuple().tm_mon, datetime.now().timetuple().tm_mday)
            delta = date1 - date2
            return str(delta.days)
        
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        print(f"{self.__dict__}")

    @property
    def value(self):
       return self.__value    

    @value.setter
    def value(self, value_):
       if len(value_) > 0:
          self.__value = value_
            
class Name(Field):
    def __init__(self, name):
        self.__value = name

    @property
    def value(self):
       return self.__value    

    @value.setter
    def set_value(self, value):
       if len(value) > 0:
          self.__value = value    
        
class Phone(Field):
    def __init__(self, phone):
        self.value = phone

    @property
    def value(self):
       return self.__value

    @value.setter
    def value(self, phone):
       if re.search('\+\d{12}', phone) != None:
          self.__value = phone
       else:
          raise  ValueError("Phone should be in the next format: '+XXXXXXXXXXXX' (12 digits)")
 
            
class Birthday(Field):
    def __init__(self, birthday):
        self.value = birthday

    @property
    def value(self):
       return self.__value
    
    @value.setter
    def value(self, birthday):
       if re.search('\d{2}\.\d{2}\.\d{4}', birthday) != None:
          self.__value = datetime.strptime(birthday, '%d.%m.%Y').date()
       else:
          raise  ValueError("Birthday should be in the next format: 'dd.mm.yyyy'")


        
r = Record('Tatyana')
r1 = Record('Vladyslav')
r3 = Record('Vera')


r.add_phone('+380972248800')
r.add_phone('+380502248811')
r.edit_phone('+380502248811','+380502248800')
r1.add_phone('+380681085720')
r1.add_phone('+380681085721')
r3.add_phone('+380976706960')


#print(type(Phone('+380972248800')))
print(r.name.value)
for p in r.phones:
    print(p.value)

a = AddressBook("Work telephones")
b = Birthday('24.06.1977')
#b.value='24.06.1977'
r.add_birthday(b)
print(r.days_to_birthday())
a.add_record(r)
a.add_record(r1)
a.add_record(r3)

for page in a:
    print(page)
    