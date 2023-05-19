from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        idemp,sector,salary,year = line.split(',')
        if not idemp == "idemp":
         yield idemp, sector

    def reducer(self, key, values):
        cont = 0
        sectors = {}
        for sector in values:
           cont+=1
        yield key, cont

if __name__ == '__main__':
    MRWordFrequencyCount.run()