#!/usr/bin/env python
# If you don't have mysql.connect library
# Run `pip install mysql-connector` to install

import mysql.connector
from mysql.connector import errorcode
from SQLInit import init
from SQLCreate import *
from SQLQuery import *

config = {
    "user": '',    # your mysql username
    "password": '',  # your mysql password
    "host": '127.0.0.1',
}
# Set your own database name
database = 'Whiteboard'

def create_type(cursor,cnx):
    create_random_users(cursor, 50)
    # cnx.commit()
    create_random_courses(cursor, 5)
    # cnx.commit()
    create_random_takenClasses(cursor)
    # cnx.commit()
    create_random_assignment(cursor)
    # cnx.commit()
    create_random_AssignmentGrade(cursor)
    cnx.commit()
    create_random_assignmentSubmission(cursor)
    # cnx.commit()
    create_random_exam(cursor)
    # cnx.commit()
    create_random_ExamGrade(cursor)
    # cnx.commit()
    create_random_classAnnouncement(cursor)
    # cnx.commit()
    create_random_classMaterials(cursor)
    # cnx.commit()



def query_type(cursor):
    query_users(cursor)
    query_courses(cursor)
    query_takenClasses(cursor)
    query_assignment(cursor)
    query_assignmentSubmission(cursor)
    query_exam(cursor)
    query_classAnnouncement(cursor)
    query_classMaterials(cursor)



def main(argv,database):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(buffered=True)
        if argv == "init":
            print("init")
            init(cursor, database)
            cnx.commit()        # Make sure data is committed to the database
        elif argv == "create":
            print("create")
            cursor.execute("USE %s;" % database)
            create_type(cursor,cnx)
            cnx.commit()            # Make sure data is committed to the database
        elif argv == "query":
            print("query")
            cursor.execute("USE %s;" % database)
            query_type(cursor)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise err
    else:
        cnx.close()




action = ["init", "create","query","deleteDB"]


# init database and all table:
main(action[0],database)


# Create Table
main(action[1],database)


# Query from Database
main(action[2], database)

