-- Create the database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS rms_dev_db;

-- Create the user if it doesn't already exist, with the specified password
CREATE USER IF NOT EXISTS 'rms_dev'@'localhost' IDENTIFIED BY 'Rms_dev_pwd1!';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON `rms_dev_db`.* TO 'rms_dev'@'localhost';

-- Optionally, grant SELECT privileges on the performance_schema for monitoring purposes
GRANT SELECT ON `performance_schema`.* TO 'rms_dev'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;
