from collections import defaultdict
import datetime

def login_check(cursor, username, password):

    qry = "SELECT ID, userType, firstName, lastName FROM Users WHERE userName = %s AND password= %s ;"
    cursor.execute(qry, (username, password))

    for (ID, userType, firstName, lastName) in cursor:
        # print("ID = {:d}, userType={:d}".format(ID, userType))
        return {"ID": ID, "userType": userType, "firstName": firstName, "lastName": lastName}

    return -1

def get_Courses(cursor, userID):
    cursor.execute("SELECT userType FROM Users WHERE ID = %s;" % userID)
    for (userType) in cursor:
        uType = userType[0]

    if uType == 1:  # Professor
        cursor.execute("SELECT courseID, courseName,semester,year "
                            "FROM Courses WHERE professorID = %s "
                            "ORDER BY year ASC,semester DESC;" % userID)
    else:  # student
        cursor.execute("SELECT courseID, courseName,semester,year "
                            "FROM Courses NATURAL JOIN TakenClasses "
                            "WHERE studentID = %s "
                            "ORDER BY year ASC,semester DESC;" % userID)
    coursesInfo = []
    for (courseID, courseName, semester, year) in cursor:
        coursesInfo.append({'courseID': courseID, 'courseName': courseName,
                            'semester': semester, 'year': year})

    if not coursesInfo:
        return -1
    return coursesInfo

def get_courseInfo(cursor, courseID):
    qry = "SELECT professorID,courseName, semester,year, firstName,lastName,email " \
          "FROM Users JOIN Courses ON Users.ID = Courses.professorID " \
          "WHERE courseID = %(courseID)s ORDER BY year ASC,semester DESC;"
    cursor.execute(qry, {"courseID": courseID})

    courseInfo = {}
    for (professorID, courseName, semester, year, firstName, lastName, email) in cursor:
        courseInfo['courseName'] = courseName
        courseInfo['semester'] = semester
        courseInfo['year'] = year
        courseInfo['professorID'] = professorID
        courseInfo['professorName'] = firstName + " " + lastName
        courseInfo['professorEmail'] = email

    if not courseInfo:
        return -1
    return courseInfo

def get_Materials(cursor, courseID):
    qry = "SELECT materialID, material,postTime " \
          "FROM ClassMaterials WHERE courseID = %(courseID)s ORDER BY postTime DESC;"
    cursor.execute(qry, {"courseID": courseID})

    materialInfo = []
    for (materialID, content, postTime) in cursor:
        materialInfo.append({'materialID': materialID, 'material': content,
                             'postTime': postTime.strftime("%m/%d/%Y, %H:%M:%S")})

    if not materialInfo:
        return -1
    return materialInfo

def get_Announcement(cursor, courseID):
    qry = "SELECT announcementID, announcement,postTime " \
          "FROM ClassAnnouncement WHERE courseID = %(courseID)s ORDER BY postTime DESC;"
    cursor.execute(qry, {"courseID": courseID})

    announcementInfo = []
    for (announcementID, content, postTime) in cursor:
        announcementInfo.append({'announcementID': announcementID, 'announcement': content,
                                 'postTime': postTime.strftime("%m/%d/%Y, %H:%M:%S")})
    if not announcementInfo:
        return -1
    return announcementInfo

def get_Assignments(cursor, courseID, ID):
    cursor.execute("SELECT userType FROM Users WHERE ID = %s;" % ID)
    for (userType) in cursor:
        uType = userType[0]


    qry = "SELECT assignID, deadline,task,gradeTotal,postTime " \
          "FROM Assignment WHERE courseID = %(courseID)s ORDER BY postTime DESC;"
    cursor.execute(qry, {"courseID": courseID})

    assignmentInfo = []
    for (assignID, deadline, task, gradeTotal, postTime) in cursor:
        if deadline < datetime.datetime.now():
            pastDue = True
        else:
            pastDue = False
        assignmentInfo.append({'assignID': assignID, 'task': task, 'gradeTotal': gradeTotal,
                               'deadline': deadline.strftime("%m/%d/%Y, %H:%M:%S"),
                               'postTime': postTime.strftime("%m/%d/%Y, %H:%M:%S"),
                               'pastDue': pastDue
                               })
    if uType == 0:
        for dict in assignmentInfo:
            assignID = dict['assignID']
            cursor.execute("SELECT submissionID FROM AssignmentSubmission "
                           "WHERE studentID = %s AND assignID = %s;" % (ID,assignID))
            dict['isSubmit'] = False
            for (submissionID) in cursor:
                dict['isSubmit'] = True

    if not assignmentInfo:
        return -1
    return assignmentInfo


def get_submission(cursor, assignID):

    cursor.execute("SELECT submissionID, TakenClasses.studentID, file, gradeTotal, uploadTime, Users.firstName,Users.lastName "
                   "FROM TakenClasses JOIN Assignment "
                   "ON TakenClasses.courseID = Assignment.courseID AND assignID = %s "
                   "LEFT JOIN AssignmentSubmission "
                   "ON AssignmentSubmission.studentID = TakenClasses.studentID "
                   "AND AssignmentSubmission.assignID=Assignment.assignID "
                   "JOIN Users ON TakenClasses.studentID = Users.ID "
                   "ORDER BY Users.lastName ASC;"% assignID)

    submissionInfo = []
    for (submissionID, studentID, file, gradeTotal, uploadTime, firstName, lastName) in cursor:
        if submissionID == None:
            submissionInfo.append({'submissionID': None, 'studentID': studentID,
                                   'content': None, 'gradeTotal': gradeTotal,
                                   'submitTime': None,
                                   'studentName': firstName + ' ' + lastName,
                                   'isSubmit': False

                                   })
        else:
            submissionInfo.append({'submissionID':submissionID, 'studentID':studentID,
                                   'content':file, 'gradeTotal': gradeTotal,
                                   'submitTime':uploadTime,
                                   'studentName': firstName+' '+lastName,
                                   'isSubmit':True

            })

    if not submissionInfo:
        return -1
    return submissionInfo



# ################################
# Below still need modify

# # get_grades
# def get_grades(cursor, userID, courseID):
#     cursor.execute("SELECT userType FROM Users WHERE ID = %s;" % userID)
#     for (userType) in cursor:
#         uType = userType[0]
#
#     if uType == 1:  # Professor
#         qry = "SELECT TakenClasses.studentID, TakenClasses.grade, Users.firstName,Users.lastName,Courses.courseName " \
#               "FROM Courses NATURAL JOIN TakenClasses " \
#               "JOIN Users ON TakenClasses.studentID = Users.ID " \
#               "WHERE coursesID = %s AND professorID = %s ORDER BY Users.lastName ASC;"
#         cursor.execute(qry, (courseID, userID))
#
#         gradeInfo = defaultdict(list)
#         for (studentID, grade, firstName, lastName, courseName) in cursor:
#             gradeInfo['studentID'].append(studentID)
#             gradeInfo['grade'].append(grade)
#             gradeInfo['studentFirstName'].append(firstName)
#             gradeInfo['studentLastName'].append(lastName)
#             gradeInfo['courseName'].append(courseName)
#
#         if not gradeInfo:
#             return -1
#
#     else:  # Student
#         qry = "SELECT Courses.courseName, Courses.professorID, TakenClasses.grade, Users.firstName,Users.lastName " \
#               "FROM TakenClasses NATURAL JOIN Courses " \
#               "JOIN Users ON Courses.professorID = Users.ID " \
#               "WHERE coursesID = %s AND studentID = %s ORDER BY Users.lastName ASC;"
#         cursor.execute(qry, (courseID, userID))
#
#         gradeInfo = defaultdict(list)
#         for (courseName, professorID, grade, firstName, lastName) in cursor:
#             gradeInfo['courseName'].append(courseName)
#             gradeInfo['professorID'].append(professorID)
#             gradeInfo['finalgrade'].append(grade)
#             gradeInfo['professorFirstName'].append(firstName)
#             gradeInfo['professorLastName'].append(lastName)
#         if not gradeInfo:
#             return -2
#     return gradeInfo

