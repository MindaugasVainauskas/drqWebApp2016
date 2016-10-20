--Users table for registered users
drop table if exists users
    create table users(
      id integer primary key autoincrement,
      name varchar(20) not null,
      surname varchar(20) not null,
      password varchar(20) null,      
      email varchar(20) not null
    );    
