import mysql.connector
from mysql.connector import errorcode
from DB_functions import DB
import datetime
config = {
    "user": '',
    "password": '',
    "host": '127.0.0.1',
    "database": 'Whiteboard'
}

User = DB(config)

usr = User.login_check('Ada753','26okzoiysg')

cour = User.get_Courses(3)

cinfo = User.get_courseInfo(1)

m = User.get_Materials(1)

ann = User.get_Announcement(2)

assP = User.get_Assignments(1, 10)

assS = User.get_Assignments(3, 2)

sub = User.get_Submission(1)

upM = User.uploadMaterial(1, "Test")

upAnn = User.makeAnnouncement(1, "Test ANN")

upAss = User.addAssignment(1,datetime.datetime.now(),"tre","sdgf",103)

upEx = User.create_Exam(1,"tes",80,20)

subAss = User.submit_Assignment(1,5,"dsfagf")

subAG = User.submit_AssignmentGrade(1,5,80)

subSG = User.submit_SubmissionGrade(2, 90)

subEG = User.submit_ExamGrade(5,1,90)

delM = User.del_Material(2)

delAnn = User.del_Announcement(2)

delAss = User.del_Assignment(8)

delEx = User.del_Exam(6)
print()