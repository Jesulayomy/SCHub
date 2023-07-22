CREATE DATABASE IF NOT EXISTS schub;
CREATE USER IF NOT EXISTS "schub_dev"@"localhost" IDENTIFIED BY "schub_dev_pwd";
GRANT ALL PRIVILEGES ON schub.* TO "schub_dev"@"localhost";
