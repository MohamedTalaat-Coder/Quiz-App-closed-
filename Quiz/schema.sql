DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password CHAR(255) NOT NULL
);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Question VARCHAR(255) UNIQUE NOT NULL,
    Answer VARCHAR(255) NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id)
);