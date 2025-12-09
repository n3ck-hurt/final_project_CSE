CREATE DATABASE IF NOT EXISTS cse_final_project;
USE cse_final_project;

CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    major VARCHAR(120) NOT NULL,
    gpa DECIMAL(3,2) NOT NULL DEFAULT 0.00
);

INSERT INTO students (name, email, major, gpa) VALUES
('Alice Johnson', 'alice.johnson@example.com', 'Computer Science', 3.85),
('Brian Smith', 'brian.smith@example.com', 'Information Systems', 3.70),
('Carla Gomez', 'carla.gomez@example.com', 'Software Engineering', 3.92),
('Darius Lee', 'darius.lee@example.com', 'Data Science', 3.65),
('Emily Chen', 'emily.chen@example.com', 'Cybersecurity', 3.88),
('Farah Patel', 'farah.patel@example.com', 'Computer Engineering', 3.55),
('Gina Rossi', 'gina.rossi@example.com', 'Information Systems', 3.40),
('Hector Ramirez', 'hector.ramirez@example.com', 'Computer Science', 3.25),
('Isabella Cruz', 'isabella.cruz@example.com', 'Data Science', 3.95),
('Jamal White', 'jamal.white@example.com', 'Software Engineering', 3.60),
('Kara Nguyen', 'kara.nguyen@example.com', 'Computer Science', 3.45),
('Luis Fernandez', 'luis.fernandez@example.com', 'Cybersecurity', 3.75),
('Maya Singh', 'maya.singh@example.com', 'Information Systems', 3.15),
('Noah Brown', 'noah.brown@example.com', 'Data Science', 3.30),
('Olivia Davis', 'olivia.davis@example.com', 'Computer Engineering', 3.10),
('Priya Shah', 'priya.shah@example.com', 'Software Engineering', 3.67),
('Quinn Baker', 'quinn.baker@example.com', 'Computer Science', 3.28),
('Rita Morales', 'rita.morales@example.com', 'Cybersecurity', 3.82),
('Samir Ali', 'samir.ali@example.com', 'Information Systems', 3.48),
('Tina Brooks', 'tina.brooks@example.com', 'Data Science', 3.58);


