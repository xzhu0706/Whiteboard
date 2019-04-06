
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
    qry = ("SELECT studentID,courseID,estFinalGrade FROM TakenClasses;")
    cursor.execute(qry)
    print("*" * 80)
    for (studentID,courseID,grade) in cursor:
        print(f"{courseID} : {studentID}, {grade}")
    print("*" * 80)

def query_assignment(cursor):
    qry = ("SELECT assignmentID, courseID, deadline, postTime FROM Assignment;")
    cursor.execute(qry)
    print("*" * 80)
    for (assignmentID, courseID, deadline, postTime) in cursor:
        print(f"{assignmentID} : {courseID}, {deadline},   {postTime}")
    print("*" * 80)

def query_assignmentSubmission(cursor):
    qry = ("SELECT submissionID, studentID, assignmentID, uploadTime FROM AssignmentSubmission;")
    cursor.execute(qry)
    print("*" * 80)
    for (submissionID, studentID, assignmentID, uploadTime) in cursor:
        print(f"{submissionID} : {studentID}, {assignmentID}, {uploadTime}")
    print("*" * 80)

def query_exam(cursor):
    qry = ("SELECT examID, courseID, gradeTotal, description, postTime FROM Exam;")
    cursor.execute(qry)
    print("*" * 80)
    for (examID, courseID, gradeTotal, description, examDay) in cursor:
        print(f"{examID} : {courseID}, {gradeTotal},  {description}, {examDay}")
    print("*" * 80)





# def query_examGrade(cursor):
#     qry = ("SELECT gradeID,studentID, submissionID, examID, grade, gradeTime FROM GradeBook;")
#     cursor.execute(qry)
#     print("*" * 80)
#     for (gradeID,studentID, submissionID, examID, grade, gradeTime) in cursor:
#         print(f"{gradeID} : {studentID}, {examID}, {submissionID}, {grade},{gradeTime}")
#     print("*" * 80)
    # GradeBook(studentID, courseID, submissionID, description, grade)

def query_classAnnouncement(cursor):
    qry = ("SELECT announcementID,courseID,announcement, postTime FROM ClassAnnouncement;")
    cursor.execute(qry)
    print("*" * 80)
    for (announcementID,courseID,announcement, postTime) in cursor:
        print(f"{announcementID} : {courseID},  {announcement}, {postTime}")
    print("*" * 80)


def query_classMaterials(cursor):
    qry = ("SELECT materialID,courseID,material, postTime FROM ClassMaterial;")
    cursor.execute(qry)
    print("*" * 80)
    for (materialID,courseID,material, postTime) in cursor:
        print(f"{materialID} : {courseID},  {material}, {postTime}")
    print("*" * 80)
