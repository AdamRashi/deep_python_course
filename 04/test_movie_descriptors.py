from unittest import TestCase

from movie_descriptors import Rating, Director, Actors


class Movie:
    rating = Rating()
    director = Director()
    cast = Actors()

    def __init__(self, rating=5, director="Steven Spielberg", cast=None):
        self.rating = rating
        self.director = director
        self.cast = cast or []


class TestMovieDescriptors(TestCase):
    def test_rating(self):
        test_movie = Movie()

        with self.assertRaises(ValueError):
            test_movie.rating = -1

        with self.assertRaises(ValueError):
            test_movie.rating = 11

        with self.assertRaises(TypeError):
            test_movie.rating = "some_str"

        with self.assertRaises(TypeError):
            test_movie.rating = True

        test_movie.rating = 9.9999
        self.assertEqual(str(test_movie.rating), "10.0")

        test_movie.rating = 9.45
        self.assertEqual(str(test_movie.rating), "9.4")

        test_movie.rating = 6
        self.assertEqual(str(test_movie.rating), "6.0")

        test_movie.rating = 0
        self.assertEqual(str(test_movie.rating), "0.0")

    def test_director(self):
        test_movie = Movie()

        self.assertEqual(test_movie.director, "Steven Spielberg")

        with self.assertRaises(TypeError):
            test_movie.director = 1

        with self.assertRaises(TypeError):
            test_movie.director = 6.11

        with self.assertRaises(TypeError):
            test_movie.director = True

        with self.assertRaises(ValueError):
            test_movie.director = "some_str"

        with self.assertRaises(ValueError):
            test_movie.director = "Name that do not start with capital letters"

        with self.assertRaises(ValueError):
            test_movie.director = "Bad Characters $*9_"

    def test_actors(self):
        test_movie = Movie()

        self.assertEqual(test_movie.cast, [])

        with self.assertRaises(TypeError):
            test_movie.cast = 1

        with self.assertRaises(TypeError):
            test_movie.cast = 6.11

        with self.assertRaises(TypeError):
            test_movie.cast = True

        with self.assertRaises(TypeError):
            test_movie.cast = "some_str"

        with self.assertRaises(TypeError):
            test_movie.cast = ["First Name", "Second Name", 123]

        with self.assertRaises(ValueError):
            test_movie.cast = ["Name that do not start with capital letters"]

        with self.assertRaises(ValueError):
            test_movie.cast = ["Bad Characters $*9_"]
