import mysql.connector
from mysql.connector import errorcode
from collections import defaultdict
# from datetime import datetime

class postUser():
    def __init__(self,config):

        try:
            self.cnx = mysql.connector.connect(**config)
            self.cursor = self.cnx.cursor(buffered=True)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            raise err

    def uploadMaterial(self,courseID,material):
        qry = "INSERT INTO ClassMaterials (courseID,material) VALUES (%s,%s);"
        try:
            self.cursor.execute(qry, (courseID,material))
            self.cnx.commit()  # Make sure data is committed to the database
            return True
        except mysql.connector.Error as err:
            print(err)
            return False


    def makeAnnouncement(self,courseID,announcement):
        qry = "INSERT INTO ClassAnnouncement (courseID,announcement) VALUES (%s,%s);"
        try:
            self.cursor.execute(qry, (courseID,announcement))
            self.cnx.commit()  # Make sure data is committed to the database
            return True
        except mysql.connector.Error as err:
            return False

    def createAssignment(self,courseID,deadline,task,gradeTotal):
        qry = "INSERT INTO Assignment (courseID,deadline,task,gradeTotal) " \
              "VALUES (%s,%s,%s,%s);"
        try:
            self.cursor.execute(qry, (courseID,deadline,task,gradeTotal))
            self.cnx.commit()  # Make sure data is committed to the database
            return True
        except mysql.connector.Error:
            return False



################################
    # Below still need modify

    def create_Submission(self,studentID,assignID,file):
        isGraded = 0
        qry = "INSERT INTO AssignmentSubmission(studentID,assignID,isGraded,file) VALUES (%s,%s,%s,%s);"
        try:
            self.cursor.execute(qry, (studentID,assignID,isGraded,file))
            self.cnx.commit()  # Make sure data is committed to the database
            return "Upload Submission Success"
        except mysql.connector.Error as err:
            return "Upload Submission Failed"





    def assign_grade(self,studentID,submissionID,courseID,grade,description):


        try:
            if submissionID == 0:
                qry = "INSERT INTO GradeBook(studentID, assignID,description,grade) VALUES (%s,%s,%s,%s);"
                self.cursor.execute(qry, (studentID, courseID, description, grade))
            else:
                qry = "INSERT INTO GradeBook(studentID,submissionID, assignID,description,grade) VALUES (%s,%s,%s,%s,%s);"
                self.cursor.execute(qry, (studentID,courseID, submissionID,description,grade))

                qry = "UPDATE AssignmentSubmission SET isGraded = 1 WHERE submissionID = %(submissionID)s;"
                self.cursor.execute(qry,{'submissionID':submissionID})


            qry = "SELECT SUM(gradeTotal), SUM(grade) " \
                  "FROM AssignmentSubmission JOIN Assignment " \
                  "ON Assignment.AssignID = AssignmentSubmission.assignID AND coursesID = %s " \
                  "JOIN GradeBook ON GradeBook.submissionID = AssignmentSubmission.submissionID " \
                  "AND GradeBook.studentID = %s"
            # Get Assignment Grade
            self.cursor.execute(qry, (courseID,studentID))
            for (gradeTotal, grade) in self.cursor:
                totalGrade = gradeTotal
                currentGrade = grade

            self.cursor.execute("SELECT grade FROM AssignmentSubmission WHERE submissionID is NULL;")
            for (grade) in self.cursor:
                totalGrade += 100
                currentGrade += grade


            finalgrade = currentGrade/totalGrade * 100
            qry = "INSERT INTO TakenClasses (studentID,courseID,grade) VALUES (%s,%s,%s)" \
                  "ON DUPLICATE KEY UPDATE grade = %s "
            self.cursor.execute(qry, (studentID,courseID, finalgrade,finalgrade))

            self.cnx.commit()            # Make sure data is committed to the database
            return "Update Grade Success"
        except mysql.connector.Error as err:
            return "Update Grade Failed"


        #Update to final grade
