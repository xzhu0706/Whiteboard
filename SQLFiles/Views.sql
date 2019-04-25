DROP VIEW IF EXISTS compareAssignment;
DROP VIEW IF EXISTS compareExam;
DROP VIEW IF EXISTS assSubmit;
USE Whiteboard;

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

