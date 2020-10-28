DROP TABLE IF EXISTS users;
CREATE TABLE users (
    uuid BINARY(16) PRIMARY KEY,
    name VARCHAR(30) ,
    username VARCHAR(30)
);
