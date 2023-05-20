from mrjob.job import MRJob
from mrjob.step import MRStep

class MRP3_6(MRJob):
    def mapper(self, _, line):
        Usuario,Movie,Rating,Genre,Date = line.split(',')
        if not "Movie" == Movie:
            yield Date, int(Rating)

    def reducer(self, Date, values):
        cont = 0
        sum = 0
        for rating in values:
            cont+=1
            sum+=rating
        yield None, (Date, sum/cont)

    def reducer_get_better_average(self, _, values):
        max = -1
        better_date = ''
        for date,count in values:
            if count > max: 
                max = count
                better_date = date
        yield better_date, max 

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                    reducer=self.reducer
            ),
            MRStep(reducer=self.reducer_get_better_average)
        ]

if __name__ == '__main__':
    MRP3_6.run()