#!/usr/bin/env python

import csv
import json
import sqlalchemy

def csv_load():
  # connect to the database
  engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
  connection = engine.connect()
  metadata = sqlalchemy.schema.MetaData(engine)

  ##prepared mysql tables

  # drop table if exists people_raw;
  # drop table if exists places;
  # drop table if exists people;
  # create table people_raw(id int auto_increment primary key, given_name varchar(100),family_name varchar(100),date_of_birth date,place_of_birth varchar(200));
  # create table places(id int auto_increment primary key, city varchar(100),county varchar(100),country varchar(100));
  # create table people(id int auto_increment primary key, given_name varchar(100),family_name varchar(100),date_of_birth date,birthplace_id int, foreign key(birthplace_id) references places(id));

  # make an ORM object to refer to the table
  get_people_raw = sqlalchemy.schema.Table('people_raw', metadata, autoload=True, autoload_with=engine)
  get_places = sqlalchemy.schema.Table('places', metadata, autoload=True, autoload_with=engine)
  get_people = sqlalchemy.schema.Table('people', metadata, autoload=True, autoload_with=engine)

  #delete all from tables
  connection.execute(get_people.delete()) # must be deleted first due to foreign key connection
  connection.execute(get_people_raw.delete())
  connection.execute(get_places.delete())
  # read the CSV data file into the table

  with open('/data/places.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
      connection.execute(get_places.insert().values(city = row[0], county = row[1], country = row[2]))

  with open('/data/people.csv') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
      connection.execute(get_people_raw.insert().values(given_name = row[0], family_name = row[1], date_of_birth = row[2],place_of_birth=row[3]))

  # normalize by adding fkey to people_raw > people (birth_place_id)
  # consider using ORM to insert sql-result
  sql_statement_1 = 'insert into people (given_name, family_name, date_of_birth, birthplace_id)select given_name, family_name, date_of_birth, plc.id as birthplace_id ' \
                    ' from people_raw p ' \
                    ' left join places plc on upper(plc.city) = upper(p.place_of_birth)'

  connection.execute(sql_statement_1)

def output_to_json():
  """output SQL-result to a JSON file"""

  engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
  connection = engine.connect()
  metadata = sqlalchemy.schema.MetaData(engine)

  #consider using ORM to join tables
  sql_statement = 'select p2.country, count(1) num_of_people ' \
                    'from people p1 ' \
                    'inner join places p2 on p1.birthplace_id = p2.id group by p2.country'

  with open('/data/my_output_python.json', 'w') as json_file:
    rows = connection.execute(sql_statement).fetchall()
    rows = [{row[0]: row[1]} for row in rows]
    json.dump(rows[0] | rows[1], json_file, separators=(',', ':'))


def main():
  csv_load()
  output_to_json()

if __name__ == '__main__':
    main()