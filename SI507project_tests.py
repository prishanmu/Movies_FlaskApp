import sqlite3
import unittest


class HW5SQLiteDBTests(unittest.TestCase):

	def setUp(self):
		self.conn = sqlite3.connect("movies.db") # Connecting to database that should exist in autograder
		self.cur = self.conn.cursor()



	def test_movie_insert_works(self):
		movie = ('Jurassic Park', 'SS', 'Science Fiction', 8.0)
		m = ('Jurassic Park', 'SS', 'Science Fiction', 8.0)
		self.cur.execute("insert into Movies(title, director, genre, imdb_rating) values (?, (select id from director where name=?), ?, ?)", movie)
		self.conn.commit()

		self.cur.execute("select director, genre, imdb_rating movies where title = 'Jurassic Park'")
		data = self.cur.fetchone()
		self.assertEqual(data,m,"Testing another select statement after a sample insertion")

	def test_for_movies_table(self):
		self.cur.execute("select director, genre, imdb_rating movies where title = 'Jurassic Park'")
		data = self.cur.fetchone()
		self.assertEqual(data,('Jurassic Park', 'SS', 'Science Fiction', 8.0), "Testing data that results from selecting movie Jurassic Park")


	def test_foreign_key_director(self):
		res = self.cur.execute("select * from movies INNER JOIN directors ON movies.director = directors.id")
		data = res.fetchall()
		self.assertTrue(data, "Testing that result of selecting based on relationship between movies and directors does work")


	def tearDown(self):
		self.conn.commit()
		self.conn.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
