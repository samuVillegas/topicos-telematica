from mrjob.job import MRJob
from mrjob.step import MRStep

class MRP3_2(MRJob):
    def mapper(self, _, line):
        Usuario,Movie,Rating,Genre,Date = line.split(',')
        if not "Usuario" == Usuario:
            yield Date, 1

    def reducer(self, date, values):
        yield None, (date, sum(values))

    def reducer_get_max(self, _, values): 
        max = -1
        major_date = ''
        for date,count in values:
            if count > max: 
                max = count
                major_date = date
        yield major_date, max 

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                    reducer=self.reducer
            ),
            MRStep(reducer=self.reducer_get_max)
        ]

if __name__ == '__main__':
    MRP3_2.run()