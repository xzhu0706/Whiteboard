from DB_init import db_User
import datetime
config = {
    "user": '',
    "password": '',
    "host": '127.0.0.1',
    "database": 'Whiteboard2'
}

User = db_User(config)

# Parameters, student or professor currently have course
userName ="Allan105"
password = "r3vwfi1hz2"

########   Test GET
# Login
login = User.login_check(userName,password)
userID = login['ID']
userType = login['userType']

# Course
courseList = User.get_Courses(userID)
seletedCourseID = courseList[0]['courseID']

courseListInfo = User.get_courseInfo(seletedCourseID)

# Material
materials = User.get_Materials(seletedCourseID)
# Announcement
announcement = User.get_Announcement(seletedCourseID)

# Assignment
assignments = User.get_Assignments(seletedCourseID, userID)
seletedAssignmentID = assignments[6]['assignmentID']

# Submission
submission = User.get_Submission(seletedAssignmentID)

# Gradebook
gradeBook = User.get_Grades(seletedCourseID,userID)

########## Test Create
if userType == 1:       #(Only allow by professor)

    uploadMaterial = User.uploadMaterial(seletedCourseID,"Material - For extra reading")
    makeAnnouncement = User.makeAnnouncement(seletedCourseID, "No Class next Monday")

    deadlineDay = 10
    deadline = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=deadlineDay),
                                         datetime.time.max)

    createAssignment = User.createAssignment(seletedCourseID,deadline=deadline, title="Extra Credit",
                                             task = "Write Analysis for the paper",
                                             gradeTotal= 50)
    create_Exam = User.create_Exam(seletedCourseID,description="Pop Quiz",
                                   gradeTotal=100, examPercentage=5)
# ######## Test Submission
if userType == 0:       #(Only allow by professor submit assignment)
    submit_Assignment = User.submit_Assignment(seletedAssignmentID,userID,"Finish Reading!!!")

if userType == 1:
    # Grade Assignment
    submission = User.get_Submission(seletedAssignmentID)
    seletedSubmissionID = 0
    for student in submission:
        if student['submissionID'] is not None:
            seletedSubmissionID = student['submissionID']

    submit_AssignmentGrade = User.submit_AssignmentGrade(seletedSubmissionID,assignmentGrade=90)



    # Grade Exam
    gradeBook = User.get_Grades(seletedCourseID, userID)
    selectedStudent = 0
    seletedExamID = 0
    for student in gradeBook:
        if student['exam'][0]['examID'] is not None:
            seletedExamID = student['exam'][0]['examID']
            selectedStudent =student['studentID']
            break
    submit_ExamGrade = User.submit_ExamGrade(selectedStudent,seletedExamID,examGrade=50)

# ####### Test Delete
del_Material = User.del_Material(materialID=1)
del_Announcement = User.del_Announcement(announcementID= 1)
del_Assignment = User.del_Assignment(assignmentID=1)

del_Exam = User.del_Exam(examID=3)


print()