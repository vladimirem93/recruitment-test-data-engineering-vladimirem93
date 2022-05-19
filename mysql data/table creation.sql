create table people (id int auto_increment primary key, given_name varchar(100),family_name varchar(100),date_of_birth date,place_of_birth varchar(200));
create table places(id int auto_increment primary key, city varchar(100),county varchar(100),country varchar(100));

--consider people2places;


select ifnull(p2.country,'N') as country, count(1) num_of_people from people p1
inner join places p2 on upper(p1.place_of_birth) = upper(p2.city)
group by ifnull(p2.country,'N')