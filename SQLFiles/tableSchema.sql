-- DROP DATABASE IF EXISTS Whiteboard;
CREATE DATABASE IF NOT EXISTS Whiteboard;
USE Whiteboard;
DROP TABLE IF EXISTS ClassAnnouncement,ClassMaterial,ExamGrade;
DROP TABLE IF EXISTS AssignmentGrade, AssignmentSubmission,Exam;
DROP TABLE IF EXISTS Exam,Assignment,TakenClasses;
DROP TABLE IF EXISTS Courses,Users;


CREATE TABLE Users(
  ID       INTEGER PRIMARY KEY AUTO_INCREMENT,
  userName VARCHAR(40) NOT NULL UNIQUE,
  password VARCHAR(40) NOT NULL,
  email VARCHAR(80),
  firstName VARCHAR(40),
  lastName VARCHAR(40),
  userType INTEGER NOT NULL
);

CREATE TABLE Courses(
  courseID INTEGER PRIMARY KEY AUTO_INCREMENT,
  courseName VARCHAR(40),
  semester VARCHAR(40),
  year INTEGER,
  professorID INTEGER,
  assignmentPercentage INTEGER,
  FOREIGN KEY (professorID) REFERENCES Users(ID));


CREATE TABLE TakenClasses(
  studentID INTEGER,
  courseID INTEGER,
  estFinalGrade FLOAT,
  PRIMARY KEY (studentID,courseID),
  FOREIGN KEY (studentID) REFERENCES Users(ID),
  FOREIGN KEY (courseID) REFERENCES Courses(courseID));

CREATE TABLE Assignment(
  assignmentID INTEGER PRIMARY KEY AUTO_INCREMENT,
  courseID INTEGER,
  deadline TIMESTAMP,
  title VARCHAR(40),
  task VARCHAR(256),
  gradeTotal INTEGER,
  postTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (courseID) REFERENCES Courses(courseID));

CREATE TABLE AssignmentGrade(
  assignmentID INTEGER,
  studentID INTEGER,
  assignmentGrade FLOAT,
  gradeTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (assignmentID, studentID),
  FOREIGN KEY (studentID) REFERENCES TakenClasses(studentID),
  FOREIGN KEY (assignmentID) REFERENCES Assignment(assignmentID) ON DELETE CASCADE );

CREATE TABLE AssignmentSubmission(
  submissionID INTEGER PRIMARY KEY AUTO_INCREMENT,
  assignmentID INTEGER,
  studentID INTEGER,
  file VARCHAR(256),
  uploadTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (assignmentID, studentID)
    REFERENCES AssignmentGrade(assignmentID, studentID) ON DELETE CASCADE);

CREATE TABLE Exam(
  examID INTEGER PRIMARY KEY AUTO_INCREMENT,
  courseID INTEGER,
  gradeTotal INTEGER,
  description VARCHAR(128),
  examPercentage INTEGER,
  postTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (courseID) REFERENCES Courses(courseID));

CREATE TABLE ExamGrade(
  examID INTEGER,
  studentID INTEGER,
  examGrade FLOAT,
  gradeTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  primary key (examID,studentID),
  FOREIGN KEY (examID) REFERENCES Exam(examID) ON DELETE CASCADE,
  FOREIGN KEY (studentID) REFERENCES TakenClasses(studentID));

CREATE TABLE ClassAnnouncement(
  announcementID INTEGER PRIMARY KEY AUTO_INCREMENT,
  courseID INTEGER,
  announcement VARCHAR(256),
  postTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (courseID) REFERENCES Courses(courseID)
);

CREATE TABLE ClassMaterial(
  materialID INTEGER PRIMARY KEY AUTO_INCREMENT,
  courseID INTEGER,
  material VARCHAR(256),
  postTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (courseID) REFERENCES Courses(courseID)
);
