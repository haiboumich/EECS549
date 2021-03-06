CREATE TABLE UserInfo (   
	username VARCHAR(20),
	firstname VARCHAR(20),
	lastname VARCHAR(20),
	password VARCHAR(256),
	email VARCHAR(40),
	PRIMARY KEY (username)
);

CREATE TABLE Favorite (
	username VARCHAR(20),
	restaurant VARCHAR(40),
	PRIMARY KEY (username, restaurant),
	FOREIGN KEY (username) REFERENCES UserInfo(username)
)