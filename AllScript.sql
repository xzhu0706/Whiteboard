CREATE DATABASE IF NOT EXISTS Whiteboard;
USE Whiteboard;

DROP TRIGGER IF EXISTS assignmentTrigger;
DROP PROCEDURE IF EXISTS getLogin;
DROP PROCEDURE IF EXISTS getCourses;
DROP PROCEDURE IF EXISTS courseInfo;
DROP PROCEDURE IF EXISTS materialInfo;
DROP PROCEDURE IF EXISTS announcementInfo;
DROP PROCEDURE IF EXISTS getAssignments;
DROP PROCEDURE IF EXISTS getSubmission;
DROP PROCEDURE IF EXISTS getAssGrade;
DROP PROCEDURE IF EXISTS getExGrade;
DROP PROCEDURE IF EXISTS getStudentInfo;

DROP PROCEDURE IF EXISTS addMaterial;
DROP PROCEDURE IF EXISTS addAnnouncement;
DROP PROCEDURE IF EXISTS addAnnouncement;
DROP PROCEDURE IF EXISTS addAssignment;
DROP PROCEDURE IF EXISTS addExam;
DROP PROCEDURE IF EXISTS addSubmission;
DROP PROCEDURE IF EXISTS gradeAssignment;
DROP PROCEDURE IF EXISTS gradeSubmission;
DROP PROCEDURE IF EXISTS gradeExam;

DROP PROCEDURE IF EXISTS delMaterial;
DROP PROCEDURE IF EXISTS delAnnouncement;
DROP PROCEDURE IF EXISTS delAssignment;
DROP PROCEDURE IF EXISTS delExam;

DROP FUNCTION IF EXISTS getFinalGrade;

DROP VIEW IF EXISTS compareAssignment;
DROP VIEW IF EXISTS compareExam;
DROP VIEW IF EXISTS assSubmit;

DROP TABLE IF EXISTS ClassAnnouncement,ClassMaterial,ExamGrade;
DROP TABLE IF EXISTS AssignmentSubmission,Exam;
DROP TABLE IF EXISTS AssignmentGrade;
DROP TABLE IF EXISTS Exam,Assignment;
DROP TABLE IF EXISTS TakenClasses;
DROP TABLE IF EXISTS Courses,Users;

-- DROP DATABASE IF EXISTS Whiteboard;
-- CREATE DATABASE IF NOT EXISTS Whiteboard;
-- USE Whiteboard;
DROP TABLE IF EXISTS ClassAnnouncement,ClassMaterial,ExamGrade;
DROP TABLE IF EXISTS AssignmentGrade, AssignmentSubmission,Exam;
DROP TABLE IF EXISTS Exam,Assignment,TakenClasses;
DROP TABLE IF EXISTS Courses,Users;

-- Tables
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


-- Views

CREATE VIEW compareAssignment AS(
    SELECT courseID, studentID,A.assignmentID,title, gradeTotal, assignmentGrade/gradeTotal AS assGrade
    FROM AssignmentGrade AG LEFT JOIN Assignment A
    ON  AG.assignmentID = A.assignmentID
);


CREATE VIEW compareExam AS (
  SELECT TakenClasses.courseID,ExamGrade.studentID, Exam.examID, gradeTotal, examPercentage, description,examPercentage*(examGrade/gradeTotal) AS examPerent
  FROM TakenClasses LEFT JOIN Exam
  ON TakenClasses.courseID = Exam.courseID
  LEFT JOIN ExamGrade ON Exam.examID = ExamGrade.examID
  AND ExamGrade.studentID = TakenClasses.studentID
);

CREATE VIEW assSubmit AS (
  SELECT A1.studentID, A.assignmentID, deadline,title, task,gradeTotal,postTime,submissionID, file, assignmentGrade,
         uploadTime,submissionID is not NULL AS isSubmitted, deadline < uploadTime AS isLate, deadline < postTime AS pastDue
  FROM AssignmentGrade A1 LEFT JOIN Assignment A ON A1.assignmentID = A.assignmentID
  LEFT JOIN AssignmentSubmission S ON A.assignmentID = S.assignmentID AND A1.studentID = S.studentID);



-- Trigger for assignmentGrade when add to assignment
DELIMITER //
  CREATE TRIGGER  assignmentTrigger AFTER INSERT ON Assignment
  FOR EACH ROW
  BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE sID INTEGER;
    DECLARE studentC CURSOR FOR
      SELECT studentID FROM TakenClasses
      WHERE courseID = NEW.courseID;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN studentC;
      student_ass: LOOP
        FETCH studentC INTO sID;
          IF done = 1 THEN
              LEAVE student_ass;
          END IF;
        INSERT INTO AssignmentGrade(assignmentID,studentID,gradeTime) VALUE (NEW.assignmentID,sID,NULL);
      end loop student_ass;
    CLOSE studentC;
  END;
DELIMITER ;

-- Trigger for examGrade when add to assignment
DELIMITER //
  CREATE TRIGGER  examTrigger AFTER INSERT ON Exam
  FOR EACH ROW
  BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE sID INTEGER;
    DECLARE studentC CURSOR FOR
      SELECT studentID FROM TakenClasses
      WHERE courseID = NEW.courseID;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    OPEN studentC;
      student_ass: LOOP
        FETCH studentC INTO sID;
          IF done = 1 THEN
              LEAVE student_ass;
          END IF;
        INSERT INTO ExamGrade(examID, studentID, examGrade) VALUE (NEW.examID,sID,NULL);
      end loop student_ass;
    CLOSE studentC;
  END;
DELIMITER ;

-- Trigger for update final grade when insert assignment grade
DELIMITER //
  CREATE TRIGGER gradeTrigger AFTER UPDATE ON AssignmentGrade
    FOR EACH ROW
    BEGIN
      DECLARE finalG FLOAT;
      DECLARE cID INTEGER;
      SELECT courseID INTO cID FROM Assignment WHERE Assignment.assignmentID = NEW.assignmentID;
      SET finalG = getFinalGrade(cID, NEW.studentID);
    end //
DELIMITER ;

-- Trigger for update final grade when insert exam grade
DELIMITER //
  CREATE TRIGGER examUpdateTrigger AFTER UPDATE ON ExamGrade
    FOR EACH ROW
    BEGIN
      DECLARE finalG FLOAT;
      DECLARE cID INTEGER;
      SELECT courseID INTO cID FROM Exam WHERE Exam.examID = NEW.examID;
      SET finalG = getFinalGrade(cID, NEW.studentID);
    end //
DELIMITER ;

DELIMITER //
  CREATE TRIGGER examInsertTrigger AFTER INSERT ON ExamGrade
    FOR EACH ROW
    BEGIN
      DECLARE finalG FLOAT;
      DECLARE cID INTEGER;
      SELECT courseID INTO cID FROM Exam WHERE Exam.examID = NEW.examID;
      SET finalG = getFinalGrade(cID, NEW.studentID);
    end //
DELIMITER ;

-- function for update final grade
DELIMITER //
CREATE FUNCTION getFinalGrade(cID INTEGER,sID INTEGER) RETURNS FLOAT
BEGIN
  DECLARE assPer INTEGER;
  DECLARE assTotal FLOAT;
  DECLARE examPer INTEGER;
  DECLARE examTotal FLOAT;
  DECLARE finalGrade FLOAT;

  SELECT assignmentPercentage INTO assPer FROM Courses WHERE courseID = cID;
  SELECT SUM(examPercentage) INTO examPer FROM compareExam
  WHERE courseID = cID AND studentID = sID AND examPerent is not NULL;

  -- RETURN examPer;
  SELECT SUM(assGrade)/COUNT(*) INTO assTotal FROM compareAssignment
  WHERE courseID = cID AND studentID = sID AND assGrade is not NULL;

  SELECT Sum(examPerent) INTO examTotal FROM compareExam
  WHERE courseID = cID AND studentID = sID AND examPerent is not NULL;

  IF assTotal IS NULL AND examTotal IS NULL THEN RETURN -1;
  ELSEIF assTotal IS NULL
    THEN SET finalGrade = examTotal/examPer*100;
  ELSEIF examTotal IS NULL
    THEN SET finalGrade = assTotal * 100;
  ELSE
    SET finalGrade = (examTotal+assTotal*assPer)/(assPer+examPer)*100;
  END IF ;

  UPDATE TakenClasses SET estFinalGrade = finalGrade
  WHERE courseID = cID AND studentID = sID;
  RETURN finalGrade;
end //
DELIMITER ;

-- Delete
DELIMITER $$
  CREATE PROCEDURE delMaterial(IN mID INTEGER)
  BEGIN
    DELETE FROM ClassMaterial where materialID = mID;
  end $$
DELIMITER ;


DELIMITER $$
  CREATE PROCEDURE delAnnouncement(IN annID INTEGER)
  BEGIN
    DELETE FROM ClassAnnouncement where announcementID =  annID;
  end $$
DELIMITER ;


DELIMITER $$
  CREATE PROCEDURE delAssignment(IN assID INTEGER)
  BEGIN
    DELETE FROM Assignment where assignmentID = assID;
  end $$
DELIMITER ;


DELIMITER $$
  CREATE PROCEDURE delExam(IN eID INTEGER)
  BEGIN
    DELETE FROM Exam where examID = eID;
  end $$
DELIMITER ;


-- Insert
DELIMITER $$
  CREATE PROCEDURE addMaterial(IN cID INTEGER,IN content VARCHAR(256))
  BEGIN
    INSERT INTO ClassMaterial (courseID,material) VALUES (cID, content);
  end $$
DELIMITER ;

DELIMITER $$
  CREATE PROCEDURE addAnnouncement(IN cID INTEGER,IN content VARCHAR(256))
  BEGIN
    INSERT INTO ClassAnnouncement (courseID,announcement) VALUES (cID, content);
  end $$
DELIMITER ;


DELIMITER $$
  CREATE PROCEDURE addAssignment(IN cID INTEGER,IN due TIMESTAMP,
                                  IN tit VARCHAR(40), IN tas VARCHAR(256), IN gtotal INTEGER)
  BEGIN
    INSERT INTO Assignment (courseID,deadline,title, task,gradeTotal)
    VALUES (cID, due,tit,tas,gtotal);
  end $$
DELIMITER ;

DELIMITER $$
  CREATE PROCEDURE addExam(IN cID INTEGER,IN des VARCHAR(128), IN gTotal INTEGER, IN percent INTEGER)
  BEGIN
    INSERT INTO Exam(courseID,gradeTotal,description,examPercentage)
    VALUES (cID, gTotal,des,percent);
  end $$
DELIMITER ;

DELIMITER $$
  CREATE PROCEDURE addSubmission(IN aID INTEGER,IN sID INTEGER, IN content VARCHAR(256))
  BEGIN
    INSERT INTO AssignmentSubmission(studentID,assignmentID,file)
    VALUES (sID, aID,content);
  end $$
DELIMITER ;


-- Grade Assignment
DELIMITER $$
  CREATE PROCEDURE gradeAssignment(IN aID INTEGER, IN sID INTEGER, IN grade FLOAT)
  BEGIN
    UPDATE AssignmentGrade SET AssignmentGrade = grade
    WHERE assignmentID = aID AND studentID = sID;
  end $$
DELIMITER ;


-- Grade Submission
DELIMITER $$
  CREATE PROCEDURE gradeSubmission(IN subID INTEGER, IN grade FLOAT)
  BEGIN
      DECLARE sID INTEGER;
      DECLARE aID INTEGER;
      DECLARE subInfo CURSOR FOR
        SELECT studentID, assignmentID FROM AssignmentSubmission
        WHERE submissionID = subID;

      OPEN subInfo;
      FETCH subInfo into sID, aID;
      UPDATE AssignmentGrade SET AssignmentGrade = grade
        WHERE assignmentID = aID AND studentID = sID;
      CLOSE subInfo;
  end $$
DELIMITER ;
-- call gradeSubmission(1, 70)

-- Grade Exam
DELIMITER $$
  CREATE PROCEDURE gradeExam(IN sID INTEGER,IN eID INTEGER, IN grade FLOAT)
  BEGIN
    IF EXISTS(SELECT * FROM ExamGrade WHERE examID=eID AND studentID=sID)
      THEN UPDATE ExamGrade SET examGrade = grade
            WHERE examID=eID AND studentID=sID;
    ELSE INSERT INTO ExamGrade(examID, studentID, examGrade)
        VALUES (eID,sID,grade);
    END IF;
  end $$
DELIMITER ;
-- call gradeExam(46,3,90)


-- Get Procedure
DELIMITER $$
  CREATE PROCEDURE getLogin(IN name VARCHAR(40),IN pw VARCHAR(40))
  BEGIN
    SELECT ID, userType, firstName, lastName
    FROM Users WHERE userName = name AND password= pw ;
  end; $$
DELIMITER ;
-- CALL Login('Ada386','yph8v87cag');

DELIMITER $$
  CREATE PROCEDURE getCourses(IN userID INTEGER)
  BEGIN
    IF EXISTS(SELECT * FROM Users
      WHERE userType=1 AND ID = userID)
      THEN SELECT courseID, courseName,semester,year
                            FROM Courses WHERE professorID = userID
                            ORDER BY year ASC,semester DESC;
    ELSEIF EXISTS(SELECT * FROM Users
      WHERE userType=0 AND ID = userID)
      THEN SELECT courseID, courseName,semester,year
            FROM Courses NATURAL JOIN TakenClasses
              WHERE studentID = userID ORDER BY year ASC,semester DESC;
    End If;
  end $$
DELIMITER ;
-- Call getCourses(5)

DELIMITER $$
  CREATE PROCEDURE courseInfo(IN cID INTEGER)
  BEGIN
    SELECT professorID,courseID,courseName, semester,year, firstName,lastName,email
      FROM Users JOIN Courses ON Users.ID = Courses.professorID
    WHERE courseID = cID ORDER BY year ASC,semester DESC;
  end $$
DELIMITER ;

-- Call courseInfo(2)

DELIMITER $$
  CREATE PROCEDURE materialInfo(IN cID INTEGER)
  BEGIN
    SELECT materialID, material,postTime
      FROM ClassMaterial WHERE courseID = cID
    ORDER BY materialID DESC;
  end $$
DELIMITER ;
-- Call materialInfo(2);

DELIMITER $$
  CREATE PROCEDURE announcementInfo(IN cID INTEGER)
  BEGIN
    SELECT announcementID, announcement,postTime
      FROM ClassAnnouncement WHERE courseID = cID
    ORDER BY announcementID DESC;
  end $$
DELIMITER ;
-- CALL announcementInfo(2);



-- def get_Assignments
DELIMITER $$
  CREATE PROCEDURE getAssignments(IN cID INTEGER, IN userID INTEGER)
  BEGIN
    IF EXISTS(SELECT * FROM Users WHERE userType = 1 AND ID = userID)
    THEN SELECT assignmentID, deadline,title, task,gradeTotal,postTime, deadline<CURRENT_TIMESTAMP AS pastDue
         FROM Assignment WHERE courseID = cID;
    ELSE SELECT assignmentID,deadline,title, task,gradeTotal,postTime,
                pastDue, isLate,isSubmitted FROM assSubmit WHERE studentID =userID;
    END IF ;
  end $$
DELIMITER ;
-- CALL getAssignments(1,3);



-- def get_submission
DELIMITER $$
  CREATE PROCEDURE getSubmission(IN aID INTEGER)
  BEGIN
    SELECT studentID, submissionID,file, gradeTotal, uploadTime, firstName, lastName,assignmentGrade,
    pastDue, isSubmitted, isLate, assignmentGrade is not NULL as isGraded
    FROM asssubmit A LEFT JOIN Users U ON A.studentID = U.ID
      WHERE a.assignmentID = aID ORDER BY U.lastName ASC;
  end $$
DELIMITER ;
-- CALL getSubmission(1)


-- def   get_grades
DELIMITER $$
  CREATE PROCEDURE getGrade(IN cID INTEGER, IN uID INTEGER)
  BEGIN
    IF EXISTS(SELECT * FROM Users WHERE userType = 0 AND ID = uID)
      THEN
        SELECT U.ID,firstName,lastName,estFinalGrade, assignmentPercentage FROM Users U
          JOIN TakenClasses T ON U.ID =T.studentID AND U.ID = uID
          JOIN Courses ON T.courseID = Courses.courseID;

        SELECT assignmentID,title,gradeTotal,assGrade*gradeTotal FROM compareassignment
        WHERE courseID = cID AND studentID = uID;

        SELECT examID, gradeTotal, examPercentage, description AS title,
        examPerent/examPercentage*gradeTotal AS examGrade FROM compareexam
        WHERE courseID = cID AND studentID = uID;


    ELSE
      SELECT U.ID,firstName,lastName,estFinalGrade,assignmentPercentage FROM Users U
          JOIN TakenClasses T ON U.ID =T.studentID AND T.courseID = cID
          JOIN Courses ON T.courseID = Courses.courseID ORDER BY U.ID ASC ;

      SELECT studentID,assignmentID,title,gradeTotal,assGrade*gradeTotal FROM compareassignment
      WHERE courseID = cID ORDER BY studentID ASC ;

      SELECT examID, studentID, gradeTotal, examPercentage, description AS title,
                        examPerent/examPercentage*gradeTotal AS examGrade FROM compareexam
                        WHERE courseID = cID and studentID is not NULL ORDER BY studentID ASC;
    end if;
  end $$
DELIMITER ;
-- CALL getGrade(1,10);



