-- Create stored procedure ComputeAverageWeightedScoreForUser
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE avg_weighted_score FLOAT;
    SELECT SUM(score * weight) / SUM(weight) INTO avg_weighted_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE user_id = user_id;
    UPDATE users SET average_score = avg_weighted_score WHERE id = user_id;
END //
DELIMITER ;

