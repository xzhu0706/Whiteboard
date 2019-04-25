
# # get_grades
def get_grades(cursor, cnx, courseID,userID):
    cursor.execute("SELECT userType FROM Users WHERE ID = %s;" % userID)
    for (userType) in cursor:
        uType = userType[0]

    sIDs = []
    if uType == 0:  # Student

        cursor.execute("SELECT assignmentPercentage FROM Courses WHERE courseID = %s;" % courseID)
        for (assignmentPercentage) in cursor:
            assignmentPercentage = assignmentPercentage[0]

        cursor.execute("SELECT AssignmentGrade.assignmentID, assignmentGrade,gradeTotal,"
                       "deadline,title, firstName,lastName "
                       "FROM AssignmentGrade LEFT JOIN Assignment "
                       "ON AssignmentGrade.assignmentID = Assignment.assignmentID "
                       "LEFT JOIN Users ON AssignmentGrade.studentID = Users.ID "
                       "WHERE courseID = %s AND studentID = %s "
                       "ORDER BY AssignmentGrade.assignmentID DESC;" % (courseID, userID))
        gradeDict = {"studentID": userID, "name": "",
                        "assignment": [], "assignmentPercentage": assignmentPercentage,
                        "exam": [], "finalGrade": 0}
        for (assignmentID, assignmentGrade, gradeTotal, deadline, title, firstName, lastName) in cursor:
            gradeDict["name"] = firstName + " " + lastName
            gradeDict["assignment"].append({"assignmentID": assignmentID, "assignmentTitle": title,
                                               "assignmentGrade": assignmentGrade, "gradeTotal": gradeTotal})

        cursor.execute("SELECT Exam.examID, examGrade,gradeTotal,examPercentage,description "
                       "FROM  TakenClasses LEFT JOIN Exam "
                       "ON TakenClasses.courseID = Exam.courseID "
                       "LEFT JOIN ExamGrade ON Exam.examID = ExamGrade.examID "
                       "AND ExamGrade.studentID = TakenClasses.studentID "
                       "WHERE TakenClasses.courseID = %s "
                       "AND TakenClasses.studentID = %s "
                       "ORDER BY Exam.examID DESC;" % (courseID, userID))
        for (examID, examGrade, gradeTotal, examPercentage, description) in cursor:
            gradeDict["exam"].append({"examID": examID, "examTitle": description,
                                         "examGrade": examGrade, "examPercentage": examPercentage,
                                         "gradeTotal": gradeTotal
                                         })
        finalGrade = update_finalgrade(cursor, cnx, courseID, userID)
        if finalGrade == False:
            return -1
        else:
            if finalGrade is not None:
                gradeDict["finalGrade"] = round(finalGrade, 2)
            else:
                gradeDict["finalGrade"] = finalGrade





    else:           # Professor
        cursor.execute("SELECT studentID From TakenClasses WHERE courseID = %s;" %courseID)
        for (studentID) in cursor:
            sIDs.append(studentID[0])

        cursor.execute("SELECT assignmentPercentage FROM Courses WHERE courseID = %s;" % courseID)
        for (assignmentPercentage) in cursor:
            assignmentPercentage = assignmentPercentage[0]
        gradeDict ={"percentage":{},"gradeTotal":{}, "title":{},"data":[]}
        gradeDict["percentage"]["assignmentPercentage"] = assignmentPercentage

        get = True
        for studentID in sIDs:
            # get assignment grade

            cursor.execute("SELECT AssignmentGrade.assignmentID, assignmentGrade,gradeTotal,"
                           "deadline,title, firstName,lastName "
                           "FROM AssignmentGrade LEFT JOIN Assignment "
                           "ON AssignmentGrade.assignmentID = Assignment.assignmentID "
                           "LEFT JOIN Users ON AssignmentGrade.studentID = Users.ID "
                           "WHERE courseID = %s AND studentID = %s "
                           "ORDER BY AssignmentGrade.assignmentID ASC;"%(courseID,studentID))

            studentGrade = {"ID": studentID, "name":"", "final":0.0}

            for (assignmentID, assignmentGrade, gradeTotal, deadline,title, firstName, lastName) in cursor:
                studentGrade["name"] = firstName + " " + lastName
                if assignmentID < 10:
                    assignmentName = "as0"+str(assignmentID)
                else: 
                    assignmentName = "as"+str(assignmentID)

                studentGrade[assignmentName]= assignmentGrade

                if get:
                    gradeDict["gradeTotal"][assignmentName] = gradeTotal
                    gradeDict["title"][assignmentName] = title

            #  Get exam grade
            cursor.execute("SELECT Exam.examID, examGrade,gradeTotal,examPercentage,description "
                           "FROM  TakenClasses LEFT JOIN Exam "
                           "ON TakenClasses.courseID = Exam.courseID "
                           "LEFT JOIN ExamGrade ON Exam.examID = ExamGrade.examID "
                           "AND ExamGrade.studentID = TakenClasses.studentID "
                           "WHERE TakenClasses.courseID = %s "
                           "AND TakenClasses.studentID = %s "
                           "ORDER BY Exam.examID ASC;" % (courseID, studentID))
            for(examID,examGrade,gradeTotal,examPercentage,description) in cursor:
                if examID < 10:
                    examName = "ex0"+str(examID)
                else:
                    examName = "ex"+str(examID)

                studentGrade[examName] = examGrade
                if get:
                    gradeDict["gradeTotal"][examName] = gradeTotal
                    gradeDict["title"][examName] = description
                    gradeDict["percentage"][examName] = examPercentage

            # finalGrade = update_finalgrade(cursor,cnx, courseID,studentID)
            # if finalGrade == False:
            #     return -1
            # else:
            #     if finalGrade is not None:
            #         studentGrade["final"] = round(finalGrade,2)
            #     else:
            #         studentGrade["final"] = finalGrade
            # gradeDict['data'].append(studentGrade)

    if not gradeDict:
        return -1
    return gradeDict

