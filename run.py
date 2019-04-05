from flask import Flask, jsonify,request
from flask_cors import CORS
from DB_init import db_User
# from DB_Post import postUser
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


# @app.route("/api/assignments/<courseID>", methods=['GET])
# given: courseId, userID
# return:
# 		dict of list: (assignID, task, title, gradeTotal,deadline, postTime,pastDue) for professor
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


# @app.route("/api/createAssignment", methods=['POST'])
# given: userId, courseId, task, deadline, gradeTotal
# return: boolean of success or not of updating DB
@app.route("/api/createAssignment", methods=['POST'])
def createAss():
	json_load = request.get_json()
	courseID = json_load['courseID']
	title = json_load['title']
	task = json_load['task']
	# for deadline: just give n day after current day
	deadlineDay = json_load['deadline']
	deadline = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=deadlineDay), datetime.time.max)
	gradeTotal = json_load['gradeTotal']

	# boolean value of update in DB or not
	boolean = User.createAssignment(courseID,deadline,title,task,gradeTotal)

	return jsonify(update=boolean)


@app.route('/api/deleteAnnouncement/<announcementID>', methods=['DELETE'])
def delAnnouncement(announcementID):
	# boolean value of update in DB or not
	boolean = User.del_Announcement(announcementID)
	return jsonify(update=boolean)

@app.route('/api/deleteAssignment/<assignID>', methods=['DELETE'])
def delAssignment(assignID):
	# boolean value of update in DB or not
	boolean = User.del_Assignment(assignID)
	return jsonify(update=boolean)


@app.route('/api/deleteMaterial/<materialID>', methods=['DELETE'])
def delMaterial(materialID):
	# boolean value of update in DB or not
	boolean = User.del_Material(materialID)

	return jsonify(update=boolean)


# @app.route("/api/submitAssignment", methods=['POST'])
# Need assignID, studentID, assignmentContent
# return: boolean of success or not of updating DB
@app.route("/api/submitAssignment", methods=['POST'])
def submitAss():
	json_load = request.get_json()
	assignID = json_load['assignID']
	studentID = json_load['studentID']
	content = json_load['content']

	boolean = User.submit_Assignment(assignID,studentID,content)
	return jsonify(update=boolean)


# @app.route("/api/submission/<assignID>", methods=['GET'])
# given: assignID    (for professor see student submission)
# return: list of dict: (submissionID, studentID, content, submitTime, studentName,isSubmit)
# 		if the student no submit the assign yet:
# 				submissionID,content, and submitTime will be NULL, and isSubmit will be False
# 		found=False if No Student Found for that assignment

@app.route("/api/submissions/<assignID>", methods=['GET'])
def getSubmission(assignID):
	submissionList = User.get_Submission(assignID)

	if submissionList == -1:
		return jsonify(found=False), 404
	else:
		return jsonify(submissionList), 200

# @app.route("/api/gradeSubmission", methods=['POST'])
# given: submissionID, grade
@app.route("/api/gradeSubmission", methods=['POST'])
def gradeSubmission():
	json_load = request.get_json()
	submissionID = json_load['submissionID']
	grade = json_load['grade']

	boolean = User.submit_Grade(submissionID, grade)
	return jsonify(update=boolean)
# ################################################################

@app.route("/api/grade/<courseID>/<userID>", methods=['GET'])
def getGrade(courseID,userID):
	submissionList = User.get_Submission(courseID)###########

	if submissionList == -1:
		return jsonify(found=False), 404
	else:
		return jsonify(submissionList), 200

#
# # @app.route("/api/grades", methods=['GET'])
# # given: userId & courseId
# # return:
# # 		For professor (sorted by student lastname), student final grade
# # 		  	dict of list: (studentID, grade, studentFirstName, studentLastName,courseName)
# # 		For student  (sorted by professor lastname), assignment grade and final grade
# # 		  	dict of list: (courseName, professorID, grade, professorFirstName, professorLastName )
# # return message if no grade found
# @app.route("/api/grades", methods=['GET'])
# def gradeInfo():
# 	json_load = request.get_json()
# 	userID = json_load['userId']
# 	courseID = json_load['courseId']
#
# 	grades = User.get_grades(userID,courseID)
#
# 	if grades == -1:
# 		return jsonify(message="You haven't assign any grade yet.")
# 	elif grades == -2:
# 		return jsonify(message="No grade have been posted")
# 	else:
# 		return jsonify(grades), 200




if __name__ == "__main__":
	config = {
		"user": '',
		"password": '',
		"host": '127.0.0.1',
		"database": 'Whiteboard'
	}

	User = db_User(config)
	app.run()



# For student, get grade return all assignment grade, assignment title, examtitle, examgrade, final grade
# For professor, get grade return all (assignment grade, assignment title, examtitle, examgrade, final grade) for each student