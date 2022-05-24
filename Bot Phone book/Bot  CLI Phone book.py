import re

exit_command = ["good bye", "close", "exit"]

phone_book = {
"Tatiana" : "+380972248800",
"Vladyslav": "+380676706960"
    }

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

def is_correct_input(data):
    name = ""
    phone = ""
    message =""
    is_correct_input = re.search("[a-z][a-zA-Zа-яА-Я1-9]{1,100} \+?[{0,1}\d \-\(\)]*$",data)
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

def print_dict(dict):
    for key in dict.keys():
        print(key," ",dict[key])

def hello_(data):
    return "How can I help You?"

def add_(data):
    name, phone, message = is_correct_input(data)
    if message == "":
            if name in phone_book.keys() and phone == phone_book[name]:
                print ("Contact is already exist with exactly the same number")
            elif name not in phone_book.keys() and phone in phone_book.values():     
                print ("Another contact has this number")
            elif name in phone_book.keys() and  phone not in phone_book.values():
                choose = ""
                while choose not in ["y","Y","n","N"]:
                    choose = input("Contact already exist with another phone number. Press [Y] if You would like to rewrite it or [N] otherwise: ")
                    if choose in ["y","Y"]:
                        phone_book[name] = phone
                        print ("Contact successfully changed")
                    elif choose in ["n","N"]:
                        print ("Contact left unchanged")
                        return "Please choose command"
                    else: print ("Choose Y or N")

            else:
                phone_book[name] = phone
                print ("Contact successfully added to phone_book")
    else:
        print (message)
        print ("Please use next format for add comand: ", exec_command["add"][1])    
    return "Please choose command"

def change_(data):
    name, phone, message = is_correct_input(data)
    if message == "":
        if name in phone_book.keys():
            phone_book[name] = phone
            print("Contact successfully changed")
        else:
            print("Contact not in your phone book")
    else:
        print (message)
        print ("Please use next format for add comand: ", exec_command["change"][1]) 
    return "Please choose command"    

def phone_(data):
    name = data.strip().rstrip().lower()
    find_count = 0
    for contact in phone_book.keys():
       match_ = re.search("\w*"+name+"\w*", contact.lower())
       if match_!=None: 
           print(contact, " ", phone_book[contact])
           find_count+=1
    if find_count == 0:
       print("Couldn't find ", name, " in the phone book")
    return "Please choose command"

def show_all(data):
    print_dict(phone_book)
    return "Please choose command"

def help_(command):
    print("List of available commands: ")
    for key in exec_command.keys():
        print (exec_command[key][1])
    return "Please choose command"

# command dictionary {command: [commandhandler_, command description, number of parameters]}
exec_command = {
    "hello": [hello_, "hello", 0],
    "add": [add_, "add [name] [phone]", 2],
    "change": [change_, "change [name] [phone]", 2],
    "phone": [phone_, "phone [name]", 1],
    "show all": [show_all, "show all", 0],
    "help": [help_, "help",0]
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
        command = input(communication_str+": ")
        communication_str = parser(command)
        
listener()  
