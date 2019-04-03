import random
import datetime
import string
import mysql.connector


def random_users():
    last = ("Aaren","Aarika","Oliver","Jacob","William","Sophia","Emma","Isabella")
    first = ("Allan", "Selina", "Hebe", "Ella", "Ada", "Frances", "Barbara","Abigail")


    firstName =random.choice(first)
    lastName =random.choice(last)
    username = firstName+''.join(random.choices(string.digits,k=3))
    password = ''.join((random.choices(string.ascii_lowercase+string.digits,k=10)))

    if random.uniform(0,1) < 0.9:
        userType = 0
        email = "@".join((username, "citymail.cuny.edu"))
    else:
        userType = 1
        email = "@".join((username, "cuny.ccny.edu"))

    return username, password,email,firstName,lastName,userType

def create_random_users(cursor,num):
    check = 0
    for i in range(num):
        username, password, email, firstName, lastName, userType = random_users()
        qry = "INSERT INTO Users (userName, password,email,firstName,lastName,userType) VALUES (%s,%s,%s,%s,%s,%s);"
        try:
            cursor.execute(qry, (username, password,email,firstName,lastName,userType))
        except mysql.connector.Error as err:
            i -= 1
            check += 1
        if check >= 10:
            print("Create %d Users" % i)
            break

def create_random_courses(cursor,num):
    qry = ("SELECT ID, userType FROM Users;")
    cursor.execute(qry)
    professorIDs = []
    for (ID, userType) in cursor:
        if userType ==1:
            professorIDs.append(ID)

    semesters = ("Spring", "Fall")
    check = 0
    for i in range(num):
        courseName = "CSc" + ''.join((random.choices(string.digits, k=3)))
        semester = random.choice(semesters)
        year = random.randint(2015,2019)
        professorID = random.choice(professorIDs)
        qry = "INSERT INTO Courses (courseName, semester, year, professorID) VALUES (%s,%s,%s,%s);"

        try:
            cursor.execute(qry, (courseName, semester, year, professorID))
        except mysql.connector.Error as err:
            i -= 1
            check += 1
        if check >= 10:
            print("Create %d Users" % i)
            break



def create_random_takenClasses(cursor,num):
    qry = ("SELECT ID, userType FROM Users;")
    cursor.execute(qry)
    studentIDs = []
    for (ID, userType) in cursor:
        if userType ==0:
            studentIDs.append(ID)

    qry = ("SELECT courseID FROM Courses;")
    cursor.execute(qry)
    courseIDs = []
    for courseID in cursor:
        courseIDs.append(courseID[0])

    check = 0
    for i in range(num):
        studentID = random.choice(studentIDs)
        courseID = random.choice(courseIDs)
        grade = random.randint(50, 100)
        qry = "INSERT INTO TakenClasses (studentID,courseID,grade) VALUES (%s,%s,%s);"

        try:
            cursor.execute(qry, (studentID, courseID, grade))
        except mysql.connector.Error as err:
            i -= 1
            check += 1
        if check >= 10:
            print("Create %d Users" % i)
            break



def create_random_assignment(cursor,num,days):
    qry = ("SELECT courseID FROM Courses;")
    cursor.execute(qry)
    courseIDs = []
    for courseID in cursor:
        courseIDs.append(courseID[0])

    check = 0
    task = 'task'
    gradeTotal = 100
    for i in range(num):
        courseID = random.choice(courseIDs)
        deadline = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=days), datetime.time.max)
        qry = "INSERT INTO Assignment (courseID,deadline,task,gradeTotal) VALUES (%s,%s,%s,%s);"

        try:
            cursor.execute(qry, (courseID, deadline, task, gradeTotal))
        except mysql.connector.Error as err:
            i -= 1
            check += 1
        if check >= 10:
            print("Create %d Users" % i)
            break

def create_random_assignmentSubmission(cursor,num):
    qry =("SELECT studentID,assignID FROM TakenClasses NATURAL JOIN Assignment;")
    cursor.execute(qry)

    stuID =[]
    assID =[]
    for(studentID,assignID) in cursor:
        stuID.append(studentID)
        assID.append(assignID)

    check = 0
    file = "File"

    for i in range(num):

        studentID = stuID[i]
        assignID = assID[i]
        isGraded = random.randint(0, 1)
        qry = "INSERT INTO AssignmentSubmission(studentID,assignID,isGraded,file) VALUES (%s,%s,%s,%s);"

        try:
            cursor.execute(qry, (studentID, assignID, isGraded, file))
        except mysql.connector.Error as err:
            i -= 1
            check += 1

        if check >= 10:
            print("Create %d Users" % i)
            break

def create_random_exam(cursor, num):
    qry = ("SELECT courseID FROM Courses;")
    cursor.execute(qry)
    courseIDs = []
    for courseID in cursor:
        courseIDs.append(courseID[0])

    gradeTotal = 100
    des = "Exams"
    for i in range(num):
        courseID = random.choice(courseIDs)
        qry = "INSERT INTO Exam(courseID,gradeTotal,description) VALUES (%s,%s,%s);"
        cursor.execute(qry, (courseID, gradeTotal, des))


def create_random_gradeBook(cursor, num):
    cursor.execute("SELECT studentID,courseID,submissionID From "
                    "AssignmentSubmission NATURAL JOIN TakenClasses WHERE isGraded = 1;")

    subTuple = []
    for (studentID,courseID,submissionID) in cursor:
        subTuple.append((studentID,courseID,submissionID))

    cursor.execute("SELECT studentID,courseID,examID From "
                    "Exam NATURAL JOIN TakenClasses;")

    exTuple = []
    for (studentID,courseID,examID) in cursor:
        exTuple.append((studentID,courseID,examID))


    qry = "INSERT INTO GradeBook(studentID, submissionID,grade) VALUES (%s,%s,%s);"

    if num < len(subTuple):
        for i in range(num):
            studentID, courseID, submissionID = subTuple[i]
            grade = random.randint(50, 100)
            cursor.execute(qry, (studentID, submissionID,grade))
    else:
        for i in range(len(subTuple)):
            studentID, courseID, submissionID = subTuple[i]
            grade = random.randint(50, 100)
            cursor.execute(qry, (studentID, submissionID, grade))
        qry = "INSERT INTO GradeBook(studentID, examID,grade) VALUES (%s,%s,%s);"

        if num - len(subTuple) < len(exTuple):

            for i in range(num - len(subTuple)):
                studentID, courseID, examID = exTuple[i]
                grade = random.randint(50, 100)
                cursor.execute(qry, (studentID, examID, grade))
        else:
            for i in range(len(exTuple)):
                studentID, courseID, examID = exTuple[i]
                grade = random.randint(50, 100)
                cursor.execute(qry, (studentID, examID, grade))


        print("Insert %s tuple into Gradebook" % str(len(subTuple)+len(exTuple)))



def create_random_classAnnouncement(cursor,num):
    qry = ("SELECT courseID FROM Courses;")
    cursor.execute(qry)
    courseIDs = []
    for courseID in cursor:
        courseIDs.append(courseID[0])

    announcement = "announcement"
    qry = "INSERT INTO ClassAnnouncement (courseID,announcement) VALUES (%s,%s);"
    for i in range(num):
        cursor.execute(qry, (courseIDs[random.choice(range(len(courseIDs)))],announcement))


def create_random_classMaterials(cursor,num):
    qry = ("SELECT courseID FROM Courses;")
    cursor.execute(qry)
    courseIDs = []
    for courseID in cursor:
        courseIDs.append(courseID[0])

    material = "material"
    qry = "INSERT INTO ClassMaterials (courseID,material) VALUES (%s,%s);"

    for i in range(num):
        cursor.execute(qry, (courseIDs[random.choice(range(len(courseIDs)))],material))
