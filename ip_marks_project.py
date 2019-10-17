#from project_module import *
from ip_marks_module import *
import sys
"""
First create following tables in IPMARKS database

create database ipmarks;

use ipmarks;

create table stu
(rollno int primary key,
name varchar(20) not null,
mobno varchar(10),
stream char(1),
std int);

create table exam(
exam_code varchar(20) primary key,
exam_name varchar(40),
max_marks int not null,
min_marks int,
doe date);

create table marks(
rollno int,
exam_code varchar(10),
obt_marks varchar(3),
foreign key(rollno) references stu(rollno) on delete cascade on update cascade,
foreign key(exam_code) references exam(exam_code) on delete cascade on update cascade);
"""

settings(hname="localhost",uname="root", pwd="1234", db = "ipmarks")    

ls1 = ["WELCOME TO IP MARKS MANAGEMENT", "ADD NEW STUDENT","FEED MARKS", "REPORTS", "EXAMINATION SETTINGS","QUIT"]   
ls2 = ["VARIOUS REPORTS", "Show Marks Slip", "Show Progress Report of particular student","Back","Quit"]

flag = ""
while True:
    ch = show_menu(ls1[0], ls1[1:])
    if ch=="1":
        add_student()
    elif ch=="2":
        add_marks_classwise()
    elif ch=="4":
        add_exam()
    elif ch=="3":
        while True:
            ch = show_menu(ls2[0], ls2[1:])
            if ch=="1": #show marks slip
                show_markslips()
            elif ch=="2": #shoe progress report a student
                progress_report()
            elif ch=="3":
                break
            elif ch=="4":
                byebye()
                sys.exit()
            else:
                print("\nWroing choice...Try agian...!!!")
        if ch==3:
            break
    elif ch=="5":
        byebye()
        break
    else:
        print("\nWroing choice...Try agian...!!!")
        
    

 
 

 