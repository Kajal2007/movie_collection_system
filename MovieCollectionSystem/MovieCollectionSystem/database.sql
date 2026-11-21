-- Movie Collection Management System: database setup
-- Run this file once in MySQL (Workbench or command line).

-- 1. Create the database
CREATE DATABASE IF NOT EXISTS movie_collection;

-- 2. Use the database
USE movie_collection;

-- 3. Create the movies table
CREATE TABLE IF NOT EXISTS movies (
    movie_id     INT AUTO_INCREMENT PRIMARY KEY,   -- unique id, generated automatically
    movie_name   VARCHAR(150) NOT NULL,            -- name of the movie
    genre        VARCHAR(50)  NOT NULL,            -- e.g. Action, Drama
    release_year INT          NOT NULL,            -- e.g. 2010
    rating       DECIMAL(3,1) NOT NULL,            -- 0.0 to 10.0
    language     VARCHAR(50)  NOT NULL             -- e.g. English, Hindi
);

-- 4. Optional sample data (so the page is not empty on first run)
INSERT INTO movies (movie_name, genre, release_year, rating, language) VALUES
('Inception', 'Sci-Fi', 2010, 8.8, 'English'),
('3 Idiots', 'Comedy', 2009, 8.4, 'Hindi'),
('The Dark Knight', 'Action', 2008, 9.0, 'English'),
('Baahubali: The Beginning', 'Action', 2015, 8.0, 'Telugu');

-- Handy queries used by the project (for reference)
-- SELECT * FROM movies ORDER BY movie_id DESC;
-- SELECT * FROM movies WHERE movie_name LIKE '%dark%';
