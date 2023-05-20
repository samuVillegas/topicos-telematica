from mrjob.job import MRJob

class MRP1_2(MRJob):

    def mapper(self, _, line):
        idemp,sector,salary,year = line.split(',')
        if not idemp == "idemp":
         yield idemp, int(salary)

    def reducer(self,idemp, values):
        count = 0
        sum = 0
        for salary in values:
            sum+=salary
            count+=1
        yield idemp, (sum/count)

if __name__ == '__main__':
    MRP1_2.run()