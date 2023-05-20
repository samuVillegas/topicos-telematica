from mrjob.job import MRJob
from mrjob.step import MRStep

class MRP3_4(MRJob):
    def mapper(self, _, line):
        Usuario,Movie,Rating,Genre,Date = line.split(',')
        if not "Movie" == Movie:
            yield Movie, int(Rating)

    def reducer(self, Movie, values):
        cont = 0
        sum = 0
        for rating in values:
            cont+=1
            sum+=rating
        yield Movie, (cont, sum/cont)

if __name__ == '__main__':
    MRP3_4.run()