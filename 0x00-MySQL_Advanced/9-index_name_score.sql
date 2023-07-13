-- Create index idx_name_first_score on names table
CREATE INDEX idx_name_first_score ON names (name(1), score);

