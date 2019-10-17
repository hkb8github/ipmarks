import mysql.connector as myconnector
from numpy import *
user_name = "root"
password = "1234"
host_name = "localhost"
database_name = "ipmarks"

def settings(hname, uname, pwd, db):
    global user_name, password, host_name, database_name
    user_name = uname
    password = pwd
    host_name = hname
    database_name = db
    print(database_name)
    

def save_record(table_name, values_list, fields_list=[]):
    conn = myconnector.connect(host=host_name, user=user_name, passwd = password, database=database_name)
    if conn.is_connected():
        sql_query = "insert into " + table_name
        if len(fields_list)>0:
            sql_query += "("
            for x in fields_list:
                print(x)
                sql_query += x +","
            sql_query = sql_query[:-1]
            sql_query += ") "
        sql_query += " values("
        for x in values_list:
            sql_query += "'"+ str(x) +"',"
        sql_query = sql_query[:-1]
        sql_query += ")"
        cursor = conn.cursor()
        cursor.execute(sql_query)
        conn.commit()
        conn.close()
        return True
    else:
        return False

def delete_record(table_name, value, field_name):
    conn = myconnector.connect(host=host_name, user=user_name, passwd = password, database=database_name)
    if conn.is_connected():
        sql_query = "delete from " + table_name + " where {} = '{}'".format(field_name, value)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        conn.commit()
        conn.close()
        return True
    else:
        return False

def execute_sql_query(sql_query):
    conn = myconnector.connect(host=host_name, user=user_name, passwd = password, database=database_name)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute(sql_query)
        conn.commit()
        conn.close()
        return True
    else:
        return False
    
def show_result_in_table(sql_query, width=[], header=[]):
    conn = myconnector.connect(host=host_name, user=user_name, passwd = password, database=database_name)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        #print(len(data))
        if len(data)>0:
            nof = len(data[0])
            print("-"*(sum(width)+len(width)+1))
            heading="|"
            for i, x in zip(range(nof), header):
                x = str(x)
                if len(x) > width[i]:
                    heading += x[:width[i]]
                else:
                    heading += x + " "*(width[i]-len(x))
                heading += "|"
            print(heading)
            print("-"*(sum(width)+len(width)+1))
            if len(width)>0:
                for rec in data:
                    print("|", end="")
                    for x,i in zip(rec, range(nof)):
                        x = str(x)
                        if width[i]>= len(x):
                            v = x + " "*(width[i]-len(x))
                        else:
                            v = x[:i]
                        print(v, end="|")
                    print()
                print("-"*(sum(width)+len(width)+1))                    
            else: #taking width=10
                pass
        else:
            print("No record found")
        conn.close()
        return True
    else:
        return False

def get_result(sql_query):
    conn = myconnector.connect(host=host_name, user=user_name, passwd = password, database=database_name)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        return data
    else:
        return False

    
f_ls=[]
v_ls=['vishi',4,'2012-02-12']

def show_menu(menu_title, options=[], choice="Please enter your choice: "):
    choice += "  "
    a = len(menu_title)%2
    b = len(choice)%2
    if a-b != 0:
        menu_title +=" "
    options.append(choice)
    max_len = len(choice)
    for x in options:
        if len(x) > max_len:
            max_len = len(x)
    if max_len<len(menu_title):
        max_len = len(menu_title)
    max_len +=4
    title_start = (max_len - len(menu_title))//2
    title_start = int(title_start)
    title = "|"+ (" " * title_start + menu_title + " " * title_start) + "|"
    hor_bar = "┌" + "-" * (max_len) + "┐"
    
    print(hor_bar)
    print(title)
    hor_bar = "├" + "-" * (max_len) + "┤"
    print(hor_bar)
    options.pop()
    for x , i in zip(options, range(len(options))):
        op = "|" + str(i+1) + " "
        op +=  options[i] + (" "*(max_len-len(options[i])-len(op)+1)) + "|"
        print(op)
    hor_bar = "└" + "-" * (max_len) + "┘"
    print(hor_bar)
    choice = choice[:-3]
    #ch = input(choice)
    ch = input(choice)
    return ch

def get_alpha(prompt="Enter string: ", minl=1, maxl=20):
    while True:
        s = input(prompt)
        m = s
        s = s.replace(" ","")
        if s.isalpha() and len(s)>=minl :
            return m[:maxl].upper()
        else:
            print("\nPlease type only alphabats (a-z/A-Z) only...Plese try again...!!!")

def get_int(prompt="Enter a number: ", start=-100000 , end=100000):
    while True:
        s = input(prompt).strip()
        t = s[0]
        if t=="-":
            s=s[1:]
        if s.isdigit():
            s = "-"+s if t=="-" else s
            s = int(s)
            if s>=start and s<=end:
                return s
            else:
                print("\nPlease enter value in range({}...{})".format(start, end))
        else:
            print("\nPlease type digits(0-9) only...Plese try again...!!!")

def get_date(prompt="Date(yyyy-mm-dd): "):
    while True:
        s = input(prompt).strip()
        if s[4] in "-:/" and s[7] in "-:/":
            y = s[:4]
            m = s[5:7]
            d = s[8:]
            if y.isdigit() and m.isdigit() and d.isdigit():
                y = int(y)
                m = int(m)
                d = int(d)
                if m==2 :
                    if (y%100==0 and y%400==0) or (y%100!=0 and y%4==0):
                        if d>=1 and d<=29:
                            return s
                        else:
                            print("\nPlease enter a valid date format(yyyy-mm-dd)....Try again...!!!")
                    else:
                        if d>=1 and d<=28:
                            return s
                        else:
                            print("\nPlease enter a valid date format(yyyy-mm-dd)....Try again...!!!")
                elif m in [4,6,9,11]:
                    if d>=1 and d<=30:
                        return s
                    else:
                        print("\nPlease enter a valid date format(yyyy-mm-dd)....Try again...!!!")
                elif m in [1,3,5,7,8,10,12]:
                    if d>=1 and d<=31:
                        return s
                    else:
                        print("\nPlease enter a valid date format(yyyy-mm-dd)....Try again...!!!")
                else:
                    print("\nPlease enter a valid date format(yyyy-mm-dd)....Try again...!!!")
            else:
                print("\nPlease enter a valid date format(yyyy-mm-dd)....Try again...!!!")
        else:
            print("\nPlease enter a valid date format(yyyy-mm-dd)....Try again...!!!")
def byebye():
    print("=====================================================")
    print("This program is developed by:-")
    print("                              H.K. BHABHIWAL")
    print("                              PGT (COMPUTER SCIENCE)")
    print("                              K.V. NO.1, NEEMUCH")
    print("                              hiteshsir@hotmail.com")
    print("Happy to see you again")
    print("=====================================================")

def convert_data_in_list(data):
    if len(data)>0:
        nof = len(data[0])
        ls = []
        for i in range(nof):
            ls.append([])
        for row in data:
            for x,i  in zip(row, range(nof)):
                ls[i].append(x)
        return ls
    else:
        return False

if __name__ =="__main__":
    
    sql = "select * from stu"
    data = get_result(sql)
    convert_data_in_list(data)