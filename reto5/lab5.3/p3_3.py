from mrjob.job import MRJob
from mrjob.step import MRStep

class MRP3_3(MRJob):
    def mapper(self, _, line):
        Usuario,Movie,Rating,Genre,Date = line.split(',')
        if not "Usuario" == Usuario:
            yield Date, 1

    def reducer(self, date, values):
        yield None, (date, sum(values))

    def reducer_get_max(self, _, values): 
        min = 1000000
        minor_date = ''
        for date,count in values:
            if count < min: 
                min = count
                minor_date = date
        yield minor_date, min 

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                    reducer=self.reducer
            ),
            MRStep(reducer=self.reducer_get_max)
        ]

if __name__ == '__main__':
    MRP3_3.run()