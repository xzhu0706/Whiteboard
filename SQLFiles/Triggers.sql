USE Whiteboard;
DROP TRIGGER IF EXISTS assignmentTrigger;

-- Trigger for assignmentGrade when add to assignment
DELIMITER //
  CREATE TRIGGER assignmentTrigger AFTER INSERT ON Assignment
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
        INSERT INTO AssignmentGrade(assignmentID,studentID) VALUE (NEW.assignmentID,sID);
      end loop student_ass;
    CLOSE studentC;
  END; //
DELIMITER ;

