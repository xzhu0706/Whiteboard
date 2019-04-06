from flask import Flask, jsonify,request
from flask_cors import CORS
from DB_init import db_User
import datetime

app = Flask(__name__)
CORS(app, support_credentials=True)

#-------------------------------------------- Check in with DB -------------------------------------------------------#
# @app.route("/auth/login", methods=['GET'])
# given: username, password
# return: dict of (ID, userType, firstName, lastName) if correct login
# 		  message if login info not correct
@app.route("/auth/login", methods=['POST'])
def login():
	json_load = request.get_json()

	username = json_load['username']
	password = json_load['password']

	id_type = User.login_check(username, password)

	if id_type != -1:
		return jsonify(id_type), 200
	else:
		return jsonify(authorization=False, message="Wrong username or password"), 403


# @app.route("/api/courses/<userID>", methods=['GET'])
# given: userId
# return: list of dict: (courseID, courseName, semester, year) for both prof and student
# 		Sorted by semester and year
# 		found=False if no course found
@app.route("/api/courses/<userID>", methods=['GET'])
def courses(userID):
	courseList = User.get_Courses(userID)

	if courseList == -1:
		return jsonify(found=False), 404
	else:
		return jsonify(courseList), 200


# @app.route("/api/courseinfo/<courseID>", methods=['GET'])
# given: userId
# return:
# 		  list of dict: (courseName, semester, year,professorName,professorEmail)
# 		  found=False if no course found
@app.route("/api/courseInfo/<courseID>", methods=['GET'])
def courseInfo(courseID):
	course = User.get_courseInfo(courseID)

	if course == -1:
		return jsonify(found=False), 404
	else:
		return jsonify(course), 200


# @app.route("/api/materials/<courseID>", methods=['GET'])
# given: courseId
# return:
# 		list of dict: (materialID, material, postTime) for that courseID
# 		(sort by postTime)
# 		found=False if No Material Found
@app.route("/api/materials/<courseID>", methods=['GET'])
def materialInfo(courseID):

	materialList = User.get_Materials(courseID)
	if materialList == -1:
		return jsonify(found=False)
	else:
		return jsonify(materialList), 200

# @app.route("/api/announcement/<courseID>", methods=['GET'])
# given: courseId
# return:
# 		list of dict: (announcementID, announcement, postTime) for that courseID
# 		(sort by postTime)
# 		found=False if No Annocement Found
@app.route("/api/announcement/<courseID>", methods=['GET'])
def announcementInfo(courseID):
	announcementList = User.get_Announcement(courseID)

	if announcementList == -1:
		return jsonify(found=False)
	else:
		return jsonify(announcementList), 200

# @app.route("/api/assignments/<courseID>", methods=['GET])
# given: courseId, userID
# return:
# 		dict of list: (assignmentID, task, title, gradeTotal,deadline, postTime,pastDue) for professor
# 		extra boolean data: isSumbit     for student
# 		(sort by postTime)
# 		found=False if No Assignment Found
@app.route("/api/assignments/<courseID>/<userID>", methods=['GET'])
def assignmentInfo(courseID,userID):
	assignmentList = User.get_Assignments(courseID,userID)

	if assignmentList == -1:
		return jsonify(found=False)
	else:
		return jsonify(assignmentList), 200

# @app.route("/api/submission/<assignmentID>", methods=['GET'])
# given: assignmentID    (for professor see student submission)
# return: list of dict: (submissionID, studentID, content, submitTime, studentName,isSubmit)
# 		if the student no submit the assign yet:
# 				submissionID,content, and submitTime will be NULL, and isSubmit will be False
# 		found=False if No Student Found for that assignment

@app.route("/api/submissions/<assignmentID>", methods=['GET'])
def getSubmission(assignmentID):
	submissionList = User.get_Submission(assignmentID)

	if submissionList == -1:
		return jsonify(found=False), 404
	else:
		return jsonify(submissionList), 200

# For student return a dict of {"assignment":[], "exam":[], "final": number}
# 		where "assignment" is list of {"assignmentTitle", "assignmentGrade"}
# 			 "exam" is list of {"examTitle", "examGrade"}

# For professor return list of dict
# 		{"studentID", "name", "assignment":[], "exam":[], "final"}
# 		"assignment" and "exam" have same layout as student
@app.route("/api/grade/<courseID>/<userID>", methods=['GET'])
def getGrade(courseID,userID):
	submissionList = User.get_Grades(courseID,userID)
	if submissionList == -1:
		return jsonify(found=False), 404
	else:
		return jsonify(submissionList), 200


#----------------------------- Create Material/Announcement/Assignment/Exam --------------------------------#

# @app.route("/api/createMaterial", methods=['POST'])
# given: courseId, material
# return: boolean of success or not of updating DB
@app.route("/api/createMaterial", methods=['POST'])
def createMaterial():
	json_load = request.get_json()
	courseID = json_load['courseID']
	material = json_load['material']

	# boolean value of update in DB or not
	boolean = User.uploadMaterial(courseID,material)

	return jsonify(update=boolean)


# @app.route("/api/createAnnouncement", methods=['POST'])
# given: courseId, material
# return: boolean of success or not of updating DB
@app.route("/api/createAnnouncement", methods=['POST'])
def createAnnouncement():
	json_load = request.get_json()
	courseID = json_load['courseID']
	announcement = json_load['announcement']

	# boolean value of update in DB or not
	boolean = User.makeAnnouncement(courseID,announcement)

	return jsonify(update=boolean)


# @app.route("/api/createAssignment", methods=['POST'])
# given: courseID, title, task, deadline, gradeTotal
# for deadline: just give n day after current day
# return: boolean of success or not of updating DB
@app.route("/api/createAssignment", methods=['POST'])
def createAss():
	json_load = request.get_json()
	courseID = json_load['courseID']
	title = json_load['title']
	task = json_load['task']
	# for deadline: just give n day after current day
	deadlineDay = int(json_load['deadline'])
	deadline = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=deadlineDay), datetime.time.max)
	gradeTotal = json_load['gradeTotal']

	# boolean value of update in DB or not
	boolean = User.createAssignment(courseID,deadline,title,task,gradeTotal)

	return jsonify(update=boolean)

# @app.route("/api/createExam", methods=['POST'])
# given: courseID,examTitle, examPercentage gradeTotal
# return: boolean of success or not of updating DB
@app.route("/api/createExam", methods=['POST'])
def createExam():
	json_load = request.get_json()
	courseID = json_load['courseID']
	gradeTotal = json_load['gradeTotal']
	examTitle = json_load['examTitle']
	examPercentage = json_load['examPercentage']
	boolean = User.create_Exam(courseID, examTitle, gradeTotal,examPercentage)
	return jsonify(update=boolean)


#------------------ Submit Assignment(student), Submit Grade for Assignment/Submission --------------------------------#
# @app.route("/api/submitAssignment", methods=['POST'])
# Need assignmentID, studentID, assignmentContent
# return: boolean of success or not of updating DB
@app.route("/api/submitAssignment", methods=['POST'])
def submitAss():
	json_load = request.get_json()
	assignmentID = json_load['assignmentID']
	studentID = json_load['studentID']
	content = json_load['content']

	boolean = User.submit_Assignment(assignmentID,studentID,content)
	return jsonify(update=boolean)


# Grade for not submitted assignment
# @app.route("/api/gradeAssignment", methods=['POST'])
# given: assignmentID, studentID, assignmentGrade
# return: boolean of success or not of updating DB
@app.route("/api/gradeAssignment", methods=['POST'])
def gradeAssignment():
	json_load = request.get_json()
	assignmentID = json_load['assignmentID']
	studentID = json_load['studentID']
	assignmentGrade = json_load['assignmentGrade']

	boolean = User.submit_AssignmentGrade(assignmentID, studentID, assignmentGrade)
	return jsonify(update=boolean)



# @app.route("/api/gradeSubmission", methods=['POST'])
# given: submissionID, grade
# return: boolean of success or not of updating DB
@app.route("/api/gradeSubmission", methods=['POST'])
def gradeSubmission():
	json_load = request.get_json()
	submissionID = json_load['submissionID']
	assignmentGrade = json_load['assignmentGrade']

	boolean = User.submit_SubmissionGrade(submissionID, assignmentGrade)
	return jsonify(update=boolean)


# @app.route("/api/gradeExam", methods=['POST'])
# given: studentID, examID,examGrade
# return: boolean of success or not of updating DB
@app.route("/api/gradeExam", methods=['POST'])
def gradeExam():
	json_load = request.get_json()
	studentID = json_load['studentID']
	examID = json_load['examID']
	examGrade = json_load['examGrade']

	boolean = User.submit_ExamGrade(studentID, examID, examGrade)
	return jsonify(update=boolean)



#------------------------------ Delete Material/Announcement/Assignment/Exam --------------------------------#

@app.route('/api/deleteAnnouncement/<announcementID>', methods=['DELETE'])
def delAnnouncement(announcementID):
	# boolean value of update in DB or not
	boolean = User.del_Announcement(announcementID)
	return jsonify(update=boolean)

@app.route('/api/deleteAssignment/<assignmentID>', methods=['DELETE'])
def delAssignment(assignmentID):
	# boolean value of update in DB or not
	boolean = User.del_Assignment(assignmentID)
	return jsonify(update=boolean)

@app.route('/api/deleteMaterial/<materialID>', methods=['DELETE'])
def delMaterial(materialID):
	# boolean value of update in DB or not
	boolean = User.del_Material(materialID)
	return jsonify(update=boolean)

@app.route('/api/deleteExam/<examID>', methods=['DELETE'])
def delMaterial(examID):
	# boolean value of update in DB or not
	boolean = User.del_Exam(examID)
	return jsonify(update=boolean)










if __name__ == "__main__":
	config = {
		"user": '',
		"password": '',
		"host": '127.0.0.1',
		"database": 'Whiteboard'
	}

	User = db_User(config)
	app.run()

