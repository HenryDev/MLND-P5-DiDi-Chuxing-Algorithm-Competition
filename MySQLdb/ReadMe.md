# MySQL version
mysql  Ver 14.14 Distrib 5.5.49, for debian-linux-gnu (x86_64) using readline 6.3

# MySQL5.5 Install scripts

sudo apt-get update

sudo apt-get install mysql-server

sudo apt-get install mysql-client

sudo apt-get install mysql-workbench

# Optional installation
sudo mysql_install_db

## Alternatively follow for installation instructions
https://www.linode.com/docs/databases/mysql/install-mysql-on-ubuntu-14-04

# Login to mysql db
mysql -u root -p

# Create a DB schema for di_di
Create database di_di;

# Create user and grant access to the database
create user 'user'@'localhost' identified by 'password';
grant all on testdb.* to 'user';
