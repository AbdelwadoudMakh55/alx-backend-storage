-- Create VIEW
CREATE VIEW need_meeting AS
SELECT name 
FROM students
WHERE score < 80 AND (last_meeting IS NULL OR MONTH(CURDATE()) - MONTH(last_meeting) > 1 OR YEAR(CURDATE()) > YEAR(last_meeting));
