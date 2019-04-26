USE Whiteboard;
DROP TRIGGER IF EXISTS assignmentTrigger;
DROP TRIGGER IF EXISTS examTrigger;
DROP TRIGGER IF EXISTS gradeTrigger;
DROP TRIGGER IF EXISTS examUpdateTrigger;
DROP TRIGGER IF EXISTS examInsertTrigger;


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

-- INSERT INTO ExamGrade (examID, studentID, examGrade) VALUES (2,5,80)
