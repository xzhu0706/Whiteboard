import random
import datetime
import string



def random_users(num):
    last = ("Aaren","Aarika","Oliver","Jacob","William","Sophia","Emma","Isabella")
    first = ("Allan", "Selina", "Hebe", "Ella", "Ada", "Frances", "Barbara","Abigail")

    for _ in range(num):
        firstName =random.choice(first)
        lastName =random.choice(last)
        username = firstName+''.join(random.choices(string.digits,k=3))
        password = ''.join((random.choices(string.ascii_lowercase+string.digits,k=10)))
        per = random.uniform(0,1)
        if per < 0.8:
            userType = 0
            email = "@".join((username, "citymail.cuny.edu"))
        else:
            userType = 1
            email = "@".join((username, "cuny.ccny.edu"))

        yield (username, password,email,firstName,lastName,userType)

def create_random_users(cursor,num):
    for info in random_users(num):
        username, password, email, firstName, lastName, userType, *_ = info
        qry = "INSERT INTO Users (userName, password,email,firstName,lastName,userType) VALUES (%s,%s,%s,%s,%s,%s);"
        cursor.execute(qry, (username, password,email,firstName,lastName,userType))





def random_courses(num,IDs):
    semesters = ("Spring","Fall")
    for _ in range(num):
        courseName = "CSc"+''.join((random.choices(string.digits,k=3)))
        semester = random.choice(semesters)
        year = random.randint(2015,2019)
        professorID = random.choice(IDs)
        yield (courseName,semester,year,professorID)

def create_random_courses(cursor,num):
    qry = ("SELECT ID, userType FROM Users;")
    cursor.execute(qry)
    professorIDs = []
    for (ID, userType) in cursor:
        if userType ==1:
            professorIDs.append(ID)

    for info in random_courses(num,professorIDs):
        courseName, semester, year, professorID, *_ = info
        qry = "INSERT INTO Courses (courseName, semester, year, professorID) VALUES (%s,%s,%s,%s);"
        cursor.execute(qry, (courseName, semester, year, professorID))


#
# def random_takenClasses(num,sIDs,cIDs):
#
#     for i in range(num):
#         studentID = random.choice(sIDs)
#         coursesID = random.choice(cIDs)
#         grade = random.randint(50,100)
#         yield(studentID,coursesID,grade)



def create_random_takenClasses(cursor,num):
    cursor.execute("SELECT ID, userType FROM Users;")
    studentIDs = []
    for (ID, userType) in cursor:
        if userType ==0:
            studentIDs.append(ID)

    cursor.execute("SELECT coursesID FROM Courses;")
    coursesIDs = []
    for coursesID in cursor:
        coursesIDs.append(coursesID[0])

    for i in range(num):
        sID = studentIDs[i%len(studentIDs)]
        cID = coursesIDs[i//len(studentIDs)]
        grade = random.randint(50, 100)

        qry = "INSERT INTO TakenClasses (studentID,coursesID,grade) VALUES (%s,%s,%s);"
        cursor.execute(qry, (sID,cID,grade))




def random_assignment(num,cIDs,day):
    for _ in range(num):
        coursesID = random.choice(cIDs)
        deadline = datetime.datetime.now() + datetime.timedelta(days = day)
        task = 'task'
        gradeTotal = 100
        yield (coursesID,deadline,task,gradeTotal)

def create_random_assignment(cursor,num,days):
    qry = ("SELECT coursesID FROM TakenClasses;")
    cursor.execute(qry)
    coursesIDs = []
    for coursesID in cursor:
        coursesIDs.append(coursesID[0])

    for info in random_assignment(num,coursesIDs,days):
        coursesID, deadline, task, gradeTotal, *_ = info

        qry = "INSERT INTO Assignment (coursesID,deadline,task,gradeTotal) VALUES (%s,%s,%s,%s);"
        cursor.execute(qry, (coursesID,deadline,task,gradeTotal))



def create_random_assignmentSubmission(cursor,num):
    qry =("SELECT studentID,assignID FROM TakenClasses NATURAL JOIN Assignment;")
    cursor.execute(qry)

    stuID =[]
    assID =[]
    for(studentID,assignID) in cursor:
        stuID.append(studentID)
        assID.append(assignID)

    for i in range(num):
        if i > len(stuID):
            break
        studentID = stuID[i]
        assignID = assID[i]
        isGraded = random.randint(0,1)
        file = "File"
        # print(f"{studentID}: {assignID},  {isGraded}")

        qry = "INSERT INTO AssignmentSubmission(studentID,assignID,isGraded,file) VALUES (%s,%s,%s,%s);"
        cursor.execute(qry, (studentID,assignID,isGraded,file))


def create_random_gradeBook(cursor, num):
    qry = ("SELECT studentID,coursesID,submissionID From AssignmentSubmission NATURAL JOIN TakenClasses;")
    cursor.execute(qry)

    tuples = []
    for (studentID,coursesID,submissionID) in cursor:
        tuples.append((studentID,coursesID,submissionID))

    for i in range(num):
        if i >= len(tuples):
            break
        studentID, coursesID, submissionID = tuples[i]
        description =" description"
        grade = random.randint(50,100)

        qry = "INSERT INTO GradeBook(studentID,coursesID, submissionID,description,grade) VALUES (%s,%s,%s,%s,%s);"
        cursor.execute(qry, (studentID,coursesID, submissionID,description,grade))




def create_random_classAnnouncement(cursor,num):
    qry = ("SELECT coursesID FROM TakenClasses;")
    cursor.execute(qry)
    coursesIDs = []
    for coursesID in cursor:
        coursesIDs.append(coursesID[0])

    for i in range(num):
        announcement = "announcement"

        qry = "INSERT INTO ClassAnnouncement (coursesID,announcement) VALUES (%s,%s);"
        cursor.execute(qry, (coursesIDs[random.choice(range(len(coursesIDs)))],announcement))


def create_random_classMaterials(cursor,num):
    qry = ("SELECT coursesID FROM TakenClasses;")
    cursor.execute(qry)
    coursesIDs = []
    for coursesID in cursor:
        coursesIDs.append(coursesID[0])

    for i in range(num):
        material = "material"

        qry = "INSERT INTO ClassMaterials (coursesID,material) VALUES (%s,%s);"
        cursor.execute(qry, (coursesIDs[random.choice(range(len(coursesIDs)))],material))
