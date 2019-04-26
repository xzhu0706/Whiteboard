DROP FUNCTION IF EXISTS getFinalGrade;
USE Whiteboard;

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

-- SET @final = getFinalGrade(2,2);
-- SELECT @final;

-- SELECT SUM(assGrade)/COUNT(*) FROM compareAssignment WHERE courseID = 2 AND studentID = 46 AND assGrade is not NULL; -- 0.97
-- SELECT Sum(examPerent) FROM compareExam WHERE courseID = 2 AND studentID = 46; -- 24.7
-- SELECT assignmentPercentage FROM Courses WHERE courseID = 2; -- 30
-- SELECT SUM(examPercentage) FROM Exam WHERE courseID = 2; -- 54
