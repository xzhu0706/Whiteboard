#!/usr/bin/env python
# If you don't have mysql.connect library
# Run `pip install mysql-connector` to install

import mysql.connector
from mysql.connector import errorcode
from InsertDB import *

config = {
    "user": 'jinchen',    # your mysql username
    "password": '19841036',  # your mysql password
    "host": '127.0.0.1',
}
# Set your own database name
database = 'Whiteboard'

def create_type(cursor,cnx):
    create_random_users(cursor, 50)
    create_random_courses(cursor, 5)
    create_random_takenClasses(cursor)
    create_random_assignment(cursor)
    # create_random_AssignmentGrade(cursor)
    cnx.commit()
    create_random_assignmentSubmission(cursor)
    create_random_exam(cursor)
    create_random_ExamGrade(cursor)
    create_random_classAnnouncement(cursor)
    create_random_classMaterials(cursor)

def parse_sql(filename):
    data = open(filename, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--') or line.startswith('#'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts


def executeScriptsFromFile(cnx, cursor,filename):
    # Open and read the file as a single buffer
    try:
        fd = open('./' + filename, 'r')
    except FileNotFoundError:
        fd = open('SQLFiles/' + filename, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')


    for command in sqlCommands:
        try:
            cursor.execute(command)
            cnx.commit()
        except mysql.connector.errors.ProgrammingError as err:
            print(err)

def executeBlock(cnx,cursor,filename):
    sqlCommands = parse_sql('SQLFiles/' + filename)

    for stmt in sqlCommands:
        cursor.execute(stmt, multi=True)
    cnx.commit()

def main():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(buffered=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise err


    # Initialize Table, Trigger, Procedure, View, Function
    # executeScriptsFromFile(cnx, cursor, 'ResetDB.sql')
    # executeScriptsFromFile(cnx, cursor, 'tableSchema.sql')
    # executeScriptsFromFile(cnx, cursor, 'Views.sql')
    # executeBlock(cnx, cursor, 'Triggers.sql')
    # cnx.commit()

    cursor.execute("CREATE DATABASE IF NOT EXISTS Whiteboard;")
    cursor.execute("USE Whiteboard;")

    create_type(cursor, cnx)

    # executeBlock(cnx, cursor, 'storefunctions.sql')
    # executeBlock(cnx, cursor, 'deleteProcedure.sql')
    # executeBlock(cnx, cursor, 'insertProcedure.sql')
    # executeBlock(cnx, cursor, 'getProcedure.sql')
    # cnx.commit()


    cnx.commit()  # Make sure data is committed to the database




if __name__ == "__main__":
    main()
