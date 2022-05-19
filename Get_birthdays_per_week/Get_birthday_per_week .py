from datetime import datetime, timedelta

birthday_dict = {} 

users_collegues_dict = [{'name': 'Tetiana', 'birthday':'1977.5.28'}, 
                 {'name': 'Vladyslav', 'birthday':'2000.5.22'},
                 {'name': 'Olga', 'birthday':'1988.5.23'}, 
                 {'name': 'Nadya', 'birthday':'1956.5.24'},
                 {'name': 'Katerina', 'birthday':'1878.5.25'},
                 {'name': 'Svetlana', 'birthday':'1999.5.26'},
                 {'name': 'Petro', 'birthday':'1968.5.27'},
                 {'name': 'Vera', 'birthday':'1977.5.24'},
                 {'name': 'Veronika', 'birthday':'1989.5.22'}]

days ={ 0:'Monday',
        1:'Tuesday',
        2:'Wednesday',
        3:'Thursday',
        4:'Friday',
        5:'Saturday',
        6:'Sunday'}  

current_date = datetime.now().date()

from datetime import datetime, timedelta

birthday_dict = {}

users_collegues_dict = [
    {"name": "Tetiana", "birthday": "1977.5.28"},
    {"name": "Vladyslav", "birthday": "2000.5.22"},
    {"name": "Olga", "birthday": "1988.5.23"},
    {"name": "Nadya", "birthday": "1956.5.24"},
    {"name": "Katerina", "birthday": "1878.5.25"},
    {"name": "Svetlana", "birthday": "1999.5.26"},
    {"name": "Petro", "birthday": "1968.5.27"},
    {"name": "Vera", "birthday": "1977.5.24"},
    {"name": "Veronika", "birthday": "1989.5.22"},
]

days = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

current_date = datetime.now().date()


def get_birthdays_per_week(users):
    start_next_week = (current_date - timedelta(days=current_date.weekday()) + timedelta(days=7))
    for colleague in users:
        date_b = datetime.strptime(colleague["birthday"].replace(colleague["birthday"].split(".")[0], str(current_date.year)),"%Y.%m.%d",).date()
        if date_b >= start_next_week - timedelta(days=2) and date_b < start_next_week + timedelta(days=5):
            if date_b.weekday() in (5, 6):
                if days[0] not in birthday_dict.keys():
                    birthday_dict[days[0]] = [colleague["name"]]
                else:
                    birthday_dict[days[0]].extend([colleague["name"]])
            else:
                if days[date_b.weekday()] not in birthday_dict.keys():
                    birthday_dict[days[date_b.weekday()]] = [colleague["name"]]
                else:
                    birthday_dict[days[date_b.weekday()]].extend([colleague["name"]])
    for day_b in birthday_dict.keys():
        print(day_b, ":")
        for name_c in birthday_dict[day_b]:
            print("    " + name_c)
    return None


get_birthdays_per_week(users_collegues_dict)
