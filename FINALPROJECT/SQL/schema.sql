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
GameURL varchar(150)
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
 
