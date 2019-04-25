import mysql.connector
from mysql.connector import errorcode


class DB():
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
        self.cursor.callproc('getLogin',[username,password,])
        for result in self.cursor.stored_results():
            info = result.fetchall()[0]
            if info:
                return {"ID": info[0], "userType": info[1], "firstName": info[2], "lastName": info[3]}
        return -1

    def get_Courses(self, userID):
        coursesInfo = []
        self.cursor.callproc('getCourses', [userID, ])
        for result in self.cursor.stored_results():
            infos = result.fetchall()
            if infos:
                for info in infos:
                    coursesInfo.append({'courseID': info[0], 'courseName': info[1],
                                        'semester': info[2], 'year': info[3]})
                return coursesInfo
            return -1


    def get_courseInfo(self, courseID):
        self.cursor.callproc('courseInfo',[courseID,])
        for result in self.cursor.stored_results():
            info = result.fetchall()[0]
            if info:
                return {"courseID": info[1], "courseName": info[2],
                        "semester": info[3], "year": info[4],
                        "professorID": info[0], "professorName": info[5]+" "+info[6],
                        "professorEmail": info[7]}
        return -1

    def get_Materials(self, courseID):
        self.cursor.callproc('materialInfo',[courseID,])
        for result in self.cursor.stored_results():
            infos = result.fetchall()
            if infos:
                materialInfo = []
                for info in infos:
                    materialInfo.append({"materialID": info[0], "material": info[1],
                            "postTime": info[2].strftime("%m/%d/%Y, %H:%M:%S")})
                return materialInfo
        return -1

    def get_Announcement(self, courseID):
        self.cursor.callproc('announcementInfo',[courseID,])
        for result in self.cursor.stored_results():
            infos = result.fetchall()
            if infos:
                announcementInfo = []
                for info in infos:
                    announcementInfo.append({"announcementID": info[0], "announcement": info[1],
                        "postTime": info[2].strftime("%m/%d/%Y, %H:%M:%S")})
                return announcementInfo
        return -1

    def get_Assignments(self, courseID, ID):
        self.cursor.callproc('getAssignments',[courseID,ID,])
        for result in self.cursor.stored_results():
            infos = result.fetchall()
            if infos:
                assignmentInfo = []
                for info in infos:
                    dict = {'assignmentID': info[0], 'task': info[3],
                           'gradeTotal': info[4], 'title':info[2],
                           'deadline': info[1].strftime("%m/%d/%Y, %H:%M:%S"),
                           'postTime': info[5].strftime("%m/%d/%Y, %H:%M:%S"),
                           'pastDue': info[6]
                           }
                    if len(info) > 7:
                        dict['isLate'] = info[8]
                        dict['isSubmitted'] =info[8]
                    assignmentInfo.append(dict)
                return assignmentInfo
            return -1

    def get_Submission(self, assignmentID):
        self.cursor.callproc('getSubmission',[assignmentID,])
        for result in self.cursor.stored_results():
            infos = result.fetchall()
            if infos:
                submissionInfo = []
                for info in infos:
                    submissionInfo.append({'submissionID': info[1], 'studentID': info[0],
                                        'content': info[2], 'gradeTotal': info[3],
                                        'submitTime': info[4].strftime("%m/%d/%Y, %H:%M:%S"),
                                        'assignmentGrade':info[7],
                                        'studentName': info[5] + ' ' + info[6],
                                        'isSubmitted': info[9], 'isGraded': info[11],
                                        'pastDue': info[8],'isLate' : info[10]
                                        })
                return submissionInfo
            return -1
    #
    # def get_Grades(self, courseID, userID):
    #     self.cursor.callproc('getStudentInfo',[courseID,userID, ])
    #     for result in self.cursor.stored_results():
    #         info = result.fetchall()[0]
    #         if info:
    #             return {"courseID": info[1], "courseName": info[2],
    #                     "semester": info[3], "year": info[4],
    #                     "professorID": info[0], "professorName": info[5]+" "+info[6],
    #                     "professorEmail": info[7]}
    #     return -1


    def uploadMaterial(self, courseID, material):
        self.cursor.callproc('addMaterial',[courseID,material,])
        self.cnx.commit()


    def makeAnnouncement(self, courseID, announcement):
        self.cursor.callproc('addAnnouncement', [courseID, announcement, ])
        self.cnx.commit()

    def addAssignment(self, courseID, deadline, title, task, gradeTotal):
        self.cursor.callproc('addAssignment', [courseID, deadline,title, task, gradeTotal ])
        self.cnx.commit()

    def create_Exam(self, courseID, description, gradeTotal, examPercentage):
        self.cursor.callproc('addExam', [courseID, description, gradeTotal, examPercentage])
        self.cnx.commit()

    def submit_Assignment(self, assignmentID, studentID, content):
        self.cursor.callproc('addSubmission', [assignmentID, studentID, content])
        self.cnx.commit()

    def submit_AssignmentGrade(self, assignmentID, studentID, assignmentGrade):
        self.cursor.callproc('gradeAssignment', [assignmentID, studentID, assignmentGrade])
        self.cnx.commit()

    def submit_SubmissionGrade(self, submissionID, assignmentGrade):
        self.cursor.callproc('gradeSubmission', [submissionID, assignmentGrade])
        self.cnx.commit()

    def submit_ExamGrade(self, studentID, examID, examGrade):
        self.cursor.callproc('gradeExam', [studentID, examID, examGrade])
        self.cnx.commit()


    def del_Material(self, materialID):
        self.cursor.callproc('delMaterial', [materialID])
        self.cnx.commit()

    def del_Announcement(self, announcementID):
        self.cursor.callproc('delAnnouncement', [announcementID])
        self.cnx.commit()

    def del_Assignment(self, assignmentID):
        self.cursor.callproc('delAssignment', [assignmentID])
        self.cnx.commit()

    def del_Exam(self, examID):
        self.cursor.callproc('delExam', [examID])
        self.cnx.commit()
