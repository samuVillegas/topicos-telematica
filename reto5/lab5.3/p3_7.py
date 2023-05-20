from mrjob.job import MRJob
from mrjob.step import MRStep

class MRP3_7(MRJob):
    def mapper(self, _, line):
        Usuario,Movie,Rating,Genre,Date = line.split(',')
        if not "Genre" == Genre:
            yield Genre, (Movie, int(Rating))

    def reducer(self, Genre, values):
        min = 10000000
        max = -1
        worst_movie = -1
        better_movie = -1
        for movie, rating in values:
            if rating > max:
                max = rating
                better_movie = movie
            if rating < min: 
                min = rating
                worst_movie = movie
        yield Genre, (better_movie, worst_movie)

if __name__ == '__main__':
    MRP3_7.run()