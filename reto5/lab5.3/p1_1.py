from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):

    def mapper(self, _, line):
        idemp,sector,salary,year = line.split(',')
        if not sector == "sector":
         yield sector, int(salary)

    def reducer(self, sector, salaries):
        count = 0
        sum = 0
        for salary in salaries:
            sum+=salary
            count+=1
        yield sector, (sum/count)

if __name__ == '__main__':
    MRWordFrequencyCount.run()