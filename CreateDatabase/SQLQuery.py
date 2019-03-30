
def query_users(cursor):
    qry = ("SELECT ID, userName, password,email FROM Users;")
    cursor.execute(qry)
    print("*" * 80)
    for (ID, userName, password,email) in cursor:
        print(f"{ID} : {userName}, {password},{email}")
    print("*" * 80)

def query_courses(cursor):
    qry = ("SELECT coursesID, courseName, semester,year,professorID FROM Courses;")
    cursor.execute(qry)
    print("*" * 80)
    for (coursesID, courseName, semester,year,professorID) in cursor:
        print(f"{coursesID} : {courseName}, {semester},{year},{professorID}")
    print("*" * 80)


def query_takenClasses(cursor):
    qry = ("SELECT studentID,coursesID,grade FROM TakenClasses;")
    cursor.execute(qry)
    print("*" * 80)
    for (studentID,coursesID,grade) in cursor:
        print(f"{coursesID} : {studentID}, {grade}")
    print("*" * 80)

def query_assignment(cursor):
    qry = ("SELECT assignID, coursesID, deadline, timestamp FROM Assignment;")
    cursor.execute(qry)
    print("*" * 80)
    for (assignID, coursesID, deadline, timestamp) in cursor:
        print(f"{assignID} : {coursesID}, {deadline},   {timestamp}")
    print("*" * 80)

def query_assignmentSubmission(cursor):
    qry = ("SELECT submissionID, studentID, assignID, isGraded, timestamp FROM AssignmentSubmission;")
    cursor.execute(qry)
    print("*" * 80)
    for (submissionID, studentID, assignID, isGraded, timestamp) in cursor:
        print(f"{submissionID} : {studentID}, {assignID},  {isGraded}, {timestamp}")
    print("*" * 80)

def query_gradeBook(cursor):
    qry = ("SELECT gradeID,studentID, coursesID, submissionID, description, grade, timestamp FROM GradeBook;")
    cursor.execute(qry)
    print("*" * 80)
    for (gradeID,studentID, coursesID, submissionID, description, grade, timestamp) in cursor:
        print(f"{gradeID} : {studentID}, {coursesID},  {submissionID}, {description}, {grade},{timestamp}")
    print("*" * 80)
    # GradeBook(studentID, coursesID, submissionID, description, grade)

def query_classAnnouncement(cursor):
    qry = ("SELECT announcementID,coursesID,announcement, timestamp FROM ClassAnnouncement;")
    cursor.execute(qry)
    print("*" * 80)
    for (announcementID,coursesID,announcement, timestamp) in cursor:
        print(f"{announcementID} : {coursesID},  {announcement}, {timestamp}")
    print("*" * 80)


def query_classMaterials(cursor):
    qry = ("SELECT materialID,coursesID,material, timestamp FROM ClassMaterials;")
    cursor.execute(qry)
    print("*" * 80)
    for (materialID,coursesID,material, timestamp) in cursor:
        print(f"{materialID} : {coursesID},  {material}, {timestamp}")
    print("*" * 80)
