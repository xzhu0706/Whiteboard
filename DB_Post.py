import mysql.connector


# ########## Create

def uploadMaterial(cursor, courseID,material):
    qry = "INSERT INTO ClassMaterial (courseID,material) VALUES (%s,%s);"
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

        assignmentID = 0

        cursor.execute("SELECT max(assignmentID) FROM Whiteboard2.Assignment;")
        for (assignmentID) in cursor:
            assignmentID = assignmentID[0]

        cursor.execute("SELECT studentID FROM TakenClasses WHERE courseID = %s" % courseID)
        studentIDs = []
        for (studentID) in cursor:
            studentIDs.append(studentID[0])

        qry = "INSERT INTO AssignmentGrade(assignmentID,studentID) VALUE (%s,%s);"
        for studentID in studentIDs:
            cursor.execute(qry, (assignmentID,studentID))
        return True
    except mysql.connector.Error as err:
        print("Error in createAssignment")
        print(err)
        return False

def createExam(cursor, courseID, description,gradeTotal,examPercentage):
    try:
        qry = "INSERT INTO Exam(courseID,gradeTotal,description,examPercentage) VALUES (%s,%s,%s,%s);"
        cursor.execute(qry, (courseID, gradeTotal, description,examPercentage))
        return True
    except mysql.connector.Error as err:
        print("Error in createExam")
        print(err)
        return False

# Submit Grade or Assignment
def submit_Assignment(cursor,assignmentID,studentID,content):
    qry = "INSERT INTO AssignmentSubmission(studentID,assignmentID,file) VALUES (%s,%s,%s);"
    try:
        cursor.execute(qry, (studentID,assignmentID,content))
        return True
    except mysql.connector.Error:
        return False

def submit_AssignmentGrade(cursor,cnx, assignmentID, studentID, assignmentGrade):
    try:
        qry = "INSERT INTO AssignmentGrade(assignmentID,studentID, assignmentGrade) VALUE (%s,%s,%s)" \
              "ON DUPLICATE KEY UPDATE AssignmentGrade = %s;"
        cursor.execute(qry, (assignmentID, studentID, assignmentGrade, assignmentGrade))

        cursor.execute("SELECT courseID FROM Assignment "
                       "WHERE assignmentID = %s;" % assignmentID)
        for(courseID) in cursor:
            cID = courseID[0]

        finalGrade = update_finalgrade(cursor,cnx,cID,studentID)
        if finalGrade == False:
            return False
        return True
    except mysql.connector.Error as err:
        print("Error in submit_AssignmentGrade")
        print(err)
        return False

def submit_SubmissionGrade(cursor, cnx, submissionID, assignmentGrade):
    try:
        cursor.execute("SELECT studentID, assignmentID FROM AssignmentSubmission "
                       "WHERE submissionID = %s;" % submissionID)

        for (studentID,assignmentID) in cursor:
            sID = studentID
            aID = assignmentID
        qry = "INSERT INTO AssignmentGrade(assignmentID,studentID, assignmentGrade) VALUES (%s,%s,%s) " \
              "ON DUPLICATE KEY UPDATE assignmentGrade = %s;"
        cursor.execute(qry, (aID, sID, assignmentGrade,assignmentGrade))


        cursor.execute("SELECT courseID FROM Assignment "
                       "WHERE assignmentID = %s;" % aID)
        for(courseID) in cursor:
            cID = courseID[0]

        finalGrade = update_finalgrade(cursor,cnx,cID,sID)
        if finalGrade == False:
            return False
        return True
    except mysql.connector.Error as err:
        print("Error in submit_SubmissionGrade")
        print(err)
        return False

def submit_ExamGrade(cursor,cnx, studentID, examID, examGrade):
    qry = "INSERT INTO ExamGrade(examID, studentID, examGrade) VALUES (%s,%s,%s) " \
          "ON DUPLICATE KEY UPDATE examGrade = %s;"
    try:
        cursor.execute(qry, (examID, studentID, examGrade,examGrade))

        cursor.execute("SELECT courseID FROM Exam "
                       "WHERE examID = %s;" % examID)
        for (courseID) in cursor:
            cID = courseID[0]

        finalGrade = update_finalgrade(cursor,cnx, cID, studentID)
        if finalGrade == False:
            return False
        return True
    except mysql.connector.Error as err:
        print("Error in submit_ExamGrade")
        print(err)
        return False


def update_finalgrade(cursor,cnx, courseID, studentID):
    # Get assignment grade
    cursor.execute("SELECT assignmentGrade,gradeTotal "
                   "FROM AssignmentGrade LEFT JOIN Assignment "
                   "ON  AssignmentGrade.assignmentID = Assignment.assignmentID "
                   "WHERE courseID = %s AND studentID = %s ;" %(courseID,studentID))
    totalAssignmentGrade,assignmentPercentage = 0,30
    i = 0
    for (assignmentGrade, gradeTotal) in cursor:
        if assignmentGrade is not None:
            totalAssignmentGrade += assignmentGrade/gradeTotal
            i+=1

    if i != 0:
        totalAssignmentGrade /= i
    cursor.execute("SELECT assignmentPercentage FROM Courses WHERE courseID = %s;" %courseID)
    for (assignmentPercentage) in cursor:
        assignmentPercentage = assignmentPercentage[0]

    #  Get exam grade
    cursor.execute("SELECT examGrade,gradeTotal,examPercentage "
                   "FROM  TakenClasses LEFT JOIN Exam "
                   "ON TakenClasses.courseID = Exam.courseID "
                   "LEFT JOIN ExamGrade ON Exam.examID = ExamGrade.examID "
                   "AND ExamGrade.studentID = TakenClasses.studentID "
                   "WHERE TakenClasses.courseID = %s "
                   "AND TakenClasses.studentID = %s;" %(courseID,studentID))

    totalExamGrade, totalExamPercentages = 0,0
    for (examGrade,gradeTotal,examPercentage) in cursor:
        if examGrade is not None:
            totalExamGrade += examGrade/gradeTotal *examPercentage
            totalExamPercentages += examPercentage

    if totalAssignmentGrade == 0 and totalExamGrade == 0:
        return None
    elif totalAssignmentGrade == 0:
        estFinalGrade = totalExamGrade/totalExamPercentages *100
    elif totalExamGrade == 0:
        estFinalGrade = totalAssignmentGrade *100
    else:
        estFinalGrade = (totalExamGrade+totalAssignmentGrade*assignmentPercentage)/(assignmentPercentage+totalExamPercentages)*100

    try:
        cursor.execute("UPDATE TakenClasses SET estFinalGrade = %s "
                       "WHERE studentID = %s AND courseID =%s;"%(estFinalGrade,studentID,courseID))
        cnx.commit()
        return estFinalGrade
    except mysql.connector.Error as err:
        print("Error in update_finalgrade")
        print(err)
        return False



# Delete
def del_Material(cursor,materialID):
    try:
        cursor.execute("DELETE FROM ClassMaterial where materialID = %s;"% materialID)
        return True
    except mysql.connector.Error:
        return False

def del_Announcement(cursor,announcementID):
    try:
        cursor.execute("DELETE FROM ClassAnnouncement where announcementID = %s;"% announcementID)
        return True
    except mysql.connector.Error:
        return False

def del_Assignment(cursor,assignmentID):
    try:
        cursor.execute("DELETE FROM Assignment where assignmentID = %s;"% assignmentID)
        return True
    except mysql.connector.Error:
        return False

def del_Exam(cursor, examID):
    try:
        cursor.execute("DELETE FROM Exam where examID = %s;" % examID)
        return True
    except mysql.connector.Error:
        return False
