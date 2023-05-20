from mrjob.job import MRJob
from mrjob.step import MRStep

class MRP3_5(MRJob):
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

    def reducer_get_worst_average(self, _, values):
        min = 1000000
        worst_date = ''
        for date,count in values:
            if count < min: 
                min = count
                worst_date = date
        yield worst_date, min 

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                    reducer=self.reducer
            ),
            MRStep(reducer=self.reducer_get_worst_average)
        ]

if __name__ == '__main__':
    MRP3_5.run()