--Users table for registered users
drop table if exists users
    create table users(
      id integer primary key autoincrement,
      name varchar(20) not null,
      surname varchar(20) not null,
      password varchar(20) null,      
      email varchar(20) not null
    );
    
--Contacts table where users will keep their contacts
drop table if exists contacts
    create table contacts(
        cid integer autoincrement,
        usid integer foreign key reference table users(id),
        cname varchar(20) not null,
        csurname varchar(20) not null,
        cphone varchar(15) not null,
        cemail varchar(20) not null,
		primary key (cid, usid)
    );