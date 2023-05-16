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
 	PRIMARY KEY (`Staff_ID`));
  
CREATE TABLE `team_rocket_project`.`Jobs` (
    `Job_ID` INT AUTO_INCREMENT NOT NULL,
    `Customer Last Name` VARCHAR(45),
    `Address` VARCHAR(45),
    `Postcode` VARCHAR(45),
    `Phone_Number` VARCHAR(45),
    `Visit_Type` ENUM('DTH', 'BB', 'SE', 'MDU', 'FTTP'),
    `Staff_ID` VARCHAR(45),
    `Job_Date` DATE,
    `Start_Time` TIMESTAMP,
    `End_Time` TIMESTAMP,
    PRIMARY KEY (`Job_ID`),
    FOREIGN KEY (`Staff_ID`) REFERENCES `staff` (`Staff_ID`)
);

INSERT INTO staff VALUES ('JWI12', 'James', 'Wilson', 'Main Street', 'ML11 8EZ', '07341829218', 'Yes', 'No', 'No', 'No', 'Yes', 'No' ),
('STE01', 'Steven', 'Henderson', 'Back Street', 'ML1 8ET', '07341658218', 'No', 'No', 'No', 'No', 'No', 'Yes' );

INSERT INTO Jobs VALUES ('00001', 'Smith', '5, Main Road', 'ML11 1AA', '01555 123 456', 'DTH', 'JWI12', '2023-05-16', NULL, NULL),
('00002', 'Wilson', '10 High Street', 'ML1 1AB', '01555 456 456', 'DTH', 'JWI12', '2023-05-16', NULL, NULL),
('00003', 'Anderson', '20 Blue Wynd', 'ML12 3BC', '01555 987 456', 'DTH', 'JWI12', '2023-05-16', NULL, NULL);

INSERT INTO `team_rocket_project`.`Jobs` (`Customer Last Name`, `Address`, `Postcode`) VALUES ('McLeoud', '30 Red Road', 'EH13 9LE');
