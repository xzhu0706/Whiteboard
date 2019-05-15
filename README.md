# Whiteboard

This is a simple version of CUNY Blackboard where students and instructors interact for courses. Instrucotrs are able to send announcements, upload materials and assignments, as well as grading assignments. Students are able to see announccements, materials, assignments, as well as submitting assignments. An estimated final grade will be calculated automatically based on the percentages the instructor assigned.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

- [Python3](https://www.python.org/downloads/)
- [NPM](https://www.npmjs.com/get-npm)
- [MariaDB](https://mariadb.org/)

### Installing

Clone and install packages and modules
```
git clone https://github.com/xzhu0706/Whiteboard.git
cd Whiteboard
npm install
pip3 install -r requirements.txt
```

Start the mysql server, then log in and run the AllScript.sql file
```
mysql -u <your username> -p<your password>
source AllScript.sql
```

Initialize the database by entering your localhost user and password in the CreateDB.py file, then run
```
python3 CreateDB.py
```

Start the frontend
```
npm start
```

Open up another terminal, start the backend by entering your localhost user and password in the run.py file, then run
```
python3 run.py
```

Go ahead to [http://localhost:3000](http://localhost:3000)

To log in, go to the database to check the usernames and passwords that were generated by the SQLControl.py file.

## Built With

* [React](https://reactjs.org/) - The JavaScript Library used for frontend
* [Flask](https://github.com/pallets/flask) - The web framework used
* [MariaDB](https://mariadb.org/) - The DBMS used
