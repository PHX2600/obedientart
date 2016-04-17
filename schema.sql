-- To reload the tables:
--   mysql --user=[USER] --password=[PASS] --database=obedientart < schema.sql
-- To make the DB:
--   echo "CREATE DATABSE obedientart" | mysql -u root -p

DROP TABLE IF EXISTS users;
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(20) NOT NULL UNIQUE,
    hash VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS pics;
CREATE TABLE pics(
    id VARCHAR(100) PRIMARY KEY NOT NULL,
    file_path VARCHAR(100) NOT NULL,
    private BOOL NOT NULL
);

-- TODO put in admin user
-- INSERT into users (user, hash) VALUES ('admin', '$2a$12$uW7DWD3n497ZlVA1gJiuhOftfIudF/nINoiQKwm2/3rnvjuCg6Ldy');
