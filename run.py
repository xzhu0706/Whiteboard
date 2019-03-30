from flask import Flask, jsonify,request
from flask_cors import CORS
from DB_Get import getUser
from DB_Post import postUser

app = Flask(__name__)
CORS(app, support_credentials=True)


# @app.route("/auth/login", methods=['GET'])
# given: username, password
# return: dict of (ID, userType, firstName, lastName) if correct login
# 		  message if login info not correct
@app.route("/auth/login", methods=['GET'])
def login():
	json_load = request.get_json()

	username = json_load['username']
	password = json_load['password']

	# print("Username %s, Password %s"% (username,password))

	id_type = gUser.login_check(username, password)

	if id_type != -1:
		return jsonify(id_type), 200
	else:
		return jsonify(authorization=False, message = "Wrong username or password"), 403


# @app.route("/api/courses", methods=['GET'])
# given: userId
# return: dict of list: (courseName, semester, year, courseID) for professor
# 		  dict of list: (courseName, semester, year, courseID,professorName,professorEmail) for student
# 		Sorted by semester and year
# return message if no course found
@app.route("/api/courses", methods=['GET'])
def courseInfo():
	json_load = request.get_json()
	userID = json_load['userId']
	course = gUser.get_CourseInfo(userID)

	if course == -1:
		return jsonify(message="No Course Found for the professor")
	elif course == -2:
		return jsonify(message="No Course Found for the student")
	else:
		return jsonify(course), 200


# @app.route("/api/materials", methods=['GET'])
# given: courseId
# return: dict of list: (material, time) for materials for that courseId (sort by time)
# 		  message if No Material Found
@app.route("/api/materials", methods=['GET'])
def materialInfo():
	json_load = request.get_json()
	courseID = json_load['courseId']

	material = gUser.get_Materials(courseID)
	if material != -1:
		return jsonify(material), 200
	else:
		return jsonify(message = "No Material Found")



# @app.route("/api/assignments", methods=['GET])
# given: courseId
# return: dict of list: (assignID, deadline, task, gradeTotal, postTime) that courseId (sort by time)
# 		  message if No Assignment Found
@app.route("/api/assignments", methods=['GET'])
def assignmentInfo():
	json_load = request.get_json()
	courseID = json_load['courseId']

	assignment = gUser.get_Assignments(courseID)
	if assignment != -1:
		return jsonify(assignment), 200
	else:
		return jsonify(message = "No Assignment Found")


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


# @app.route("/api/create_assign", methods=['POST'])
# given: userId, courseId, task, due date, gradeTotal
# return: message of success or not of updating DB
@app.route("/api/create_assign", methods=['POST'])
def createAss():
	json_load = request.get_json()
	courseID = json_load['courseId']
	task = json_load['task']
	deadline = json_load['deadline']
	gradeTotal = json_load['gradeTotal']

	message = pUser.create_Assignment(courseID,deadline,task,gradeTotal)
	return jsonify(message=message)

# @app.route("/api/create_material", methods=['POST'])
# given: courseId, file (maybe more)
# return: message of success or not of updating DB
app.route("/api/create_material", methods=['POST'])
def createMaterial():
	json_load = request.get_json()
	courseID = json_load['courseId']
	material = json_load['material']

	message = pUser.create_Material(courseID,material)
	return jsonify(message=message)




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
	gUser = getUser()
	pUser = postUser()
	app.run()