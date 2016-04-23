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
    user_id INTEGER NOT NULL,
    file_path VARCHAR(100) NOT NULL,
    private BOOL NOT NULL
);

LOCK TABLES `pics` WRITE;
/*!40000 ALTER TABLE `pics` DISABLE KEYS */;
INSERT INTO `pics` VALUES ('2c4045f7-f6d9-4e21-a515-a223b966741d',5,'north_korea_vs_south_korea_by_andyandreutzza-d610b1c.jpg',0),
                          ('37365b5e-e583-448d-a9ee-852aabcf2bbd',2,'dangit_jong_un_by_strangeweirdo-d4q01md.jpg',0),
                          ('380dbbe9-409d-448e-b56d-6bb1754837ef',4,'north_korea_hates_the_usa.png',0),
                          ('665d77b2-818a-49e6-a1a3-09021567faa8',2,'kim_jong_il_and_lucky_star_by_hinata_kwanggaeto-d30cydd.jpg',0),
                          ('9c583c56-ae08-4f60-a562-4b71fe0a7a08',3,'kim_jong_il_by_pxmolina.jpg',0),
                          ('cf997c73-772c-4f00-8424-e12d51aef28c',4,'kim_jong_un_by_brandonarseneault-d8atklg.jpg',0),
                          ('e2c3ebc8-f315-4596-b797-b8a5f793cf16',5,'north_korea__my_only_friend_by_rtil.jpg',0),
                          ('ffde09ed-baa3-4fdb-a198-2d3ae6a82110',3,'kim_jong_il__pokemon_master_by_thedarkchao93.jpg',0);
/*!40000 ALTER TABLE `pics` ENABLE KEYS */;
UNLOCK TABLES;

-- TODO put in admin user
-- INSERT into users (user, hash) VALUES ('admin', '$2a$12$uW7DWD3n497ZlVA1gJiuhOftfIudF/nINoiQKwm2/3rnvjuCg6Ldy');

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'kjon_is_superb','$2b$12$xGu5wW8WPJN9/nd1EcXs8OvFztss34gTUE7b1b7jCFnrzGMvhYv/K'),
                           (3,'the-real-kay-jay-un','$2b$12$jyesbIgwpyep82RbvHemWuOeK3LenhJlBHEE3NRYiADUQRtHADcg2'),
                           (4,'luv2un','$2b$12$C2ksv3u8crudXyXUUHMcdubaucd1C9QCPABSivE8.UvYTPCjb6YF2'),
                           (5,'unununium','$2b$12$Ikr7hbEAYBGM0hygrW87oeyWaYh5jnr3MnqqLgSV8eTBc86wizznK');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
