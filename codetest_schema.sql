use codetest; 

drop table if exists examples;

create table `examples` (
  `id` int not null auto_increment,
  `name` varchar(80) default null,
  primary key (`id`)
);


drop table if exists people_raw;
drop table if exists places;
drop table if exists people;


create table people_raw(id int auto_increment primary key, given_name varchar(100),family_name varchar(100),date_of_birth date,place_of_birth varchar(200));
create table places(id int auto_increment primary key, city varchar(100),county varchar(100),country varchar(100));
create table people(id int auto_increment primary key, given_name varchar(100),family_name varchar(100),date_of_birth date,birthplace_id int, foreign key(birthplace_id) references places(id));


select  p2.country, count(1) num_of_people from people p1
inner join places p2 on upper(p1.place_of_birth) = upper(p2.city)
group by p2.country