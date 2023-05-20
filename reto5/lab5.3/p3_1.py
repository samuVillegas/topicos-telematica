from mrjob.job import MRJob

class MRP3_1(MRJob):
    def mapper(self, _, line):
        Usuario,Movie,Rating,Genre,Date = line.split(',')
        if not "Usuario" == Usuario:
            yield Usuario, float(Rating)

    def reducer(self, key, values):
        cont = 0
        sum = 0
        for i in values:
            sum+=i
            cont+=1
        yield key, (cont,(sum)/cont)

if __name__ == '__main__':
    MRP3_1.run()