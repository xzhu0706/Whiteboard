from flask import Flask, jsonify,request
from flask_cors import CORS
from dataBase import User

app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route("/auth/login", methods=['POST'])
def login():

	# TODO: need to check with DB
	json_load = request.get_json()

	username = json_load['username']
	password = json_load['password']

	print("Username %s, Password %s"% (username,password))

	id_type = user.login_check(username, password)

	if id_type != -1:
		return jsonify(id_type), 200
	else:
		return jsonify(authorization=False, message = "Wrong username or password"), 403


# @app.route("/api/courses", methods=['GET'])
# given: userId
# need: courses taken for that userid (maybe sort by semester & year)
@app.route("/api/courses", methods=['GET'])
def courseInfo():
	json_load = request.get_json()
	userID = json_load['userId']
	course = user.get_CourseInfo(userID)

	if course != -1:
		return jsonify(course), 200
	else:
		return jsonify(message = "No Course Found")


# @app.route("/api/materials", methods=['GET'])
# given: courseId
# need: materials for that courseId (sort by time)
@app.route("/api/materials", methods=['GET'])
def materialInfo():
	json_load = request.get_json()
	courseID = json_load['courseId']

	material = user.get_Materials(courseID)
	if material != -1:
		return jsonify(material), 200
	else:
		return jsonify(message = "No Material Found")



# @app.route("/api/assignments", methods=['GET])
# given: courseId
# need: posted assignments for that courseId (sort by time)
@app.route("/api/assignments", methods=['GET'])
def assignmentInfo():
	json_load = request.get_json()
	courseID = json_load['courseId']

	assignment = user.get_Assignments(courseID)
	if assignment != -1:
		return jsonify(assignment), 200
	else:
		return jsonify(message = "No Material Found")


# @app.route("/api/grades", methods=['GET'])
# given: userId & courseId
# need: if userId is student, return grades (from grade book) of student for that course
#       else if userID is professor, return grades of all students for that course
@app.route("/api/grades", methods=['GET'])
def gradeInfo():
	json_load = request.get_json()
	userID = json_load['userId']
	courseID = json_load['courseId']

	# assignment = user.get_Assignments(courseID)
	# if assignment != -1:
	# 	return jsonify(assignment), 200
	# else:
	# 	return jsonify(message="No Material Found")


# @app.route("/api/submit_assign", methods=['POST'])
# given: userId, courseId, file (maybe more)
# need: update DB

# @app.route("/api/create_assign", methods=['POST'])
# given: userId, courseId, task, due date (maybe more)
# need: update DB

# @app.route("/api/create_material", methods=['POST'])
# given: courseId, file (maybe more)
# need: update DB

# @app.route("/api/assign_grade", methods=['POST'])
# given: studentId, assignId (maybe more)
# need: update DB

# @app.route("/api/create_gradebook", methods=['POST'])
# given: studentId, courseId, description (maybe more)
# need: update DB

if __name__ == "__main__":
	user = User()
	app.run()