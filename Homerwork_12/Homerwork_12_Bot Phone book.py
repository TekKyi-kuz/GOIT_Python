from collections import UserDict
from datetime import datetime
from datetime import date
import math
import re
import json

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
                r_list.append(a_dict)
            self.current_page+=1
            return r_list
        else:
            self.current_page = 0
        raise StopIteration

    def delete(self, name):
        if name in self.data.keys():
            print("Input 'Y' to delete the record for contact: ", name)
            if input() in ["Y", "y"]:
                self.data.pop(name)
                print("Record deleted")
            else:
                print("Delete of the record cancelled")

    def dump(self, file):
        with open(file, 'w+') as write_file:
            dump_dict ={self.name:{}}
            store_records_on_the_page = self.records_on_the_page
            self.records_on_the_page = 1
            id =1
            for page in self:
                dump_dict[self.name]["RecID"+str(id)]= page[0]
                id+=1
            json.dump(dump_dict, write_file)
            self.records_on_the_page = store_records_on_the_page
            print("Data exported to the file")

    def load(self, file):
        with open(file, 'r') as read_file:
            data = json.load(read_file)
            self.name= list(data.keys())[0]
            for name in list(data[self.name].keys()):
                record = data[self.name][name]
                rec = Record(record["Name"])
                if "Phones" in record.keys():
                    for phone in record["Phones"]:
                        rec.add_phone(Phone(phone))
                if "Birthday" in record.keys():
                    lst = record["Birthday"].split("-")
                    birthday = Birthday(lst[2]+"."+lst[1]+"."+lst[0])
                    rec.add_birthday(birthday)
                self.add_record(rec)
            print ("Data have been loaded from file")        

    def find(self, request):
        result_lst = []
        for name in self.data.keys():
            search_list = [name]
            search_list.extend([phone.value for  phone in self.data[name].phones])
            for field in search_list:
                if request[0]=="+":
                    request = request[1:]    
                if re.search(request.upper(),field.upper())!=None:
                    result_lst.append(name)
                    break
        return result_lst 
               
class Record:
    def __init__(self, name):
        self.phones = list()
        self.birthday = ""
        self.name = Name(name)
      
    def add_phone(self,phone):
        if phone.value not in [ph.value for ph in self.phones]:
            self.phones.append(phone)

    def del_phone(self,phone):
        self.phones = list(filter(lambda x: x.value!=phone, self.phones))

    def edit_phone(self,phone, new_phone):
        status = ""
        if phone in [x.value for x in self.phones]:
            self.del_phone(phone)
            self.add_phone(Phone(new_phone))
        else:
            status = "Can't find the number "+phone+" in the phone list"
        return status    

          
    def add_birthday(self,birthday):
        self.birthday = birthday

    def days_to_birthday(self):
        date1 = datetime(datetime.now().timetuple().tm_yday, self.birthday.value.timetuple().tm_mon, self.birthday.value.timetuple().tm_mday)
        delta = date1.timetuple().tm_yday - datetime.now().timetuple().tm_yday
        if delta > 0:
            return str(delta)
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
          return False 


##################################################
#         CLI BOT section                        #
##################################################

exit_command = ["good bye", "close", "exit"]


def format_phone_number(func):
   def inner(phone):
      result=func(phone)
      if len(result) == 12:
          result='+'+result
      else: result='+38'+result    
      return result
   return inner
            

@format_phone_number
def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
    )
    return new_phone

def is_correct_input_add(data):
    name = ""
    phone = ""
    message =""
    is_correct_input = re.search("[a-zA-Zа-яА-Я1-9]{1,100} \+?[{0,1}\d \-\(\)]*$",data)
    if is_correct_input!=None:
        match_ = re.search(" \+?[{0,1}\d \-\(\)]*$", data)
        if match_!=None:
            phone = sanitize_phone_number(data[match_.start():match_.end()].strip())
            name = data[:match_.start()].strip().rstrip()
            if len(phone)!=13:
                message = "Incorrect telephone number. Use (+)(Country code)(XXX Operator code) XXX XX XX"
    else:
        message = "Incorrect command format"
    return (name, phone, message)


def is_correct_input_change(data):
    name = ""
    phone_old = ""
    phone_new = ""
    message =""
    is_correct_input = re.search("[a-zA-Zа-яА-Я1-9]{1,100} \+?[{0,1}\d\-\(\)]* \+?[{0,1}\d\-\(\)]*$",data)
    if is_correct_input!=None: 
        phone_old, phone_new = data.split(" ")[-2:]
        name = data[0: len(data)-len(phone_old)-len(phone_new)-2] 
        phone_old = sanitize_phone_number(phone_old)
        phone_new = sanitize_phone_number(phone_new)
        if len(phone_new)!=13 or len(phone_old)!=13:
                message = "Incorrect telephone number. Use (+)(Country code)-(XXX Operator code)-XXX-XX-XX"
    else:
        message = "Incorrect command format"
    return (name, phone_old, phone_new, message)


def hello_(data):
    return "How can I help You?"

def add_(data):
    name, phone, message = is_correct_input_add(data)
    if message == "":
            print('Name ', name, ' phone ', phone,' message', message)
            if name in a.data.keys() and phone in [ph.value for ph in a.data[name].phones]:
                print ("Contact is already exist with exactly the same number")
            elif name not in a.data.keys() and phone in a.find(phone):     
                print ("Another contact has this number")
            elif name in a.data.keys() and  phone not in a.find(phone):
                a.data[name].add_phone(Phone(phone))
                print ("Contact phone list  successfully appended")
            else:
                r = Record(name)
                p = Phone(phone)
                r.add_phone(p)
                a.add_record(r)
                print ("Contact successfully added to phone_book")
    else:
        print (message)
        print ("Please use next format for add comand: ", exec_command["add"][1])    
    return "Please choose command"

def change_(data):
    name, phone_old, phone_new, message = is_correct_input_change(data)
    if message == "":
        if name in a.data.keys():
            message  = a.data[name].edit_phone(phone_old, phone_new)
            if  message == "":
                print("Contact successfully changed")
            else:
                print(message)
        else:
            print("Contact not in your phone book")
    else:
        print (message)
        print ("Please use next format for add comand: ", exec_command["change"][1]) 
    return "Please choose command"    

def find_(data):
    name = data.strip().rstrip()
    res_lst = a.find(data)
    if res_lst == []:
        print("Couldn't find ", name, " in the phone book")
    else:
        print("Found next contacts:")
        for contact in res_lst:
            print(contact)
    return "Please choose command"

def show_all(data):
    adress_book = a    
    for page in adress_book:
        for record in page:
            print("Name:", record["Name"])
            print("Phone list:")
            for phone in record["Phones"]:
                print(phone)
            if "Birthday" in record.keys():
                print ("Birthday: ", record["Birthday"])
        input("Press enter to continue")
     
    return "Please choose command"

def help_(command):
    print("List of available commands: ")
    for key in exec_command.keys():
        print (exec_command[key][1])
    return "Please choose command"

def birthday_(data):
    cmnd_lst = data.split(" ")
    birthday = cmnd_lst[-1]
    name = data[0:len(data) - len(birthday)-1]
    if a.find(name)!=[]:
        b=Birthday(birthday)
        if b == False:
            return "Birthday should be in the next format: 'dd.mm.yyyy'"
        else: 
            a.data[name].add_birthday(b)
            return "Birthday setted successfully"

def delete_(data):
    res = re.search(" \+?[\d\-\(\)]*$",data)
    name = data.strip().split(" ")[0]
    if name in a.data.keys():
        if res == None:
            for record in a.find(name):
                print(a.find(name))
                a.delete(record)
        else:
            phone = data.strip().split(" ")[1]
            phone = sanitize_phone_number(phone)
            if phone in [ph.value for ph in a.data[name].phones]:
                a.data[name].delete_phone(phone)
                print ("Phone deleted succesfully")
            else:
                print( "Couldn't find this phone number for the "+name)
    else:
        print ("Couldn't find user "+name)
    return "Please choose command"

def save_(data):
    a.dump("Work telephones.json")
    return "Please choose command"
    
exec_command = {
    "hello": [hello_, "hello", 0], 
    "add": [add_, "add [name] [phone]", 2], 
    "change": [change_, "change [name] [phone_old] [phone_new]", 2], 
    "find": [find_, "phone or name", 1], 
    "show all": [show_all, "show all", 0],
    "help": [help_, "help",0], 
    "birthday": [birthday_, "birthday [name] [date of birthday dd.mm.yyyy]",1],
    "delete": [delete_, "delete [name] [phone (optional)]", 2],
    "save": [save_, "save", 0]
             }


def handler(command, data):
    return exec_command[command][0](data.replace(command+" ",""))
    

def parser(input_str):
    for token in exec_command.keys():
        if token in input_str:
            return handler(token, input_str.replace(token+" ", ""))
    return "Input error, please type 'help' for commands description"
            
def listener():
    command = ""
    communication_str = "CLI phone book bot looking for your command"
    while (command) not in exit_command:
        print(communication_str+": ")
        command = input()
        communication_str = parser(command)


a = AddressBook("Work telephones")
a.load("Work telephones.json")
listener() 
a.dump("Work telephones.json")