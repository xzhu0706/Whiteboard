import mysql.connector
from mysql.connector import errorcode
import DB_Get
import DB_Post

class db_User():
    def __init__(self, config):
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


    # Get info from DB
    def login_check(self, username, password):
        return DB_Get.login_check(self.cursor,username, password)

    def get_Courses(self, userID):
        return DB_Get.get_Courses(self.cursor,userID)

    def get_courseInfo(self, courseID):
        return DB_Get.get_courseInfo(self.cursor,courseID)

    def get_Materials(self, courseID):
        return DB_Get.get_Materials(self.cursor,courseID)

    def get_Announcement(self, courseID):
        return DB_Get.get_Announcement(self.cursor, courseID)

    def get_Assignments(self, courseID, ID):
        return DB_Get.get_Assignments(self.cursor, courseID,ID)

    def get_Submission(self,assignmentID):
        return DB_Get.get_submission(self.cursor,assignmentID)

    def get_Grades(self, courseID,userID):
        return DB_Get.get_grades(self.cursor, self.cnx, courseID,userID)





    # Update DB
    def update(self,result):
        if result:
            self.cnx.commit()
        return result

    # Create
    def uploadMaterial(self,courseID,material):
        result = DB_Post.uploadMaterial(self.cursor,courseID,material)
        return self.update(result)

    def makeAnnouncement(self,courseID,announcement):
        result = DB_Post.makeAnnouncement(self.cursor, courseID,announcement)
        return self.update(result)

    def createAssignment(self,courseID,deadline,title, task,gradeTotal):
        result = DB_Post.createAssignment(self.cursor, courseID,deadline,title,task,gradeTotal)
        return self.update(result)


    def create_Exam(self, courseID, description, gradeTotal,examPercentage):
        result = DB_Post.createExam(self.cursor, courseID, description,gradeTotal,examPercentage)
        return self.update(result)

    # Submit Grade or Assignment
    def submit_Assignment(self,assignmentID,studentID,content):
        result = DB_Post.submit_Assignment(self.cursor,assignmentID,studentID,content)
        return self.update(result)

    def submit_AssignmentGrade(self,assignmentID, studentID, assignmentGrade):
        result = DB_Post.submit_AssignmentGrade(self.cursor,self.cnx, assignmentID, studentID, assignmentGrade)
        return self.update(result)

    def submit_SubmissionGrade(self, submissionID, assignmentGrade):
        result = DB_Post.submit_SubmissionGrade(self.cursor,self.cnx, submissionID, assignmentGrade)
        return self.update(result)

    def submit_ExamGrade(self,studentID, examID, examGrade):
        result = DB_Post.submit_ExamGrade(self.cursor, self.cnx, studentID, examID, examGrade)
        return self.update(result)

    # Delete
    def del_Material(self, materialID):
        result = DB_Post.del_Material(self.cursor,materialID)
        return self.update(result)

    def del_Announcement(self, announcementID):
        result = DB_Post.del_Announcement(self.cursor, announcementID)
        return self.update(result)

    def del_Assignment(self, assignmentID):
        result = DB_Post.del_Assignment(self.cursor, assignmentID)
        return self.update(result)

    def del_Exam(self, examID):
        result = DB_Post.del_Exam(self.cursor, examID)


