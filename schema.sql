-- To reload the tables:
--   sqlite3 database.db < schema.sql

DROP TABLE IF EXISTS users;
CREATE TABLE users(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT(20) NOT NULL UNIQUE,
    hash TEXT(100) NOT NULL
);

DROP TABLE IF EXISTS pics;
CREATE TABLE pics(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT(20) NOT NULL UNIQUE,
    file_path TEXT(100) NOT NULL
);

DROP TABLE IF EXISTS flags;
CREATE TABLE flags (
    id INTEGER PRIMARY KEY,
    value TEXT(500)
);



--TODO replace in prod
INSERT into flags (value) VALUES ('congrats flag1');

--TODO put in admin user
-- INSERT into users (user, hash) VALUES ('admin', '$2a$12$uW7DWD3n497ZlVA1gJiuhOftfIudF/nINoiQKwm2/3rnvjuCg6Ldy');
