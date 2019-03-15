from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, support_credentials=True)

# @app.route("/")
# def hello():
# 	return "Hello, World!"

@app.route("/auth/login", methods=['POST'])
def login():
	# TODO: need to check with DB
	return jsonify({
		'userID': 1,
		'userType': 0
	})

if __name__ == "__main__":
	app.run()