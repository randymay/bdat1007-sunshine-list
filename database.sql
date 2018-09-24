CREATE DATABASE sunshine_list;

USE sunshine_list;

CREATE TABLE sector (
    sector_name VARCHAR(255), 
    total_salary_paid FLOAT,
    total_taxable_benefits FLOAT,
    total_employers INT,
    sector_id INT NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY(sector_id),
    UNIQUE KEY(sector_name));

CREATE TABLE employer (
    employer_name VARCHAR(1000), 
    total_salary_paid FLOAT,
    total_taxable_benefits FLOAT,
    total_employees INT,
    sector_id INT NOT NULL, 
    employer_id INT NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY(employer_id),
    FOREIGN KEY (sector_id) REFERENCES sector(sector_id));