SET NAMES utf8mb4;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS team_rocket_project;
CREATE SCHEMA team_rocket_project;
USE team_rocket_project;

CREATE TABLE `team_rocket_project`.`staff` (
	`Staff_ID` VARCHAR(45) NOT NULL,
 	`First_Name` VARCHAR(45) NOT NULL,
 	`Last_Name` VARCHAR(45) NOT NULL,
 	`Address` VARCHAR(45) NULL,
 	`Postcode` VARCHAR(45) NULL,
 	`Phone_Number` VARCHAR(45) NULL,
 	`DTH-Skill` ENUM('Yes', 'No'),
 	`BB_Skill` ENUM('Yes', 'No'),
 	`SE_Skill` ENUM('Yes', 'No'),
 	`MDU_Skill` ENUM('Yes', 'No'),
 	`FTTP_Skilll` ENUM('Yes', 'No'),
    `Admin` ENUM('Yes', 'No'),
   	`Password` VARCHAR(45) NULL,   
 	PRIMARY KEY (`Staff_ID`));
  
CREATE TABLE `team_rocket_project`.`Jobs` (
    `Job_ID` INT AUTO_INCREMENT NOT NULL,
    `Customer_Last_Name` VARCHAR(45),
    `Address` VARCHAR(45),
    `Postcode` VARCHAR(45),
    `Phone_Number` VARCHAR(45),
    `Visit_Type` ENUM('DTH', 'BB', 'SE', 'MDU', 'FTTP'),
    `Staff_ID` VARCHAR(45),
    `Job_Date` DATE,
    `Start_Time` TIMESTAMP,
    `End_Time` TIMESTAMP,
    `Is_Not_Done` ENUM('Yes', 'No'),
    PRIMARY KEY (`Job_ID`),
    FOREIGN KEY (`Staff_ID`) REFERENCES `staff` (`Staff_ID`)
);

INSERT INTO staff VALUES
('JWI12', 'James', 'Wilson', 'Main Street', 'ML11 8EZ', '07341829218', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'Password'),
('STE01', 'Steven', 'Henderson', 'Back Street', 'ML1 8EQ', '07341658218', 'No', 'No', 'No', 'No', 'No', 'Yes', 'Password'),
('ABC01', 'James', 'Jone', 'North Street', 'ML1 8QT', '07341658218', 'No', 'No', 'No', 'No', 'No', 'Yes', 'Password'),
('ABC02', 'George', 'Wylie', 'South Street', 'ML1 8FT', '07341658218', 'No', 'No', 'No', 'No', 'No', 'Yes', 'Password'),
('ABC03', 'Jade', 'Samson', 'East Street', 'ML1 8ED', '07341658218', 'Yes', 'Yes', 'No', 'No', 'No', 'No', 'Password'),
('ABC04', 'Jordan', 'Jones', 'West Street', 'ML1 8ED', '07341658218', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'Password'),
('ABC05', 'Kriss', 'Jobs', 'Back Road', 'ML1 8VT', '07341658218', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'Password'),
('ABC06', 'Susan', 'Boyle', 'Back Lane', 'ML1 8BT', '07341658218', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Password'),
('ABC07', 'David', 'Davidson', 'Back End', 'ML1 8EG', '07341658218', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'Password'),
('ABC08', 'William', 'Williamson', 'Back Avenue', 'ML1 9ET', '07341658218', 'Yes', 'Yes', 'No', 'No', 'No', 'No', 'Password'),
('ABC09', 'Sarah', 'MacDonald', 'High Street', 'ML1 7XY', '07341658218', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Password'),
('ABC10', 'Andrew', 'McLeod', 'Low Street', 'ML1 6YZ', '07341658218', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Password'),
('ABC11', 'Karen', 'MacKenzie', 'Market Street', 'ML1 5WV', '07341658218', 'No', 'Yes', 'No', 'No', 'No', 'No', 'Password'),
('ABC12', 'Stephen', 'Graham', 'Station Road', 'ML1 4TU', '07341658218', 'No', 'No', 'Yes', 'No', 'No', 'No', 'Password'),
('ABC13', 'Laura', 'Murray', 'Church Lane', 'ML1 3SR', '07341658218', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'Password'),
('ABC15', 'Rebecca', 'Campbell', 'River View', 'ML1 1NO', '07341658218', 'Yes', 'No', 'No', 'Yes', 'No', 'No', 'Password'),
('ABC16', 'Michael', 'Scott', 'Castle Street', 'ML2 9MN', '07341658218', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'Password'),
('ABC17', 'Nicole', 'Stewart', 'Park Avenue', 'ML2 8LK', '07341658218', 'Yes', 'No', 'Yes', 'No', 'No', 'No', 'Password'),
('ABC18', 'Daniel', 'Black', 'Meadow Lane', 'ML2 7IJ', '07341658218', 'No', 'No', 'Yes', 'No', 'No', 'No', 'Password'),
('ABC19', 'Emma', 'Robertson', 'Sunset Drive', 'ML2 6HG', '07341658218', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'Password'),
('ABC20', 'John', 'Reid', 'Hillside Road', 'ML2 5EF', '07341658218', 'Yes', 'No', 'No', 'No', 'Yes', 'No', 'Password');


INSERT INTO Jobs (`Customer_Last_Name`, `Address`, `Postcode`, `Phone_Number`, `Visit_Type`, `Job_Date`, `Start_Time`, `End_Time`)
VALUES
('Smith', '5 Main Road', 'ML11 1AA', '01555 123 456', 'DTH', '2023-05-16', NULL, NULL),
('Wilson', '10 High Street', 'ML1 1AB', '01555 456 456', 'DTH', '2023-05-16', NULL, NULL),
('Anderson', '20 Blue Wynd', 'ML12 3BC', '01555 987 456', 'DTH', '2023-05-16', NULL, NULL),
('Johnson', '30 Park Avenue', 'AB12 3CD', '01234 567 890', 'BB', '2023-05-16', NULL, NULL),
('Brown', '40 Elm Street', 'EF34 5GH', '02345 678 901', 'SE', '2023-05-16', NULL, NULL),
('Davis', '50 Maple Road', 'IJ56 7KL', '03456 789 012', 'MDU', '2023-05-16', NULL, NULL),
('Taylor', '60 Oak Avenue', 'MN78 9OP', '04567 890 123', 'FTTP', '2023-05-16', NULL, NULL),
('Clark', '70 Pine Street', 'QR90 1RS', '05678 901 234', 'DTH','2023-05-16', NULL, NULL),
('Walker', '80 Cedar Road', 'ST12 3UV', '06789 012 345', 'BB', '2023-05-16', NULL, NULL),
('Harris', '90 Willow Close', 'WX45 6YZ', '07890 123 456', 'SE', '2023-05-16', NULL, NULL),
('Lewis', '100 Birch Lane', 'YZ67 8AB', '08901 234 567', 'MDU', '2023-05-16', NULL, NULL),
('Wilsonson', '120 Maple Road', 'CD56 7DE', '02345 678 901', 'BB', '2023-05-16', NULL, NULL),
('Andersson', '130 Oak Avenue', 'DE67 8EF', '03456 789 012', 'SE', '2023-05-16', NULL, NULL),
('Johnsonson', '140 Pine Street', 'EF78 9FG', '04567 890 123', 'MDU', '2023-05-16', NULL, NULL),
('Wilson', '70 Maple Street', 'KL90 1MN', '05678 901 234', 'BB', '2023-05-16', NULL, NULL),
('Clark', '80 Birch Lane', 'MN23 4OP', '06789 012 345', 'SE', '2023-05-16', NULL, NULL),
('Walker', '90 Willow Close', 'OP45 6QR', '07890 123 456', 'DTH', '2023-05-16', NULL, NULL),
('Hall', '100 Rose Court', 'QR67 8ST', '08901 234 567', 'BB', '2023-05-16', NULL, NULL),
('Turner', '110 Daisy Way', 'ST89 0UV', '09012 345 678', 'SE', '2023-05-16', NULL, NULL),
('White', '120 Lily Avenue', 'UV01 2WX', '00123 456 789', 'DTH', '2023-05-16', NULL, NULL),
('Lewis', '130 Sunflower Drive', 'WX34 5YZ', '01234 567 890', 'BB', '2023-05-16', NULL, NULL),
('Harris', '140 Iris Lane', 'YZ56 7AB', '02345 678 901', 'SE', '2023-05-16', NULL, NULL),
('Martin', '150 Orchid Road', 'AB67 8CD', '03456 789 012', 'DTH', '2023-05-16', NULL, NULL),
('Thompson', '160 Tulip Street', 'CD78 9EF', '04567 890 123', 'BB', '2023-05-16', NULL, NULL),
('Garcia', '170 Poppy Close', 'EF90 1GH', '05678 901 234', 'SE', '2023-05-16', NULL, NULL),
('Robinson', '190 Sunflower Way', 'IJ23 4KL', '07890 123 456', 'BB', '2023-05-16', NULL, NULL),
('Clark', '200 Iris Drive', 'KL34 5MN', '08901 234 567', 'SE', '2023-05-16', NULL, NULL),
('Rodriguez', '210 Orchid Close', 'MN56 7OP', '09012 345 678', 'DTH', '2023-05-16', NULL, NULL),
('Lee', '220 Tulip Lane', 'OP78 9QR', '00123 456 789', 'BB', '2023-05-16', NULL, NULL),
('Walker', '230 Poppy Road', 'QR90 1ST', '01234 567 890', 'SE', '2023-05-16', NULL, NULL),
('Allen', '240 Daisy Street', 'ST12 3UV', '02345 678 901', 'DTH', '2023-05-16', NULL, NULL),
('Young', '250 Sunflower Avenue', 'UV23 4WX', '03456 789 012', 'BB', '2023-05-16', NULL, NULL),
('King', '260 Iris Way', 'WX56 7YZ', '04567 890 123', 'SE', '2023-05-16', NULL, NULL),
('Wright', '270 Orchid Lane', 'YZ78 9AB', '05678 901 234', 'DTH', '2023-05-16', NULL, NULL),
('Hall', '280 Tulip Close', 'AB90 1CD', '06789 012 345', 'BB', '2023-05-16', NULL, NULL),
('Lopez', '290 Poppy Drive', 'CD12 3EF', '07890 123 456', 'SE', '2023-05-16', NULL, NULL),
('Scott', '300 Iris Road', 'EF34 5GH', '08901 234 567', 'DTH', '2023-05-16', NULL, NULL),
('Green', '310 Sunflower Street', 'GH56 7IJ', '09012 345 678', 'BB', '2023-05-16', NULL, NULL),
('Adams', '320 Orchid Avenue', 'IJ78 9KL', '00123 456 789', 'SE', '2023-05-16', NULL, NULL),
('Baker', '330 Tulip Way', 'KL90 1MN', '01234 567 890', 'DTH', '2023-05-16', NULL, NULL),
('Gonzalez', '340 Poppy Lane', 'MN23 4OP', '02345 678 901', 'BB', '2023-05-16', NULL, NULL),
('Nelson', '350 Daisy Close', 'OP45 6QR', '03456 789 012', 'SE', '2023-05-16', NULL, NULL),
('Carter', '360 Sunflower Road', 'QR67 8ST', '04567 890 123', 'DTH', '2023-05-16', NULL, NULL),
('Smith', '5 Main Road', 'ML11 1AA', '01555 123 456', 'DTH', '2023-05-16', NULL, NULL),
('Wilson', '10 High Street', 'ML1 1AB', '01555 456 456', 'DTH', '2023-05-16', NULL, NULL),
('Anderson', '20 Blue Wynd', 'ML12 3BC', '01555 987 456', 'DTH', '2023-05-16', NULL, NULL),
('Johnson', '30 Park Avenue', 'AB12 3CD', '01234 567 890', 'BB', '2023-05-16', NULL, NULL),
('Brown', '40 Elm Street', 'EF34 5GH', '02345 678 901', 'SE', '2023-05-16', NULL, NULL),
('Taylor', '50 Oak Avenue', 'GH56 7IJ', '03456 789 012', 'DTH', '2023-05-16', NULL, NULL),
('Davis', '60 Pine Road', 'IJ78 9KL', '04567 890 123', 'SE', '2023-05-16', NULL, NULL),
('Wilson', '70 Maple Street', 'KL90 1MN', '05678 901 234', 'BB', '2023-05-16', NULL, NULL),
('Clark', '80 Birch Lane', 'MN23 4OP', '06789 012 345', 'SE', '2023-05-16', NULL, NULL),
('Walker', '90 Willow Close', 'OP45 6QR', '07890 123 456', 'DTH', '2023-05-16', NULL, NULL),
('Hall', '100 Rose Court', 'QR67 8ST', '08901 234 567', 'BB', '2023-05-16', NULL, NULL),
('Turner', '110 Daisy Way', 'ST89 0UV', '09012 345 678', 'SE', '2023-05-16', NULL, NULL),
('White', '120 Lily Avenue', 'UV01 2WX', '00123 456 789', 'DTH', '2023-05-16', NULL, NULL),
('Lewis', '130 Sunflower Drive', 'WX34 5YZ', '01234 567 890', 'BB', '2023-05-16', NULL, NULL),
('Harris', '140 Iris Lane', 'YZ56 7AB', '02345 678 901', 'SE', '2023-05-16', NULL, NULL),
('Martin', '150 Orchid Road', 'AB67 8CD', '03456 789 012', 'DTH', '2023-05-16', NULL, NULL),
('Thompson', '160 Tulip Street', 'CD78 9EF', '04567 890 123', 'BB', '2023-05-16', NULL, NULL),
('Garcia', '170 Poppy Close', 'EF90 1GH', '05678 901 234', 'SE', '2023-05-16', NULL, NULL);

UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'STE01' WHERE (`Job_ID` = '5');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'STE01' WHERE (`Job_ID` = '6');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC03' WHERE (`Job_ID` = '11');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC03' WHERE (`Job_ID` = '8');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC12' WHERE (`Job_ID` = '23');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC12' WHERE (`Job_ID` = '27');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC20' WHERE (`Job_ID` = '33');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC20' WHERE (`Job_ID` = '30');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC18' WHERE (`Job_ID` = '52');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC18' WHERE (`Job_ID` = '55');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC19' WHERE (`Job_ID` = '58');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC14' WHERE (`Job_ID` = '50');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC14' WHERE (`Job_ID` = '44');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC14' WHERE (`Job_ID` = '38');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC14' WHERE (`Job_ID` = '41');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC08' WHERE (`Job_ID` = '47');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC08' WHERE (`Job_ID` = '39');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC08' WHERE (`Job_ID` = '14');
UPDATE `team_rocket_project`.`jobs` SET `Staff_ID` = 'ABC08' WHERE (`Job_ID` = '18');

