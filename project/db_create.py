import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as connection:

	c = connection.cursor()

	c.execute("""CREATE TABLE cars(car_id INTEGER PRIMARY KEY AUTOINCREMENT,
		make TEXT NOT NULL, model TEXT NOT NULL, 
		year INTEGER NOT NULL,
		color TEXT NOT NULL)""")

	c.execute('INSERT INTO cars(make, model, year, color)'
		'VALUES("Dodge", "Stratus", 2004, "silver")')

	c.execute('INSERT INTO cars(make, model, year, color)'
		'VALUES("Ferrari", "Spyder", 2016, "red")')