import csv
import re
import os

__DEFAULT_PASSWORD = "SecretPassword1"
__DEFAULT_FILEPATH = "linux_users.csv"

__FILE_HEADER = []
__FILE_ROWS = []

__DATA = []

__DEFAULT_USER_DIR = ""

def file_open():
    with open(__DEFAULT_FILEPATH, 'r') as file:
        reader = csv.reader(file)
        __FILE_HEADER = next(reader)
        for row in reader:
            __FILE_ROWS.append(row)

def file_format_username(last_name: str, first_name: str):
    raw_uname = first_name[0] + last_name
    return re.sub(r'[\W_]+', '', raw_uname)

def file_duplicate_find_next_uname(curnum:int, uname:str):
    for elements in __DATA:
        if elements[0] == uname+((str)(curnum)):
            file_duplicate_find_next_uname(curnum + 1, uname)
        else:
            return curnum

def file_parse():
    uname = ""
    badinfo = False
    for userdat in __FILE_ROWS:
        exists = False
        for user in __DATA:
            if (userdat[1] == "") | (userdat[2] == ""):
                badinfo = True
            ##elif ((generate_usernames(userdat[1],userdat[2]).isalpha())):
                ##badinfo = True
            elif file_format_username(userdat[1], userdat[2]) == user[0]:
                exists = True
        if exists:
            uname = file_duplicate_find_next_uname(1, file_format_username(userdat[1], userdat[2]))
        elif (exists==False) & (badinfo==False):
            uname = file_format_username(userdat[1], userdat[2])
        else:
            uname = ""
        if (type(uname) != str):
            uname = ""
        elif (uname.isalpha()==False):
            uname = ""
        userarr:str = []
        userarr.append(uname)
        userarr.append(userdat[0])
        userarr.append(userdat[3])
        userarr.append(userdat[5])
        userarr.append(userdat[6])
        __DATA.append(userarr)

def users_create_call():
    for user in __DATA:
        user_create_single(user[0].lower(), user[1].lower(), user[2].lower(), user[3].lower(), user[4].lower())

def user_create_single(uname, employee_ID, office, department, group):
    if employee_ID == "":
        print("empty ID")
    elif uname == "":
        print("invalid username")
    elif office == "":
        print("empty office")
    elif department == "":
        print("empty department")
    elif group == "":
        print("empty group")
    elif group == "office":
        os.system("sudo mkdir " + __DEFAULT_USER_DIR + "/" + department)
        os.system("sudo groupadd " + group)
        os.system("sudo adduser " + uname +
                  " -d " + __DEFAULT_USER_DIR + "/" + department + "/" + uname +
                  " -s /bin/csh" +
                  " -p password" +
                  " -f 0 -m" +
                  " -g " + group)
        print("Created account for user: " + uname + " | ID: " + employee_ID)
    else:
        os.system("sudo mkdir " + __DEFAULT_USER_DIR + "/" + department)
        os.system("sudo groupadd " + group)
        os.system("sudo adduser " + uname +
                  " -d " + __DEFAULT_USER_DIR + "/" + department + "/" + uname +
                  " -s /bin/sh" +
                  " -p password" +
                  " -f 0 -m" +
                  " -g " + group)
        print("Created account for user: " + uname + " | ID: " + employee_ID)

def main():
    file_open()
    file_parse()
    users_create_call()

main()
