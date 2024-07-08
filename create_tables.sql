-- Create Reviews Table
CREATE TABLE IF NOT EXISTS reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    rating VARCHAR(255),
    review VARCHAR(255),
);
