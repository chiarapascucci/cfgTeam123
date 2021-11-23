CREATE DATABASE productivity_app;
USE productivity_app;

CREATE TABLE user_info (
UserID int primary key AUTO_INCREMENT,
UserName varchar(20) UNIQUE NOT NULL,
FirstName varchar(50) NOT NULL,
LastName varchar(50) NOT NULL,
PasswordSalt char(20) NOT NULL,
PasswordHash char(128) NOT NULL,
LastLogin datetime
);

CREATE TABLE game_table (
GameID int primary key AUTO_INCREMENT,
GameName varchar(20),
GameURL varchar(150) UNIQUE
);

CREATE TABLE sessions (
SessionID int primary key AUTO_INCREMENT,
UserID int NOT NULL,
StartTime datetime,
EndTime datetime, 
RequestedDuration int NOT NULL,
FOREIGN KEY (UserID) references user_info(UserID)
);

CREATE TABLE game_record (
RecordID int primary key AUTO_INCREMENT,
UserID int NOT NULL,
GameID int NOT NULL,
SessionID int NOT NULL,
StartTime datetime,
EndTime datetime, 
FOREIGN KEY (UserID) references user_info(UserID),
foreign key (GameID) references game_table(GameID),
foreign key (SessionID) references sessions(SessionID));

DELIMITER //
CREATE PROCEDURE `register_user`(user_name varchar(20),
 first_name varchar(50), last_name varchar(50), raw_pass varchar(40))
BEGIN
DECLARE salt char(10) default CONVERT(UNIX_TIMESTAMP(), char);
DECLARE hashed_pass char(64) default sha2(concat(raw_pass, salt), 224);
INSERT INTO user_info (UserName, FirstName, LastName, PasswordSalt, PasswordHash) 
VALUES
(user_name, first_name, last_name, salt, hashed_pass);
END//

CREATE PROCEDURE `validate_user`(user_name varchar(20), raw_pass varchar(40))
BEGIN
DECLARE salt char(10) default (SELECT PasswordSalt FROM user_info WHERE UserName=user_name);
DECLARE hashed_pass char(64) default sha2(concat(raw_pass, salt), 224);
SELECT UserId FROM user_info WHERE UserName=user_name AND PasswordHash=hashed_pass;
END//
DELIMITER ;
