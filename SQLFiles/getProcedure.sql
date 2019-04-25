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

USE Whiteboard;

DELIMITER $$
  CREATE PROCEDURE getLogin(IN name VARCHAR(40),IN pw VARCHAR(40))
  BEGIN
    SELECT ID, userType, firstName, lastName
    FROM Users WHERE userName = name AND password= pw ;
  end $$
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
    SELECT professorID,courseName, semester,year, firstName,lastName,email
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
  CREATE PROCEDURE getAssGrade(IN cID INTEGER, IN uID INTEGER)
  BEGIN
    IF EXISTS(SELECT * FROM Users WHERE userType = 1 AND ID = uID)
      THEN SELECT studentID,assignmentID,title,gradeTotal,assGrade FROM compareassignment WHERE courseID = cID;
    ELSE
      SELECT assignmentID,title,gradeTotal,assGrade FROM compareassignment
      WHERE courseID = cID AND studentID = uID;
    END IF;
  end $$
DELIMITER ;

DELIMITER $$
  CREATE PROCEDURE getExGrade(IN cID INTEGER, IN uID INTEGER)
  BEGIN
    IF EXISTS(SELECT * FROM Users WHERE userType = 1 AND ID = uID)
      THEN SELECT examID, studentID, gradeTotal, examPercentage, description AS title,
                  examPerent/examPercentage*gradeTotal AS examGrade FROM compareexam
                  WHERE courseID = cID;
    ELSE SELECT examID, gradeTotal, examPercentage, description AS title,
                  examPerent/examPercentage*gradeTotal AS examGrade FROM compareexam
                  WHERE courseID = cID AND studentID = uID;
    END IF;
  end $$
DELIMITER ;

DELIMITER $$
  CREATE PROCEDURE getStudentInfo(IN cID INTEGER, IN sID INTEGER)
  BEGIN
    DECLARE finalG FLOAT;
    SET finalG = getFinalGrade(cID,sID);

    SELECT studentID, firstName, lastName, finalG AS finalGrade
    FROM Users JOIN TakenClasses ON ID = studentID WHERE courseID = cID AND studentID = sID;

  end $$
DELIMITER ;
-- CALL getStudentInfo(2,44)
-- SELECT firstName,lastName FROM Users WHERE ID = 1

