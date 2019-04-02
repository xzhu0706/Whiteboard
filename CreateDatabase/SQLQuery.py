
def query_users(cursor):
    qry = ("SELECT ID, userName, password,email FROM Users;")
    cursor.execute(qry)
    print("*" * 80)
    for (ID, userName, password,email) in cursor:
        print(f"{ID} : {userName}, {password},{email}")
    print("*" * 80)

def query_courses(cursor):
    qry = ("SELECT courseID, courseName, semester,year,professorID FROM Courses;")
    cursor.execute(qry)
    print("*" * 80)
    for (courseID, courseName, semester,year,professorID) in cursor:
        print(f"{courseID} : {courseName}, {semester},{year},{professorID}")
    print("*" * 80)


def query_takenClasses(cursor):
    qry = ("SELECT studentID,courseID,grade FROM TakenClasses;")
    cursor.execute(qry)
    print("*" * 80)
    for (studentID,courseID,grade) in cursor:
        print(f"{courseID} : {studentID}, {grade}")
    print("*" * 80)

def query_assignment(cursor):
    qry = ("SELECT assignID, courseID, deadline, timestamp FROM Assignment;")
    cursor.execute(qry)
    print("*" * 80)
    for (assignID, courseID, deadline, timestamp) in cursor:
        print(f"{assignID} : {courseID}, {deadline},   {timestamp}")
    print("*" * 80)

def query_assignmentSubmission(cursor):
    qry = ("SELECT submissionID, studentID, assignID, isGraded, timestamp FROM AssignmentSubmission;")
    cursor.execute(qry)
    print("*" * 80)
    for (submissionID, studentID, assignID, isGraded, timestamp) in cursor:
        print(f"{submissionID} : {studentID}, {assignID},  {isGraded}, {timestamp}")
    print("*" * 80)

def query_gradeBook(cursor):
    qry = ("SELECT gradeID,studentID, courseID, submissionID, description, grade, timestamp FROM GradeBook;")
    cursor.execute(qry)
    print("*" * 80)
    for (gradeID,studentID, courseID, submissionID, description, grade, timestamp) in cursor:
        print(f"{gradeID} : {studentID}, {courseID},  {submissionID}, {description}, {grade},{timestamp}")
    print("*" * 80)
    # GradeBook(studentID, courseID, submissionID, description, grade)

def query_classAnnouncement(cursor):
    qry = ("SELECT announcementID,courseID,announcement, timestamp FROM ClassAnnouncement;")
    cursor.execute(qry)
    print("*" * 80)
    for (announcementID,courseID,announcement, timestamp) in cursor:
        print(f"{announcementID} : {courseID},  {announcement}, {timestamp}")
    print("*" * 80)


def query_classMaterials(cursor):
    qry = ("SELECT materialID,courseID,material, timestamp FROM ClassMaterials;")
    cursor.execute(qry)
    print("*" * 80)
    for (materialID,courseID,material, timestamp) in cursor:
        print(f"{materialID} : {courseID},  {material}, {timestamp}")
    print("*" * 80)
