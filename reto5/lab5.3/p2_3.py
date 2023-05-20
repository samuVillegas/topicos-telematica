from mrjob.job import MRJob
from mrjob.step import MRStep

class MRP2_3(MRJob):
    def mapper_get_companies(self, _, line):
        Company,price,date = line.split(',')
        if not "price" == price:
            yield Company, (float(price), date)

    def reducer_get_minor_company_date(self, company, price):
        minor = 1000000
        minor_date = ''
        for i in price:
            if float(i[0]) < minor: 
                minor = float(i[0])
                minor_date = i[1]
        yield minor_date, 1 

    def reducer_count_days(self, minor_date, values):
        yield None, (minor_date, sum(values))
    
    def reducer_get_black_day(self, _, values):
        max = -1
        major_date = ''
        for date,count in values:
            if count > max: 
                max = count
                major_date = date
        yield major_date, max 

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_companies,
                   reducer=self.reducer_get_minor_company_date
            ),
            MRStep(reducer=self.reducer_count_days),
            MRStep(reducer=self.reducer_get_black_day)
        ]


if __name__ == '__main__':
    MRP2_3.run()