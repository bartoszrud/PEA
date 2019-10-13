# import fileinput

class TSP:
    def __init__(self):
        self.graph_matrix = list()
        self.route = []

    def read_from_file(self,file_name):
        file  = open(file_name)
        self.name =  file.readline()
        self.size = int(file.readline())

        for i in range(self.size):
            row = file.readline().split()
            introw = [int(x) for x in row]
            self.graph_matrix.append(introw)

    def compute_distance(self, route):
        size = self.size
        self.distance = 0
        for i in range(size - 1):
            self.distance +=self.graph_matrix[route[i]][route[i+1]]

        self.distance +=self.graph_matrix[route[size-1]][route[0]]
        return self.distance
