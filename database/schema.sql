-- IAM Learning Platform Database Schema
-- MySQL 9.0 compatible

CREATE DATABASE IF NOT EXISTS iam_learning CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE iam_learning;

-- Users table for platform authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'instructor', 'admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Learning progress tracking
CREATE TABLE IF NOT EXISTS user_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    section_id INT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completion_date TIMESTAMP NULL,
    time_spent_seconds INT DEFAULT 0,
    quiz_score INT DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_progress (user_id, section_id)
);

-- Simulation execution logs
CREATE TABLE IF NOT EXISTS simulation_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    section_id INT NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT TRUE,
    output TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Audit log for compliance demonstration
CREATE TABLE IF NOT EXISTS audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    result ENUM('ALLOWED', 'DENIED', 'ERROR') NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Sample data
INSERT INTO users (username, email, password_hash, role) VALUES
('admin', 'admin@iam-learning.local', '$2b$12$N9qo8uLOickgx2ZMRZoMy.MqrqhmM6JGKpS4G3R1G2tUqXJXBz9C2', 'admin'),
('student', 'student@iam-learning.local', '$2b$12$N9qo8uLOickgx2ZMRZoMy.MqrqhmM6JGKpS4G3R1G2tUqXJXBz9C2', 'student');
