from project_module import *
from matplotlib.pyplot import *

def add_student():
    rollno = get_int("Enter roll number: ", 11100, 12499)
    name = get_alpha("Name of Student: ", 1, 20)
    mobno = get_int("Mobile number: ",5555555555,9999999999 )
    while True:
        stream = get_alpha("Stream (B/M/C/H): ", 1,1)
        if stream in "BMCH":
            break
        else:
            print("\nPlease enter any one character from (B/M/C/H) only...Try again...!!!")
    std = get_int("Class (11/12): ",11,12)
    status = save_record("stu",[rollno,name,mobno,stream,std])
    if status == True:
        print("\nSaved successfully.")
    else:
        print("\nSomething wrong...!!!")
        
      
def add_exam():
    exam_name = input("Exam Name: ").strip().upper()[:40]
    exam_code = input("Exam code (short name of above exam): ").strip().upper()[:20]
    max_marks = get_int("Maxmimum Marks: ", 5,100)
    min_marks = get_int("Minimum Marks to pass: ", 5, 100)
    doe = get_date("Date of Exam (yyyy-mm-dd): ")
    status = save_record("exam", [exam_code, exam_name, max_marks, min_marks, doe])
    if status == True:
        print("\nSaved successfully.")
    else:
        print("\nSomething wrong...!!!")

def add_marks_classwise():
    std = get_int("Enter class(11/12): ", 11, 12)
    ls_exam_code = []
    ls_exam_name = []
    ls_max_marks = []
    sql_query = "select exam_name, exam_code, max_marks from exam"
    conn = myconnector.connect(host=host_name, user=user_name, passwd = password, database=database_name)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        i= 1
        for row in data:
            ls_exam_name.append(row[0])
            ls_exam_code.append(row[1])
            ls_max_marks.append(row[2])
            print(i, row[1], "(",row[0],")")
            i += 1
        print("-"*64)
        exam_index = get_int("Select Exam ({} to {})".format(1, i-1), 1, i-1)
        exam_index -= 1
        
        #sql_query = "select rollno, name from stu where std = {} order by rollno".format(std)
        sql_query = "select * from stu left join marks on stu.rollno = marks.rollno where std={} and exam_code IS NULL".format(std)
        sql_query = "select * from stu left join (select * from marks where exam_code='{}') as marks on stu.rollno = marks.rollno where std={} and exam_code IS NULL".format(ls_exam_code[exam_index], std)
        cursor.execute(sql_query)
        data = cursor.fetchall()
        print('='*70)
        print("Note:- (1) Input -1 (minus one) for Absent")
        print("       (2) Press 'Enter Key' to input marks for next student, otherwise 'q' to quit")
        print("       (3) MAXIMUM MARKS: {}".format(ls_max_marks[exam_index]))
        print('='*70)
        
        i = 0
        ls_rollno = []
        ls_marks = []
        for row in data:
            prompt = "Enter marks for Roll No. {} ({}) : ".format(row[0], row[1])
            
            obt_marks = get_int(prompt, -1, ls_max_marks[exam_index])
            ls_rollno.append(row[0])
            ls_marks.append(obt_marks)
            i += 1
            next_record = input("Press ENTER KEy for continue 'q' for quit")
            if len(next_record)>0 and next_record in "qQ":
                break
        for j in range(i):
            save_record("marks", [ls_rollno[j], ls_exam_code[exam_index],ls_marks[j]] )
            
def show_markslips():
    std = get_int("Enter class(11/12): ", 11, 12)
    ls_exam_code = []
    ls_exam_name = []
    ls_max_marks = []
    sql_query = "select exam_name, exam_code, max_marks from exam"
    conn = myconnector.connect(host=host_name, user=user_name, passwd = password, database=database_name)
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        i= 1
        for row in data:
            ls_exam_name.append(row[0])
            ls_exam_code.append(row[1])
            ls_max_marks.append(row[2])
            print(i, row[1], "(",row[0],")")
            i += 1
        print("-"*64)
        exam_index = get_int("Select Exam ({} to {})".format(1, i-1), 1, i-1)
        exam_index -= 1
        
        #sql_query = "select rollno, name from stu where std = {} order by rollno".format(std)
        #sql_query = "select * from stu left join marks on stu.rollno = marks.rollno where std={} and exam_code IS NULL".format(std)
        sql_query = "select  stu.rollno, name, replace(obt_marks,-1, 'AB') from stu left join (select * from marks where exam_code='{}') as marks on stu.rollno = marks.rollno where std={} ".format(ls_exam_code[exam_index], std)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        data = cursor.fetchall()
        print("Exam Name: ",ls_exam_name[exam_index])
        print("Max Marks: ",ls_max_marks[exam_index])
        
        show_result_in_table(sql_query, width=[10,25,5], header=["Roll No.","Student's Name","Marks"])
        ch = input("Show Grpah(y/n):")
        if ch in "yY":
            ls = convert_data_in_list (data)
            name = array(ls[1])
            marks = ls[2]
            marks_arr = array(marks)
            for i in range(len(marks)):
                if marks[i].isdigit():
                    marks[i]=int(marks[i])
                else:
                    marks[i]=0
            
            ch = input("for Bar(press 'b') or Line (press 'l'): " )
            if ch in "bB":
                clf()
                title(ls_exam_name[exam_index])
                bar(ls[1], ls[2])
                show()
            elif ch in "lL":   
                clf()
                title(ls_exam_name[exam_index])
                plot(ls[1], ls[2])
                show()
def progress_report():
    rollno = get_int("Enter roll number: ",11100,12999)
    sql_query = "select stu.*, round(obt_marks/max_marks*100,2) as per, exam_name from stu, marks, exam where stu.rollno=marks.rollno and marks.exam_code = exam.exam_code and stu.rollno={}".format(rollno)
    data = get_result(sql_query)
    if len(data)>0:
        ls = convert_data_in_list(data)
        name = ls[1]
        name = name[0]
        mobno = ls[2]
        mobno = mobno[0]
        stream = ls[3]
        stream = stream[0]
        std = ls[4]
        std = std[0]
        marks = ls[5]
        exam_name = ls[6]
        for i in range(len(marks)):
            num = float(marks[i])
            if num>=0:
                marks[i]=num
            else:
                marks[i]=0
        s = "Roll number: {}\nName: {}\nMobile No.: {}\nClass and Stream: {}, {}".format(rollno, name, mobno, std, stream)
        '''
        sql_query = "select replace(replace(obt_marks,-1, 0)/max_marks*100,0,'AB') as per, exam_name from stu, marks, exam where stu.rollno=marks.rollno and marks.exam_code = exam.exam_code and stu.rollno={}".format(rollno)
        print(sql_query)
        print(s)
        show_result_in_table(sql_query)
        '''
        ch = input("for Bar(press 'b') or Line (press 'l'): " )
        if ch in "bB":
            clf()
            title(s)
            bar(exam_name, marks)   
            show()
        elif ch in "lL":    
            clf()
            title(s)
            plot(exam_name, marks)
            show()
    else:
        print("\nRoll number is not found...!!!")
            
'''
print("welcome")
settings(hname="localhost",uname="root", pwd="1234", db = "ipmarks")       
print(database_name)'''
#add_exam6()
#add_student()
#add_marks_classwise()

if __name__ == '__main__':
    progress_report()
    
    