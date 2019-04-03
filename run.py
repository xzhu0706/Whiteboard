from flask import Flask, jsonify,request
from flask_cors import CORS
from DB_Get import getUser
from DB_Post import postUser
import datetime

app = Flask(__name__)
CORS(app, support_credentials=True)


# @app.route("/auth/login", methods=['GET'])
# given: username, password
# return: dict of (ID, userType, firstName, lastName) if correct login
# 		  message if login info not correct
@app.route("/auth/login", methods=['POST'])
def login():
	json_load = request.get_json()

	username = json_load['username']
	password = json_load['password']

	id_type = gUser.login_check(username, password)

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
	courseList = gUser.get_Courses(userID)

	if courseList == -1:
		return jsonify(found=False), 404
	else:
		return jsonify(courseList), 200


# @app.route("/api/courseinfo/<courseID>", methods=['GET'])
# given: userId
# return:
# 		  list of dict: (courseName, semester, year,professorName,professorEmail)
# 		  found=False if no course found
@app.route("/api/courseinfo/<courseID>", methods=['GET'])
def courseInfo(courseID):
	course = gUser.get_courseInfo(courseID)

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

	materialList = gUser.get_Materials(courseID)
	if materialList != -1:
		return jsonify(found=False), 404
	else:
		return jsonify(materialList), 200



# @app.route("/api/createMaterial", methods=['POST'])
# given: courseId, material
# return: boolean of success or not of updating DB
@app.route("/api/createMaterial", methods=['POST'])
def createMaterial():
	json_load = request.get_json()
	courseID = json_load['courseID']
	material = json_load['material']

	# boolean value of update in DB or not
	boolean = pUser.uploadMaterial(courseID,material)

	return jsonify(update=boolean)


# @app.route("/api/announcement/<courseID>", methods=['GET'])
# given: courseId
# return:
# 		list of dict: (announcementID, announcement, postTime) for that courseID
# 		(sort by postTime)
# 		found=False if No Annocement Found
@app.route("/api/announcement/<courseID>", methods=['GET'])
def announcementInfo(courseID):
	announcementList = gUser.get_Annocement(courseID)

	if announcementList == -1:
		return jsonify(found=False), 404
	else:
		return jsonify(announcementList), 200


# @app.route("/api/createAnnocement", methods=['POST'])
# given: courseId, material
# return: boolean of success or not of updating DB
@app.route("/api/createAnnocement", methods=['POST'])
def createAnnocement():
	json_load = request.get_json()
	courseID = json_load['courseID']
	announcement = json_load['announcement']

	# boolean value of update in DB or not
	boolean = pUser.makeAnnouncement(courseID,announcement)

	return jsonify(update=boolean)




# @app.route("/api/assignments/<courseID>", methods=['GET])
# given: courseId
# return: dict of list: (assignID, task, gradeTotal,deadline, postTime) of that courseId
# 		(sort by postTime)
# 		found=False if No Assignment Found
@app.route("/api/assignments/<courseID>", methods=['GET'])
def assignmentInfo(courseID):
	assignmentList = gUser.get_Assignments(courseID)

	if assignmentList == -1:
		return jsonify(found=False), 404
	else:
		return jsonify(assignmentList), 200


# @app.route("/api/createAssignment", methods=['POST'])
# given: userId, courseId, task, deadline, gradeTotal
# return: boolean of success or not of updating DB
@app.route("/api/createAssignment", methods=['POST'])
def createAss():
	json_load = request.get_json()
	courseID = json_load['courseID']
	task = json_load['task']
	# for deadline: just give n day after current day
	deadlineDay = json_load['deadline']
	deadline = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=deadlineDay), datetime.time.max)

	gradeTotal = json_load['gradeTotal']

	# boolean value of update in DB or not
	boolean = pUser.createAssignment(courseID,deadline,task,gradeTotal)

	return jsonify(update=boolean)


# #############################################
# Below still need modify

# @app.route("/api/grades", methods=['GET'])
# given: userId & courseId
# return:
# 		For professor (sorted by student lastname), student final grade
# 		  	dict of list: (studentID, grade, studentFirstName, studentLastName,courseName)
# 		For student  (sorted by professor lastname), assignment grade and final grade
# 		  	dict of list: (courseName, professorID, grade, professorFirstName, professorLastName )
# return message if no grade found
@app.route("/api/grades", methods=['GET'])
def gradeInfo():
	json_load = request.get_json()
	userID = json_load['userId']
	courseID = json_load['courseId']

	grades = gUser.get_grades(userID,courseID)

	if grades == -1:
		return jsonify(message="You haven't assign any grade yet.")
	elif grades == -2:
		return jsonify(message="No grade have been posted")
	else:
		return jsonify(grades), 200


# @app.route("/api/submission", methods=['GET'])
# given: assignId    (for professor see student submission)
# return: dict of list: (file, submitTime, studentID, studentFirstName, studentLastName)
# return message if no Submission found
@app.route("/api/submission", methods=['GET'])
def getSubmission():
	json_load = request.get_json()
	assignID = json_load['assignId']
	submissions = gUser.get_submission(assignID)

	if submissions != -1:
		return jsonify(submissions), 200
	else:
		return jsonify(message = "No Submission Found")

# @app.route("/api/submit_assign", methods=['POST'])
# given: userId, assignId, file (maybe more)
# return: message of success or not of updating DB
@app.route("/api/submit_assign", methods=['POST'])
def submitAss():
	json_load = request.get_json()
	studentID = json_load['userId']
	assignID = json_load['assignID']
	file = json_load['file']

	message = pUser.create_Submission(studentID,assignID,file)
	return jsonify(message = message)








# @app.route("/api/assign_grade", methods=['POST'])
# Can assign for any grade (assignment/Exam/Project/....)
# 			Set submission as 0 if not grade for assignment
# 			Assume totalgrade for Exam is 100
# given: studentId, submissionId,courseId, grade,description (maybe more)
# return: message of success or not of updating DB, update for finalgrade
@app.route("/api/assign_grade", methods=['POST'])
def postGrade():
	json_load = request.get_json()
	studentID = json_load['studentId']
	submissionID = json_load['submissionId']     # if is not a assignment,
	courseID = json_load['courseId']
	grade = json_load['grade']
	description = json_load['description']

	message = pUser.assign_grade(studentID,submissionID,courseID,grade,description)
	return jsonify(message=message)





if __name__ == "__main__":
	config = {
		"user": '',
		"password": '',
		"host": '127.0.0.1',
		"database": 'Whiteboard3'
	}
	gUser = getUser(config)
	pUser = postUser(config)
	app.run()