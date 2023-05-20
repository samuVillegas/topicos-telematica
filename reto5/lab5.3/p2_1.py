from mrjob.job import MRJob

class MRP2_1(MRJob):
    def mapper(self, _, line):
        Company,price,date = line.split(',')
        if not "price" == price:
            yield Company, (price, date)
    def reducer(self, key, values):
        major = -1000000
        minor = 1000000
        major_date = ''
        minor_date = ''
        for i in values:
            if float(i[0]) > major :
                major = float(i[0])
                major_date = i[1]
            if float(i[0]) < minor: 
                minor = float(i[0])
                minor_date = i[1]
        yield key, (major_date,minor_date)

if __name__ == '__main__':
    MRP2_1.run()