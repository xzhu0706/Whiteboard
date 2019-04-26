DROP PROCEDURE IF EXISTS delMaterial;
DROP PROCEDURE IF EXISTS delAnnouncement;
DROP PROCEDURE IF EXISTS delAssignment;
DROP PROCEDURE IF EXISTS delExam;

USE Whiteboard;

-- Insert
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
