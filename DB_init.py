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


    def login_check(self, username, password):
        return DB_Get.login_check(self.cursor,username, password)

    def get_Courses(self, userID):
        return DB_Get.get_Courses(self.cursor,userID)

    def get_courseInfo(self, courseID):
        return DB_Get.get_Courses(self.cursor,courseID)

    def get_Materials(self, courseID):
        return DB_Get.get_Materials(self.cursor,courseID)

    def get_Announcement(self, courseID):
        return DB_Get.get_Announcement(self.cursor, courseID)

    def get_Assignments(self, courseID, ID):
        return DB_Get.get_Assignments(self.cursor, courseID,ID)

    def get_Submission(self,assignID):
        return DB_Get.get_submission(self.cursor,assignID)



    # Update DB
    def update(self,result):
        if result:
            self.cnx.commit()
        return result

    def uploadMaterial(self,courseID,material):
        result = DB_Post.uploadMaterial(self.cursor,courseID,material)
        return self.update(result)

    def del_Material(self, materialID):
        result = DB_Post.del_Material(self.cursor,materialID)
        return self.update(result)


    def makeAnnouncement(self,courseID,announcement):
        result = DB_Post.makeAnnouncement(self.cursor, courseID,announcement)
        return self.update(result)

    def del_Announcement(self, announcementID):
        result = DB_Post.del_Announcement(self.cursor, announcementID)
        return self.update(result)

    def createAssignment(self,courseID,deadline,title, task,gradeTotal):
        result = DB_Post.createAssignment(self.cursor, courseID,deadline,title,task,gradeTotal)
        return self.update(result)

    def del_Assignment(self, assignID):
        result = DB_Post.del_Assignment(self.cursor, assignID)
        return self.update(result)


    def submit_Assignment(self,assignID,studentID,content):
        result = DB_Post.submit_Assignment(self.cursor,assignID,studentID,content)
        return self.update(result)

    def submit_Grade(self,submissionID, grade):
        result = DB_Post.submit_grade(self.cursor, submissionID, grade)
        return self.update(result)