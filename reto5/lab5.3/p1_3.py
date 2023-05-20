from mrjob.job import MRJob

class MRP1_3(MRJob):

    def mapper(self, _, line):
        idemp,sector,salary,year = line.split(',')
        if not idemp == "idemp":
         yield idemp, sector

    def reducer(self, key, values):
        cont = 0
        sectors = set()
        long = len(sectors)
        last_long = long
        for sector in values:
            sectors.add(sector)
            long = len(sectors)
            if not last_long == long:
                cont+=1
            last_long = long
        yield key, cont

if __name__ == '__main__':
    MRP1_3.run()