import mysql.connector
from mysql.connector import errorcode
from collections import defaultdict
# from datetime import datetime

class getUser():
    def __init__(self):
        config = {
            "user": 'jinchen',
            "password": '19841036',
            "host": '127.0.0.1',
            "database": 'Whiteboard'
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

        qry = "SELECT ID, userType, firstName, lastName FROM Users WHERE userName = %s AND password= %s ;"
        self.cursor.execute(qry,(username,password))

        for (ID, userType,firstName, lastName) in self.cursor:
            # print("ID = {:d}, userType={:d}".format(ID, userType))
            return {"ID":ID, "userType":userType, "firstName":firstName,"lastName":lastName }

        return -1

    def get_CourseInfo(self,userID):

        self.cursor.execute("SELECT userType FROM Users WHERE ID = %s;" %userID)
        for (userType) in self.cursor:
            uType = userType[0]

        if uType == 1:       #Professor
            qry = "SELECT coursesID, courseName,semester,year FROM Courses " \
                  "WHERE professorID = %(userID)s ORDER BY year ASC,semester DESC;"
            self.cursor.execute(qry,{"userID":userID})

            courseInfo = defaultdict(list)
            for (courseID, courseName,semester,year) in self.cursor:
                courseInfo['courseName'].append(courseName)
                courseInfo['semester'].append(semester)
                courseInfo['year'].append(year)
                courseInfo['courseID'].append(courseID)

            if not courseInfo:
                return -1
            return courseInfo

        else:               # Student
            qry = "SELECT courseID,courseName, semester,year, firstName,lastName,email " \
                  "FROM (Users JOIN Courses ON Users.ID = Courses.professorID) NATURAL JOIN TakenClasses " \
                  "WHERE studentID = %(userID)s ORDER BY year ASC,semester DESC;"
            self.cursor.execute(qry,{"userID":userID})

            courseInfo = defaultdict(list)
            for (courseID,courseName, semester,year, firstName,lastName,email) in self.cursor:
                courseInfo['courseID'].append(courseID)
                courseInfo['courseName'].append(courseName)
                courseInfo['semester'].append(semester)
                courseInfo['year'].append(year)
                courseInfo['professorName'].append(firstName +" "+lastName)
                courseInfo['professorEmail'].append(email)

            if not courseInfo:
                return -2
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
        qry ="SELECT assignID, deadline,task,gradeTotal,timestamp FROM Assignment WHERE coursesID = %(courseID)s ORDER BY timestamp ASC;"
        self.cursor.execute(qry, {"courseID": courseID})

        assignmentInfo = defaultdict(list)
        for (assignID,deadline,task,gradeTotal,timestamp) in self.cursor:
            assignmentInfo['assignID'].append(assignID)
            assignmentInfo['deadline'].append(deadline.strftime("%m/%d/%Y, %H:%M:%S"))
            assignmentInfo['task'].append(task)
            assignmentInfo['gradeTotal'].append(gradeTotal)
            assignmentInfo['postTime'].append(timestamp.strftime("%m/%d/%Y, %H:%M:%S"))
        if not assignmentInfo:
            return -1
        return assignmentInfo

    # get_grades
    def get_grades(self,userID, courseID):
        self.cursor.execute("SELECT userType FROM Users WHERE ID = %s;" %userID)
        for (userType) in self.cursor:
            uType = userType[0]

        if uType == 1:       #Professor
            qry = "SELECT TakenClasses.studentID, TakenClasses.grade, Users.firstName,Users.lastName,Courses.courseName " \
                  "FROM Courses NATURAL JOIN TakenClasses " \
                  "JOIN Users ON TakenClasses.studentID = Users.ID " \
                  "WHERE coursesID = %s AND professorID = %s ORDER BY Users.lastName ASC;"
            self.cursor.execute(qry, (courseID,userID))

            gradeInfo = defaultdict(list)
            for (studentID,grade,firstName, lastName,courseName) in self.cursor:
                gradeInfo['studentID'].append(studentID)
                gradeInfo['grade'].append(grade)
                gradeInfo['studentFirstName'].append(firstName)
                gradeInfo['studentLastName'].append(lastName)
                gradeInfo['courseName'].append(courseName)

            if not gradeInfo:
                return -1

        else:                #Student
            qry = "SELECT Courses.courseName, Courses.professorID, TakenClasses.grade, Users.firstName,Users.lastName " \
                  "FROM TakenClasses NATURAL JOIN Courses " \
                  "JOIN Users ON Courses.professorID = Users.ID " \
                  "WHERE coursesID = %s AND studentID = %s ORDER BY Users.lastName ASC;"
            self.cursor.execute(qry, (courseID,userID))


            gradeInfo = defaultdict(list)
            for (courseName,professorID,grade,firstName, lastName) in self.cursor:
                gradeInfo['courseName'].append(courseName)
                gradeInfo['professorID'].append(professorID)
                gradeInfo['finalgrade'].append(grade)
                gradeInfo['professorFirstName'].append(firstName)
                gradeInfo['professorLastName'].append(lastName)
            if not gradeInfo:
                return -2
        return gradeInfo

    def get_submission(self,assignID):
        qry = "SELECT studentID, file, timestamp, Users.firstName,Users.lastName  " \
              "FROM AssignmentSubmission JOIN Users ON AssignmentSubmission.studentID = Users.ID " \
              "WHERE AssignmentSubmission.assignID = %(assignID)s;"
        self.cursor.execute(qry,{"assignID": assignID})

        submissionInfo = defaultdict(list)
        for (studentID, file, timestamp, firstName,lastName) in self.cursor:
            submissionInfo['studentID'].append(studentID)
            submissionInfo['file'].append(file)
            submissionInfo['submitTime'].append(timestamp.strftime("%m/%d/%Y, %H:%M:%S"))
            submissionInfo['studentFirstName'].append(firstName)
            submissionInfo['studentLastName'].append(lastName)
        if not submissionInfo:
            return -1
        return submissionInfo