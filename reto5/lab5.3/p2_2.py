from mrjob.job import MRJob

class MRP2_2(MRJob):
    def mapper(self, _, line):
        Company,price,date = line.split(',')
        if not "price" == price:
            yield Company, float(price)
    def reducer(self, key, values):
        down_flag = False
        x0 = -1
        for i in values:
            if i < x0:
                down_flag = True
                break
            x0 = i    
        if not down_flag:
            yield key, True

if __name__ == '__main__':
    MRP2_2.run()