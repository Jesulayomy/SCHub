DROP DATABASE schub_test_db;
CREATE DATABASE IF NOT EXISTS schub_test_db;
CREATE USER IF NOT EXISTS "schub_test"@"localhost" IDENTIFIED BY "SECURE1_TEST2_PASSWORD3";
GRANT ALL PRIVILEGES ON schub_test_db.* TO "schub_test"@"localhost";
