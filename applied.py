import sqlite3
import traceback
import sys
#setting up the database connection and cursor 
con = sqlite3.connect('assignment3.db')
cur = con.cursor()

#check login func, returns empty array if invalid login info, else returns name and surname
def check_login(type, uname, pword):
    con = sqlite3.connect('assignment3.db')
    cur = con.cursor()
    try:
        type = type.upper()
        ans = "[]"
        cur.execute("Select name,surname FROM {} WHERE email =? AND password =?".format(type) , (str(uname), str(pword),))
        ans = cur.fetchall()
        return ans
    except (sqlite3.Error) as er:
        return []


#calls check login func, if its return array is empty, the login info was invalid
def req_login():
    try:
        succ = False
        type, username, password = input("Enter your user type, username, then your password separated by a space. ").split()
        c = check_login(type, username, password)
        if (c != []):
            print("Logged In Successfully")
            succ = True
            return type, username, succ
        else:
            print("Invalid login info, please try again")
            return False
    except (ValueError) as er:
        print("Invalid login info, please try again")
        return False

#print all courses in DB
def course_list():
    con = sqlite3.connect('assignment3.db')
    cur = con.cursor()  
    cur.execute("Select * FROM Courses")
    ans = cur.fetchall()
    for i in ans:
        print(i)
    return (ans)
    
#search courses by 4 letter department
def search_course():
    con = sqlite3.connect('assignment3.db')
    cur = con.cursor()
    dept = input("Enter the course department: ").upper()
    cur.execute("Select * FROM Courses WHERE department =?", (str(dept),))
    ans = cur.fetchall()
    if (ans == []):
        print("No valid courses")
    for i in ans:
        print(i)
    return (ans)
#admin only create user func
def create_user():
    con = sqlite3.connect('assignment3.db')
    cur = con.cursor()
    type = input("Enter new user type: ").lower()
    match type:
        case "admin":
            try: 
                id, name, surname = input("Enter the admins id number, first name and last name: ").split()
                title = input("Enter their title: ")
                office = input("Enter their office: ")
                email = surname + name[0]
                password = 1234

                cur.execute("Insert INTO ADMIN values (?,?,?,?,?,?,?)", (int(id), str(name), str(surname), str(title), str(office),str(email), str(password),))
            except (sqlite3.Error, ValueError) as er:
                print("Invalid input, please try again")
                return False
        case "student":
            try:
                id, name, surname = input("Enter the students id number, first name and last name: ").split()
                grad = input("Enter their expected gradyear: ")
                major = input("Enter their major: ").upper()
                email = surname + name[0]
                password = 1234

                cur.execute("Insert INTO STUDENT values (?,?,?,?,?,?,?,?)", (int(id), str(name), str(surname), int(grad), str(major), str(email), str(password),  "",))

            except (sqlite3.Error, ValueError) as er:
                print("Invalid input, please try again")
                return False 
        case "instructor":
            try:
                id, name, surname = input("Enter the instructors id number, first name and last name: ").split()
                title = input("Enter their title: ")
                hyear = input("Enter their year of hire: ")
                dept = input("Enter their department: ").upper()
                email = surname + name[0]
                password =1234
                cur.execute("Insert INTO Instructor values (?,?,?,?,?,?,?,?,?)", (int(id), str(name), str(surname), str(title), int(hyear), str(dept), str(email), str(password), "",))
            except (sqlite3.Error, ValueError) as er:
                print("Invalid input, please try again")
                return False
        case _:
            print("Invalid input, please try again")
            return False
    print("User created successfully")
    con.commit()
    return True
#admin only remove user func
def remove_user():
    con = sqlite3.connect('assignment3.db')
    cur = con.cursor()
    type = input("Enter user type to be removed: ").lower()
    id = input("Enter their id number: ")
    try:
        match type:
            case "admin":
                cur.execute("DELETE FROM ADMIN WHERE id =?", (int(id),))
            case "student":
                cur.execute("DELETE FROM student WHERE id =?", (int(id),))
            case "instructor":
                cur.execute("DELETE FROM instructor WHERE id =?", (int(id),))
        con.commit()
        print("User removed from system")
        return True
    except sqlite3.Error as er:
        "Invalid input, please try again"
        return False
    
#add course to system
def add_course():
    try:
        con = sqlite3.connect('assignment3.db')
        cur = con.cursor()
        cnum = input("Enter the new courses course number: ")
        title = input("Enter the course title: ")
        dept = input("Enter the department abbreviation: ").upper()
        time = input("Enter the courses time: ")
        days = input("Enter the courses days: ")
        days = days.upper()
        sem, year = input("Enter the courses semester and year: ").split()
        sem[0].capitalize
        creds = input("Enter the courses number of credits: ")
        csize = input("Enter the courses size: ")
        cur.execute("INSERT INTO Courses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (int(cnum), str(title), str(dept), str(time), str(days), str(sem), int(year), int(creds), "null", int(csize), "", 0, ))
        print("Course added to system")
        con.commit()
        return True
    except (sqlite3.Error, ValueError) as er:
        print("Invalid input, please try again")
        return False
#remove course from system
def remove_course():
    try:
        con = sqlite3.connect('assignment3.db')
        cur = con.cursor()
        cnum = input("Enter the course number you wish to remove: ")
        cur.execute("DELETE FROM courses WHERE course_number =?", (int(cnum),))
        print("Course removed from system")
        con.commit()
        return True
    except (sqlite3.Error) as er:
        print("Invalid input, please try again")
        return False     
#print a course roster
def croster():
    try:
        con = sqlite3.connect('assignment3.db')
        cur = con.cursor()
        idnumber = input("Enter the courses id number: ")
        cur.execute("SELECT students FROM courses WHERE course_number =?", (int(idnumber),))
        out = cur.fetchall()
        print(out)
        return out
    except sqlite3.error as er:
        print("Invalid input, please try again")
        return False  
#add student to a class via get and check design, increment class count
def add_student():
    try:
        con = sqlite3.connect('assignment3.db')
        cur = con.cursor()
        cid = input("Enter the courses id number: ")
        cur.execute("SELECT csize FROM courses WHERE course_number =?", (int(cid),))
        s = cur.fetchone()
        size = s[0]
        
        cur.execute("SELECT num_students FROM courses WHERE course_number =?", (int(cid),))
        n = cur.fetchone()
        numstud = n[0]
        
        cur.execute("SELECT students FROM courses WHERE course_number =?", (int(cid),))
        o = cur.fetchall()
        out = str(o[0])
        osize = len(out)
        out = out[0:osize-2]
        disall = "[]()'"
        for character in disall:
            out = str(out).replace(character,"")
        
        if (numstud < size):
            
            sid = input("Enter the students id number: ")
            cur.execute("SELECT EXISTS(SELECT 1 FROM student WHERE id =?)", (int(sid),))
            b = cur.fetchone()
            boo = b[0]
            ccc = (sid not in out)
            if (boo & ccc):
                if (numstud == 0):
                    cur.execute("UPDATE courses set num_students = 1, students =? WHERE course_number =?", (str(sid) + ', ',int(cid),))
                    print("Student added to class")
                    
                else:
                    numstud +=1
                    cur.execute("UPDATE courses set students =?, num_students =? WHERE course_number =?", (str(out + sid) + ', ', int(numstud), int(cid),))
                    print("Student added to class")
                cur.execute("SELECT schedule FROM student WHERE id =?", (int(sid),))
                o = cur.fetchall()
                out = str(o[0])
                print(out)
                osize = len(out)
                out = out[0:osize-2]
                disall = "[]()'"
                for character in disall:
                    out = str(out).replace(character,"")
                print(out)
                print(out+cid + ", ")
                cur.execute("UPDATE student SET schedule =? WHERE id =?", (str(out+cid) + ", ", int(sid),))
                con.commit()

            else:
                print("Student is already in this class")
                return False
            return str(out+cid) + ", "

        else:
            print("Class is full!")
            return False
    except (sqlite3.Error, ValueError) as er:
        print("Invalid input, please try again")
        return False  
#remove student and decrement class count
def remove_student():
    try:
        con = sqlite3.connect('assignment3.db')
        cur = con.cursor()
        cid = input("Enter the courses id number: ")
        cur.execute("SELECT num_students FROM courses WHERE course_number =?", (int(cid),))
        s = cur.fetchone()
        size = s[0]
        if (size == 0):
            print("Class is empty!!")
            return False
        else:
            sid = input("Enter the student id number: ")
            checkid = sid +", "
            cur.execute("SELECT students FROM courses WHERE course_number =?", (int(cid),))
            o = cur.fetchall()
            out = str(o[0])
            osize = len(out)
            out = out[0:osize-2]
            disall = "[]()'"
            for character in disall:
                out = str(out).replace(character,"")
            cur.execute("SELECT students FROM courses WHERE course_number =?", (int(cid),))
            s = cur.fetchall()
            sout = str(s[0])
            disall = "[]()'"
            for character in disall:
                sout = str(sout).replace(character,"")
            if (checkid in out):
                out = out.replace(checkid , "")
                size -= 1
                cur.execute("UPDATE courses set students =?, num_students =? WHERE course_number =?", (str(out), int(size), int(cid),))
        
                cur.execute("SELECT schedule FROM student WHERE id =?", (int(sid),))
                st = cur.fetchall()
                stout = str(st[0])
                stsize = len(stout)
                stout = stout[0:stsize-2]
                print(stout)
                disall = "[]()'"
                for character in disall:
                    stout = str(stout).replace(character,"")
                remcid = str(cid) + ", "
                print(stout)
                print(remcid)
                stout = stout.replace(remcid , "")
                print(stout)
                cur.execute("UPDATE student set schedule =? where ID = ?", (str(stout), int(sid),))
                print("Student has been removed")
                con.commit()
                return True
            else:
                print("Invalid id number, student is not in the class")
                return False
    except (sqlite3.Error, ValueError) as er:
        print("Invalid input, please try again")
        return False  
#search all professors for valid dept
def find_prof():
    try:
        con = sqlite3.connect('assignment3.db')
        cur = con.cursor()
        a = []
        dept = input("Enter the courses 4 letter department abbreviation: ").upper()
        cur.execute("Select name, surname, id FROM instructor WHERE dept =?", (str(dept),))
        a = cur.fetchall()
        
        if (a == []):
            print("No valid instructors")
            return False
        else:
            for i in a:
                print(i)
            return a
    except (sqlite3.Error, ValueError) as er:
        print("Invalid input, please try again")
        return False  
#add prof to a course via id number, must also add course to instructor sched
def add_prof():
    try:
        con = sqlite3.connect('assignment3.db')
        cur = con.cursor()
        cid = input("Enter the course number: ")
        pid = input("Enter the instructors id number: ")
        #getting professors name cleanly
        cur.execute("Select name, surname FROM instructor WHERE id =?", (int(pid),))
        pn = cur.fetchall()
        profname = pn
        disall = "[](),'"
        for character in disall:
            profname = str(profname).replace(character,"")
        
        #setting instructor
        cur.execute("UPDATE courses SET instructor =? WHERE course_number =?", (profname, int(cid),))
        
        #setting professor schedule
        cur.execute("SELECT schedule FROM instructor WHERE id =?", (int(pid),))
        o = cur.fetchall()
        out = str(o[0])
        osize = len(out)
        out = out[0:osize-2]
        disall = "[]()'"
        for character in disall:
            out = str(out).replace(character,"")
        cur.execute("UPDATE instructor SET schedule =? WHERE id =?", (str(out+cid), int(pid)))
        con.commit()
        return True
    except (sqlite3.Error, ValueError) as er:
        print("Invalid input, please try again")
        return False


succ = False
while(not succ):
    utype, name, succ = req_login()
print()
cont = True
while(cont):
    match utype:
        case "admin":
            print("Search Courses (csearch) Print a list of all courses (clist) \nPrint Course Roster (roster) \nAdd a student to a course (add) \nRemove a student from a course (remove)")
            print("Create a new user (create) \nRemove a user from the database (deluse)")
            print("Find a professor to teach a course by department (findp) Link a professor to a course (linkp) ")
            print("Create a new course (newc) \nRemove a course from the database (remc) \nLogout (exit)")
            next = input("Enter your desired action by typing the text in parentheses from above: ")
            aval = ["csearch", "clist", "roster", "add", "remove", "create", "deluse", "findp", "linkp" "newc", "remc", "exit"]
            if (next not in aval):
                next = "null"
        case "student":
            print("Search courses (csearch)  Print a list of all classes (clist) \nAdd a class to your schedule (add) Remove a class from your schedule (remove) \nLogout (exit)")
            next = input("Enter your desired action by typing the text in parentheses from above ")
            aval = ["csearch", 'clist', "add", "remove", "exit"]
            if (next not in aval):
                next = "null"
        case "instructor":
            print("Search coureses (csearch) \n Print a class roster (roster) Logout(exit)")
            next = input("Enter your desired action by typing the text in parentheses from above ")
            aval = ["csearch", 'roster', "exit"]
            if (next not in aval):
                next = "null"

    match(next):
        case "csearch":
            search_course()
        case "clist":
            course_list()
        case "roster":
            croster()
        case "add":
            add_student()
        case "remove":
            remove_student()
        case "create":
             create_user()
        case "deluse":
            remove_user()
        case "findp":
            find_prof()
        case "linkp":
            add_prof()
        case "newc":
            add_course()
        case "remc":
            remove_course()
        case "exit":
            cont = False
        case "null":
            print("Invalid input, please try again")
            cont = True
    print()
#saving changes
con.commit()
con.close()
