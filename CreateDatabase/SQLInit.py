
def init(cursor,type):
    if type == "Users":
        cursor.execute("DROP TABLE IF EXISTS Users;")
        cursor.execute("CREATE TABLE Users("
                       "ID INTEGER PRIMARY KEY AUTO_INCREMENT, "
                       "userName VARCHAR(128) NOT NULL UNIQUE,"
                       "password VARCHAR(128) NOT NULL,"
                       "email VARCHAR(128), "
                       "firstName VARCHAR(128), "
                       "lastName VARCHAR(128),"
                       "userType INTEGER NOT NULL);")
    elif type == "Courses":
        cursor.execute("DROP TABLE IF EXISTS Courses;")
        cursor.execute("CREATE TABLE Courses("
                       "coursesID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "courseName VARCHAR(128),"
                       "semester VARCHAR(128), "
                       "year INTEGER, "
                       "professorID INTEGER,"
                       "FOREIGN KEY (professorID) REFERENCES Users(ID));")
    elif type =="TakenClasses":
        cursor.execute("DROP TABLE IF EXISTS TakenClasses;")
        cursor.execute("CREATE TABLE TakenClasses("
                       "studentID INTEGER,"
                       "coursesID INTEGER,"
                       "grade FLOAT NOT NULL, "
                       "PRIMARY KEY (studentID,coursesID),"
                       "FOREIGN KEY (studentID) REFERENCES Users(ID),"
                       "FOREIGN KEY (coursesID) REFERENCES Courses(coursesID));")
    elif type == "Assignment":
        cursor.execute("DROP TABLE IF EXISTS Assignment;")
        cursor.execute("CREATE TABLE Assignment("
                       "AssignID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "coursesID INTEGER,"
                       "deadline TIMESTAMP, "
                       "task VARCHAR(256), "
                       "gradeTotal INTEGER,"
                       "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       # "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "FOREIGN KEY (coursesID) REFERENCES Courses(coursesID));")
    elif type == "AssignmentSubmission":
        cursor.execute("DROP TABLE IF EXISTS AssignmentSubmission;")
        cursor.execute("CREATE TABLE AssignmentSubmission("
                       "submissionID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "studentID INTEGER NOT NULL,"
                       "assignID INTEGER NOT NULL,"
                       "isGraded INTEGER,"
                       "file VARCHAR(256), "
                       "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       # "PRIMARY KEY (submissionID,studentID),"
                       "FOREIGN KEY (studentID) REFERENCES Users(ID),"
                       "FOREIGN KEY (assignID) REFERENCES Assignment(assignID));")
    elif type == "GradeBook":
        cursor.execute("DROP TABLE IF EXISTS GradeBook;")
        cursor.execute("CREATE TABLE GradeBook("
                       "gradeID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "StudentID INTEGER,"
                       "coursesID INTEGER,"
                       "submissionID INTEGER,"
                       "description VARCHAR(128), "
                       "grade INTEGER,"
                       "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "FOREIGN KEY (submissionID) REFERENCES AssignmentSubmission(submissionID),"
                       "FOREIGN KEY (studentID,coursesID) REFERENCES TakenClasses(studentID,coursesID));")
    elif type == "ClassAnnouncement":
        cursor.execute("DROP TABLE IF EXISTS ClassAnnouncement;")
        cursor.execute("CREATE TABLE ClassAnnouncement("
                       "announcementID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "coursesID INTEGER,"
                       "announcement VARCHAR(256), "
                       "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "FOREIGN KEY (coursesID) REFERENCES Courses(coursesID));")

    elif type == "ClassMaterials":
        cursor.execute("DROP TABLE IF EXISTS ClassMaterials;")
        cursor.execute("CREATE TABLE ClassMaterials("
                       "materialID INTEGER PRIMARY KEY AUTO_INCREMENT,"
                       "coursesID INTEGER,"
                       "material VARCHAR(256), "
                       "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
                       "FOREIGN KEY (coursesID) REFERENCES Courses(coursesID));")
    else:
        print(f"Unknown Typle : {type}")


















