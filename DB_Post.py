import mysql.connector


# ########## Create

def uploadMaterial(cursor, courseID,material):
    qry = "INSERT INTO ClassMaterials (courseID,material) VALUES (%s,%s);"
    try:
        cursor.execute(qry, (courseID,material))
        return True
    except mysql.connector.Error :
        # print(err)
        return False


def makeAnnouncement(cursor,courseID,announcement):
    qry = "INSERT INTO ClassAnnouncement (courseID,announcement) VALUES (%s,%s);"
    try:
        cursor.execute(qry, (courseID,announcement))
        return True
    except mysql.connector.Error:
        return False

def createAssignment(cursor,courseID,deadline,title,task,gradeTotal):
    qry = "INSERT INTO Assignment (courseID,deadline,title, task,gradeTotal) " \
          "VALUE (%s,%s,%s,%s,%s);"
    try:
        cursor.execute(qry, (courseID,deadline,title,task,gradeTotal))
        return True
    except mysql.connector.Error:
        return False

def createExam(cursor, courseID, description,gradeTotal):

    try:
        qry = "INSERT INTO Exam(courseID,gradeTotal,description) VALUES (%s,%s,%s);"
        cursor.execute(qry, (courseID, gradeTotal, description))
        return True
    except mysql.connector.Error:
        return False

# Submit Grade or Assignment
def submit_Assignment(cursor,assignID,studentID,content):
    qry = "INSERT INTO AssignmentSubmission(studentID,assignID,file) VALUES (%s,%s,%s);"

    try:
        cursor.execute(qry, (studentID,assignID,content))
        return True
    except mysql.connector.Error:
        return False

def submit_grade(cursor, submissionID, grade):
    try:
        cursor.execute("SELECT studentID, gradeTotal FROM AssignmentSubmission "
                       "NATURAL JOIN Assignment WHERE submissionID = %s;" % submissionID)

        for (studentID,gradeTotal) in cursor:
            sID = studentID
            gradeT = gradeTotal
        gradePercent = float(grade)/gradeT *100
        # qry = "INSERT INTO GradeBook(studentID, submissionID,grade) VALUES (%s,%s,%s);"
        qry = "INSERT INTO GradeBook(studentID, submissionID,grade) VALUES (%s,%s,%s) " \
              "ON DUPLICATE KEY UPDATE GradeBook.grade = %s;"
        cursor.execute(qry, (sID, submissionID, gradePercent,gradePercent))
        return True
    except mysql.connector.Error:
        return False

def submit_Examgrade(cursor, studentID, examID, grade):
    cursor.execute("SELECT gradeTotal FROM Exam WHERE examID = %s;" % examID)
    for (gradeTotal) in cursor:
        gradeT = gradeTotal[0]
    gradePercent = float(grade) / gradeT * 100

    qry = "INSERT INTO GradeBook(studentID, examID,grade) VALUES (%s,%s,%s) " \
          "ON DUPLICATE KEY UPDATE GradeBook.grade = %s;"
    try:
        cursor.execute(qry, (studentID, examID, gradePercent,gradePercent))
        return True
    except mysql.connector.Error:
        return False


def update_grade(cursor, courseID, userID):

    cursor.execute("SELECT userType FROM Users WHERE ID = %s;" % userID)
    for (userType) in cursor:
        uType = userType[0]

    sIDs =[]
    if uType == 1:  # Student
        cursor.execute("SELECT studentID From TakenClasses WHERE courseID = %s;" %courseID)
        for (studentID) in cursor:
            sIDs.append(studentID[0])

    elif uType == 0:
        sIDs.append(userID[0])

    try:
        for studentID in sIDs:
            cursor.execute("SELECT count(*),SUM(GradeBook.grade) FROM TakenClasses "
                           "JOIN GradeBook ON TakenClasses.studentID = GradeBook.StudentID "
                           "WHERE courseID = %s AND TakenClasses.studentID = %s "
                           "AND submissionID is NOT NULL;" % (courseID, studentID))
            assignmentGrade, examGrade = -1, -1
            for (count, sumGrade) in cursor:
                assignmentGrade = sumGrade / count

            cursor.execute("SELECT count(*),SUM(GradeBook.grade) FROM TakenClasses "
                           "JOIN GradeBook ON TakenClasses.studentID = GradeBook.StudentID "
                           "WHERE courseID = %s AND TakenClasses.studentID = %s "
                           "AND examID is NOT NULL;" % (courseID, studentID))

            for (count, sumGrade) in cursor:
                if sumGrade == None:
                    examGrade = -1
                else:
                    examGrade = sumGrade / count

            if examGrade == -1 and assignmentGrade == -1:
                finalGrade = None
            else:
                if assignmentGrade == -1:
                    assignmentGrade = examGrade
                elif examGrade == -1:
                    examGrade = assignmentGrade
                finalGrade = assignmentGrade * 0.5 + examGrade * 0.5

            cursor.execute("INSERT INTO TakenClasses (studentID, courseID, grade) VALUE (%s,%s,%s)"
                           "ON DUPLICATE KEY UPDATE grade = %s;" % (studentID, courseID, finalGrade, finalGrade))
        return True
    except mysql.connector.Error:
        return False



# #################### Delete
def del_Material(cursor,materialID):
    try:
        cursor.execute("DELETE FROM ClassMaterials where materialID = %s;"% materialID)
        return True
    except mysql.connector.Error:
        return False

def del_Announcement(cursor,announcementID):
    try:
        cursor.execute("DELETE FROM ClassAnnouncement where announcementID = %s;"% announcementID)
        return True
    except mysql.connector.Error:
        return False

def del_Assignment(cursor,assignID):
    try:
        cursor.execute("DELETE FROM Assignment where assignID = %s;"% assignID)
        return True
    except mysql.connector.Error:
        return False



################################
# Below still need modify

# def create_Submission(,studentID,assignID,file):
#     isGraded = 0
#     qry = "INSERT INTO AssignmentSubmission(studentID,assignID,isGraded,file) VALUES (%s,%s,%s,%s);"
#     try:
#         .cursor.execute(qry, (studentID,assignID,isGraded,file))
#         .cnx.commit()  # Make sure data is committed to the database
#         return "Upload Submission Success"
#     except mysql.connector.Error as err:
#         return "Upload Submission Failed"





# def assign_grade(,studentID,submissionID,courseID,grade,description):
#
#
#     try:
#         if submissionID == 0:
#             qry = "INSERT INTO GradeBook(studentID, assignID,description,grade) VALUES (%s,%s,%s,%s);"
#             .cursor.execute(qry, (studentID, courseID, description, grade))
#         else:
#             qry = "INSERT INTO GradeBook(studentID,submissionID, assignID,description,grade) VALUES (%s,%s,%s,%s,%s);"
#             .cursor.execute(qry, (studentID,courseID, submissionID,description,grade))
#
#             qry = "UPDATE AssignmentSubmission SET isGraded = 1 WHERE submissionID = %(submissionID)s;"
#             .cursor.execute(qry,{'submissionID':submissionID})
#
#
#         qry = "SELECT SUM(gradeTotal), SUM(grade) " \
#               "FROM AssignmentSubmission JOIN Assignment " \
#               "ON Assignment.AssignID = AssignmentSubmission.assignID AND coursesID = %s " \
#               "JOIN GradeBook ON GradeBook.submissionID = AssignmentSubmission.submissionID " \
#               "AND GradeBook.studentID = %s"
#         # Get Assignment Grade
#         .cursor.execute(qry, (courseID,studentID))
#         for (gradeTotal, grade) in .cursor:
#             totalGrade = gradeTotal
#             currentGrade = grade
#
#         cursor.execute("SELECT grade FROM AssignmentSubmission WHERE submissionID is NULL;")
#         for (grade) in .cursor:
#             totalGrade += 100
#             currentGrade += grade
#
#
#         finalgrade = currentGrade/totalGrade * 100
#         qry = "INSERT INTO TakenClasses (studentID,courseID,grade) VALUES (%s,%s,%s)" \
#               "ON DUPLICATE KEY UPDATE grade = %s "
#         .cursor.execute(qry, (studentID,courseID, finalgrade,finalgrade))
#
#         .cnx.commit()            # Make sure data is committed to the database
#         return "Update Grade Success"
#     except mysql.connector.Error as err:
#         return "Update Grade Failed"
#

    #Update to final grade
