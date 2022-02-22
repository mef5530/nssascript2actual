#!/usr/bin/env python3
import csv
import re
import os

## @Author Max E. Friedland (mef5530@rit.edu)
## @Date 2/19/2022
## @Filename add_user.py

__DEFAULT_PASSWORD = "SecretPassword1"
__DEFAULT_FILEPATH = "linux_users.csv"

__FILE_HEADER = []
__FILE_ROWS = []

__DATA = []

__DEFAULT_USER_DIR = "/home"

#opens the file and fills the file rows and header
#@peram: null
#@return: null
def file_open():
    with open(__DEFAULT_FILEPATH, 'r') as file:
        reader = csv.reader(file)
        __FILE_HEADER = next(reader)
        for row in reader:
            __FILE_ROWS.append(row)

#removes non alphanumeric text and formats the username
#@peram: first and last name
#@return: (string) formatted username
def file_format_username(last_name: str, first_name: str):
    raw_uname = first_name[0] + last_name
    return re.sub(r'[\W_]+', '', raw_uname)

#recursivly finds the next avaliable username by appending a number on the end
#@peram: username and current appended integer
#@return: (string) next avaliable username
def file_duplicate_find_next_uname(curnum:int, uname:str):
    for elements in __DATA:
        if elements[0] == uname+((str)(curnum)):
            file_duplicate_find_next_uname(curnum + 1, uname)
        else:
            return curnum
#reads the raw info and 1: checks if the data is valid, 2: checks for duplicates, 3: adds the info to the formatted list
#@peram: null
#@return: null

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

#calls user_create_single(...) for each entry in the formatted list of users
#@peram: null
#@return: null
def users_create_call():
    for user in __DATA:
        user_create_single(user[0].lower(), user[1].lower(), user[2].lower(), user[3].lower(), user[4].lower())

#checks if the user data is valid then 1: creates the home dirrectory (command aborts if it already exists,
# 2: creates the group (also is not an issue if the group already exists, 3: creates the user.
#@peram: user info
#@return: null
def user_create_single(uname, employee_ID, office, department, group):
    if employee_ID == "":
        print("\033[1;31;40m empty ID | ID: " + employee_ID + "\033[0;33;40m")
    elif uname == "":
        print("\033[1;31;40m invalid username | ID: " + employee_ID + "\033[0;33;40m")
    elif office == "":
        print("\033[1;31;40m empty office | ID: " + employee_ID + "\033[0;33;40m")
    elif department == "":
        print("\033[1;31;40m empty department | ID: " + employee_ID + "\033[0;33;40m")
    elif group == "":
        print("\033[1;31;40m empty group | ID: " + employee_ID + "\033[0;33;40m")
    elif group == "office":
        os.system("sudo mkdir " + __DEFAULT_USER_DIR + "/" + department)
        os.system("sudo groupadd " + group)
        os.system("sudo adduser " + uname +
                  " -d " + __DEFAULT_USER_DIR + "/" + department + "/" + uname +
                  " -s /bin/csh" +
                  " -p password" +
                  " -f 0 -m" +
                  " -g " + group)
        print("\033[1;32;40m Created account for user: " + uname + " | ID: " + employee_ID + "\033[0;33;40m")
    else:
        os.system("sudo mkdir " + __DEFAULT_USER_DIR + "/" + department)
        os.system("sudo groupadd " + group)
        os.system("sudo adduser " + uname +
                  " -d " + __DEFAULT_USER_DIR + "/" + department + "/" + uname +
                  " -s /bin/sh" +
                  " -p password" +
                  " -f 0 -m" +
                  " -g " + group)
        print("\033[1;32;40m Created account for user: " + uname + " | ID: " + employee_ID + "\033[0;33;40m")

def main():
    file_open()
    file_parse()
    users_create_call()
    print("\033[1;32;40mScript has finished:)\033[0;37;40m")

main()
