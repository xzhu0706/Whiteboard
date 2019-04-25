DROP PROCEDURE IF EXISTS addMaterial;
DROP PROCEDURE IF EXISTS addAnnouncement;
DROP PROCEDURE IF EXISTS addAssignment;
DROP PROCEDURE IF EXISTS addExam;
DROP PROCEDURE IF EXISTS addSubmission;
DROP PROCEDURE IF EXISTS gradeAssignment;
DROP PROCEDURE IF EXISTS gradeSubmission;
DROP PROCEDURE IF EXISTS gradeExam;
USE Whiteboard;

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