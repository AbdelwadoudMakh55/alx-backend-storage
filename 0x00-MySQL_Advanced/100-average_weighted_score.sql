-- Creating an SQL procedure that computes average weighted score
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN user_id INT)
BEGIN
	DECLARE avg_score FLOAT;
	SELECT SUM(projects.weight * corrections.score) / SUM(projects.weight)
	INTO avg_score
	FROM projects
	INNER JOIN corrections ON corrections.project_id = projects.id
	WHERE corrections.user_id = user_id;
	UPDATE users SET average_score = avg_score WHERE id = user_id;
END //
DELIMITER ;
