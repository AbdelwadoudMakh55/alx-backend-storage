-- Creating an SQL procedure that computes average weighted score
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
	UPDATE users
   	SET users.average_score = (
		SELECT SUM(projects.weight * corrections.score) / SUM(projects.weight)
		FROM projects
		INNER JOIN corrections ON corrections.project_id = projects.id
		WHERE corrections.user_id = users.id
	);
END //
DELIMITER ;
