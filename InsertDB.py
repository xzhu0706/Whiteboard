import random
import datetime
import string
import mysql.connector
import numpy as np

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
        email = "@".join((username, "ccny.cuny.edu"))

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
        assignmentPercentage = 30
        qry = "INSERT INTO Courses (courseName, semester, year, professorID,assignmentPercentage) VALUE (%s,%s,%s,%s,%s);"

        try:
            cursor.execute(qry, (courseName, semester, year, professorID,assignmentPercentage))
        except mysql.connector.Error:
            i -= 1
            check += 1
        if check >= 10:
            print("Create %d Users" % i)
            break


def create_random_takenClasses(cursor):
    cursor.execute("SELECT ID, userType FROM Users;")
    studentIDs = []
    for (ID, userType) in cursor:
        if userType ==0:
            studentIDs.append(ID)


    cursor.execute("SELECT courseID FROM Courses;")
    courseIDs = []
    for courseID in cursor:
        courseIDs.append(courseID[0])

    studentNum = 10
    if len(studentIDs) < 10:
        studentNum = len(studentIDs)

    estFinalGrade = None
    qry = "INSERT INTO TakenClasses (studentID, courseID, estFinalGrade) VALUE (%s,%s,%s);"
    index = list(range(len(studentIDs)))
    for course in courseIDs:
        np.random.shuffle(index)
        try:
            for i in range(studentNum):
                # print("course %d, i %d"%(course, i))
                # print(index[i])
                student = studentIDs[index[i]]
                cursor.execute(qry, (student, course, estFinalGrade))
        except mysql.connector.Error:
            print("Error Create Class" )
            break



def create_random_assignment(cursor):
    qry = ("SELECT courseID FROM Courses;")
    cursor.execute(qry)
    courseIDs = []
    for courseID in cursor:
        courseIDs.append(courseID[0])

    task = 'task description'
    gradeTotal = 100
    qry = "INSERT INTO Assignment (courseID, deadline, title, task, gradeTotal,postTime) VALUE (%s,%s,%s,%s,%s,%s);"
    for course in courseIDs:
        try:
            postTime = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=random.randint(4, 10)),
                                                 datetime.time(random.randint(0, 23), random.randint(0, 59),
                                                               random.randint(0, 59)))
            for i in range(3):
                deadline = datetime.datetime.combine(postTime + datetime.timedelta(days=random.randint(10, 20)), datetime.time.max)
                title="Assignment "+str(i+1)
                cursor.execute(qry, (course, deadline, title, task, gradeTotal,postTime))
                postTime = datetime.datetime.combine(postTime + datetime.timedelta(days=random.randint(2, 6)),
                                                  datetime.time(random.randint(0, 23), random.randint(0, 59),
                                                                random.randint(0, 59)))
        except mysql.connector.Error:
            break



def create_random_AssignmentGrade(cursor):
    cursor.execute("SELECT assignmentID, studentID FROM TakenClasses NATURAL JOIN Assignment;")
    assignmentIDs, studentIDs = [], []
    for (assignmentID, studentID) in cursor:
        assignmentIDs.append(assignmentID)
        studentIDs.append(studentID)

    qry = "UPDATE AssignmentGrade SET assignmentGrade = %s WHERE assignmentID = %s AND studentID = %s;"

    try:
        for i in range(len(studentIDs)):
            # assignmentGrade = None
            if random.uniform(0, 1) < 0.3:
                studentID = studentIDs[i]
                assignmentID = assignmentIDs[i]
                assignmentGrade = random.randint(60, 100)
                cursor.execute(qry,(assignmentGrade,assignmentID,studentID))
    except mysql.connector.Error:
        print ("Error: create_random_AssignmentGrade")



def create_random_assignmentSubmission(cursor):
    cursor.execute("SELECT studentID,assignmentID FROM AssignmentGrade WHERE assignmentGrade is not NULL;")

    assignmentIDs, studentIDs = [], []
    for (studentID,assignmentID) in cursor:
        assignmentIDs.append(assignmentID)
        studentIDs.append(studentID)
    try:
        qry = "INSERT INTO AssignmentSubmission(assignmentID,studentID,file) VALUES (%s,%s,%s);"
        for i in range(len(studentIDs)):
            studentID = studentIDs[i]
            assignmentID = assignmentIDs[i]
            # print("studentID %d, assignmentID %d" %(studentID,assignmentID))
            file = "File: " + ''.join((random.choices(string.ascii_lowercase + string.digits, k=10)))
            cursor.execute(qry, (assignmentID,studentID, file))

    except mysql.connector.Error as err:
        print("Error: create_random_assignmentSubmission")
        print(err)

    # ### Not graded submission
    cursor.execute("SELECT studentID,assignmentID FROM AssignmentGrade WHERE assignmentGrade is NULL;")

    assignmentIDs, studentIDs = [], []
    for (studentID,assignmentID) in cursor:
        assignmentIDs.append(assignmentID)
        studentIDs.append(studentID)

    subNum = 10
    if len(studentIDs) < 10:
        subNum = len(studentIDs)
    try:
        qry = "INSERT INTO AssignmentSubmission(assignmentID,studentID,file) VALUES (%s,%s,%s);"
        for i in range(subNum):
            studentID = studentIDs[i]
            assignmentID = assignmentIDs[i]
            file = "File: " + ''.join((random.choices(string.ascii_lowercase + string.digits, k=10)))
            cursor.execute(qry, (assignmentID, studentID, file))

    except mysql.connector.Error:
        print("Error: create_random_assignmentSubmission")



def create_random_exam(cursor):
    cursor.execute("SELECT courseID FROM Courses;")
    courseIDs = []
    for courseID in cursor:
        courseIDs.append(courseID[0])

    gradeTotal = 100
    qry = "INSERT INTO Exam(courseID, gradeTotal, description, examPercentage) VALUES (%s,%s,%s,%s);"
    # Exam(examID, courseID, gradeTotal, description, examPercentage, postTime)
    try:
        for course in courseIDs:
            for i in range(random.randint(1,3)):
                description = "Exam"+str(i+1)
                examPercentage = random.randint(10,30)
                cursor.execute(qry, (course, gradeTotal, description,examPercentage))
    except mysql.connector.Error:
        print("Error: create_random_exam")

def create_random_ExamGrade(cursor):
    examName = "Exam1"
    cursor.execute("SELECT examID, studentID FROM TakenClasses NATURAL JOIN Exam")
    examIDs, studentIDs = [], []
    for (examID, studentID) in cursor:
        examIDs.append(examID)
        studentIDs.append(studentID)


    qry = "INSERT INTO ExamGrade(examID, studentID, examGrade) VALUE (%s, %s, %s);"

    try:
        for i in range(random.randint(5,len(studentIDs))):
            studentID = studentIDs[i]
            examID = examIDs[i]
            examGrade = random.randint(60, 100)
            cursor.execute(qry,(examID,studentID,examGrade))
    except mysql.connector.Error:
        print ("Error: create_random_AssignmentGrade")



def create_random_classAnnouncement(cursor):
    cursor.execute("SELECT courseID FROM Courses;")
    courseIDs = []
    for courseID in cursor:
        courseIDs.append(courseID[0])

    try:
        for courseID in courseIDs:
            qry = "INSERT INTO ClassAnnouncement (courseID,announcement) VALUES (%s,%s);"
            for i in range(random.randint(1,4)):
                announcement = "announcement "+str(i+1)
                cursor.execute(qry, (courseID,announcement))
    except mysql.connector.Error as err:
        print ("Error: create_random_classAnnouncement")
        print(err)


def create_random_classMaterials(cursor):
    cursor.execute("SELECT courseID FROM Courses;")
    courseIDs = []
    for courseID in cursor:
        courseIDs.append(courseID[0])

    try:
        for courseID in courseIDs:
            qry = "INSERT INTO ClassMaterial (courseID,material)  VALUES (%s,%s);"
            for i in range(random.randint(1,4)):
                material = "material "+str(i+1)
                cursor.execute(qry, (courseID,material))
    except mysql.connector.Error as err:
        print ("Error: create_random_classMaterials")
        print(err)


