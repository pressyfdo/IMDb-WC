from django.db import models

# Create your models here.
#

class Movie(models.Model):
    """
    Table to  store the details of the movies
    """
    movie_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    rating = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    stars = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)

    def add(data):
        """
        Create a movie record
        """
        name = data['data']['name']
        movie_id = data['data']['movie_id']
        year = data['data']['year']
        duration = data['data']['duration']
        rating = data['data']['rating']
        director = data['data']['director']
        writer = data['data']['writer']
        description = data['data']['description']
        genre = data['data']['genre']
        stars = data['data']['stars']

        movie = Movie.objects.create(
            movie_id = movie_id,
            name = name,
            duration = duration,
            year = year,
            director = director,
            writer = writer,
            description = description,
            rating = rating,
            genre = genre,
            stars = stars
        )

        return movie.get_details()

    def get_details(self):
        """
        Returns all the details about a movie stored in a database.
        """

        return {
            'data': {
                'movie_id': self.movie_id,
                'name': self.name,
                'year': self.year,
                'duration': self.duration,
                'rating': self.rating,
                'writer': self.writer,
                'description': self.description,
                'stars': self.stars,
                'genre': self.genre,
                'director': self.director
            }
        }
