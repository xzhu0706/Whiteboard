def init(cursor,database):
    cursor.execute("CREATE DATABASE IF NOT EXISTS %s;" % database)
    cursor.execute("USE %s;" % database)

    cursor.execute("CREATE TABLE Users("
                   "ID INTEGER PRIMARY KEY AUTO_INCREMENT, "
                   "userName VARCHAR(40) NOT NULL UNIQUE, "
                   "password VARCHAR(40) NOT NULL, "
                   "email VARCHAR(80), "
                   "firstName VARCHAR(40), "
                   "lastName VARCHAR(40),"
                   "userType INTEGER NOT NULL);")
    cursor.execute("CREATE TABLE Courses( "
                   "courseID INTEGER PRIMARY KEY AUTO_INCREMENT, "
                   "courseName VARCHAR(40), "
                   "semester VARCHAR(40),"
                   "year INTEGER,"
                   "professorID INTEGER,"
                   "FOREIGN KEY (professorID) REFERENCES Users(ID)"
                   ");")
    cursor.execute("CREATE TABLE TakenClasses("
                       "studentID INTEGER,"
                       "courseID INTEGER,"
                       "grade FLOAT, "
                       "PRIMARY KEY (studentID,courseID),"
                       "FOREIGN KEY (studentID) REFERENCES Users(ID),"
                       "FOREIGN KEY (courseID) REFERENCES Courses(courseID));")
    cursor.execute("CREATE TABLE Assignment("
                       "assignID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "courseID INTEGER,"
                       "deadline TIMESTAMP, "
                       "task VARCHAR(256), "
                       "gradeTotal INTEGER,"
                       "postTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "FOREIGN KEY (courseID) REFERENCES Courses(courseID) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE AssignmentSubmission("
                       "submissionID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "studentID INTEGER,"
                       "assignID INTEGER,"
                       "isGraded INTEGER,"
                       "file VARCHAR(256), "
                       "uploadTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "FOREIGN KEY (studentID) REFERENCES Users(ID),"
                       "FOREIGN KEY (assignID) REFERENCES Assignment(assignID));")
    cursor.execute("CREATE TABLE Exam("
                       "examID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "courseID INTEGER,"
                       "gradeTotal INTEGER,"
                       "description VARCHAR(128),"
                       "examDay TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "FOREIGN KEY (courseID) REFERENCES Courses(courseID));")

    cursor.execute("CREATE TABLE GradeBook("
                       "gradeID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "StudentID INTEGER,"
                       "examID INTEGER,"
                       "submissionID INTEGER,"
                       "grade FLOAT,"
                       "gradeTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "FOREIGN KEY (submissionID) REFERENCES AssignmentSubmission(submissionID),"
                       "FOREIGN KEY (studentID) REFERENCES Users(ID),"
                       "FOREIGN KEY (examID) REFERENCES Exam(examID));")

    cursor.execute("CREATE TABLE ClassAnnouncement("
                       "announcementID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "courseID INTEGER,"
                       "announcement VARCHAR(256), "
                       "postTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "FOREIGN KEY (courseID) REFERENCES Courses(courseID));")

    cursor.execute("CREATE TABLE ClassMaterials("
                       "materialID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "courseID INTEGER,"
                       "material VARCHAR(256), "
                       "postTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "FOREIGN KEY (courseID) REFERENCES Courses(courseID));")



















