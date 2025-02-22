#!/usr/bin/env python

import csv
import json
import sqlalchemy

def csv_load():
  # connect to the database
  engine = sqlalchemy.create_engine("mysql://codetest:swordfish@database/codetest")
  connection = engine.connect()

  metadata = sqlalchemy.schema.MetaData(engine)

  # make an ORM object to refer to the table
  get_people_raw = sqlalchemy.schema.Table('people_raw', metadata, autoload=True, autoload_with=engine)
  get_places = sqlalchemy.schema.Table('places', metadata, autoload=True, autoload_with=engine)
  get_people = sqlalchemy.schema.Table('people', metadata, autoload=True, autoload_with=engine)

  #delete all from tables
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

  sql_statement_1 = 'insert into people (given_name, family_name, date_of_birth, birthplace_id)select given_name, family_name, date_of_birth, plc.id as birthplace_id ' \
                    ' from people_raw p ' \
                    ' left join places plc on upper(plc.city) = upper(p.place_of_birth)'
  connection.execute(get_people.delete())
  connection.execute(sql_statement_1)

  #output the table to a JSON file
  sql_statement_2 = 'select  p2.country, count(1) num_of_people ' \
                    'from people p1 ' \
                    'inner join places p2 on p1.birthplace_id = p2.id group by p2.country'

  with open('/data/my_output_python.json', 'w') as json_file:
    rows = connection.execute(sql_statement_2).fetchall()
    rows = [{row[0]: row[1]} for row in rows]
    json.dump(rows[0] | rows[1], json_file, separators=(',', ':'))


def main():
  csv_load()

if __name__ == '__main__':
    main()