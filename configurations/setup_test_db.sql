CREATE DATABASE IF NOT EXISTS schub_test_db;
CREATE USER IF NOT EXISTS "schub_test"@"localhost" IDENTIFIED BY "schub_test_pwd";
GRANT ALL PRIVILEGES ON schub_test_db.* TO "schub_test"@"localhost";
