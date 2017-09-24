mysql -u root -p  "" && 

IF EXISTS(select * from sys.databases where name='gallery');
DROP DATABASE gallery; 

CREATE DATABASE gallery;

