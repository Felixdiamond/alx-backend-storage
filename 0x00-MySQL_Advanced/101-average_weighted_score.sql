-- Create stored procedure ComputeAverageWeightedScoreForUsers
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users
    JOIN (
        SELECT user_id, SUM(score * weight) / SUM(weight) AS avg_weighted_score
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        GROUP BY user_id
    ) AS subq ON users.id = subq.user_id
    SET users.average_score = subq.avg_weighted_score;
END //
DELIMITER ;

