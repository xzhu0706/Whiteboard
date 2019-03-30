import mysql.connector
from mysql.connector import errorcode
from collections import defaultdict
# from datetime import datetime

class User():
    def __init__(self):
        config = {
            "user": ' ',# your mysql username
            "password": '', # your mysql password
            "host": '127.0.0.1',
            "database": 'Whiteboard2'   # your database name
        }
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


    def login_check(self,username,password):

        qry = "SELECT ID, userType FROM Users WHERE userName = %s AND password= %s ;"
        self.cursor.execute(qry,(username,password))

        for (ID, userType) in self.cursor:
            # print("ID = {:d}, userType={:d}".format(ID, userType))
            return {"ID":ID, "userType":userType}

        return -1

    def get_CourseInfo(self,userID):

        # qry = "SELECT * FROM ((TakenClasses NATURAL JOIN Courses ) WHERE studentID = %s ORDER BY year ASC,semester DESC)NATURAL JOIN User ON professorID = User.ID;"
        qry = "SELECT courseName, semester,year, firstName,lastName,email " \
              "FROM (Users JOIN Courses ON Users.ID = Courses.professorID) NATURAL JOIN TakenClasses " \
              "WHERE studentID = %(userID)s ORDER BY year ASC,semester DESC;"
        self.cursor.execute(qry,{"userID":userID})

        courseInfo = defaultdict(list)
        for (courseName, semester,year, firstName,lastName,email) in self.cursor:
            courseInfo['courseName'].append(courseName)
            courseInfo['semester'].append(semester)
            courseInfo['year'].append(year)
            courseInfo['professorName'].append(firstName +" "+lastName)
            courseInfo['professorEmail'].append(email)

        if not courseInfo:
            return -1
        return courseInfo


    def get_Materials(self,courseID):
        qry ="SELECT material,timestamp FROM ClassMaterials WHERE coursesID = %(courseID)s ORDER BY timestamp ASC;"
        self.cursor.execute(qry, {"courseID": courseID})

        materialInfo = defaultdict(list)
        for (material,timestamp) in self.cursor:
            materialInfo['material'].append(material)
            materialInfo['time'].append(timestamp.strftime("%m/%d/%Y, %H:%M:%S"))
        if not materialInfo:
            return -1
        return materialInfo

    def get_Assignments(self,courseID):
        qry ="SELECT deadline,task,gradeTotal,timestamp FROM Assignment WHERE coursesID = %(courseID)s ORDER BY timestamp ASC;"
        self.cursor.execute(qry, {"courseID": courseID})

        assignmentInfo = defaultdict(list)
        for (deadline,task,gradeTotal,timestamp) in self.cursor:
            assignmentInfo['deadline'].append(deadline.strftime("%m/%d/%Y, %H:%M:%S"))
            assignmentInfo['task'].append(task)
            assignmentInfo['gradeTotal'].append(gradeTotal)
            assignmentInfo['postTime'].append(timestamp.strftime("%m/%d/%Y, %H:%M:%S"))
        if not assignmentInfo:
            return -1
        return assignmentInfo

    def get_grades(self,userID, courseID):
        qry = "SELECT userType FROM Users WHERE ID = %(userID)s;"
        self.cursor.execute(qry,{"userID":userID});

        userType = 3;

