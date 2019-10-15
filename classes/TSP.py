# import fileinput
import itertools

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

    def permutation_based_BF_alg(self):
        default_perm = [i+1 for i in range(self.size-1)]
        default_route = list(default_perm)
        default_route.insert(0,0)
        best_length = self.compute_distance(default_route)
        best_perm = default_route

        for i in itertools.permutations(default_perm):
            i_list = list(i)
            i_list.insert(0,0)
            x = self.compute_distance(i_list)
            if best_length > x:
                best_length = x
                best_perm = i_list

        return best_perm , best_length

    def DFS_based(self):
        self.best_route = [i for i in range(self.size)]
        self.best_lengthDFS_BF = self.compute_distance(self.best_route)
        current_perm = []
        remaining = [i for i in range(self.size)]
        self.rec_BF_func(remaining,current_perm, 0)



    def rec_BF_func(self, remaining_Vs, current_solution, V_idx):
        current_route = current_solution[:]
        remaining_vertices = remaining_Vs[:]

        if len(remaining_vertices)>0:
            current_route.append(V_idx)
            # print(remaining_vertices)
            # print(V_idx)
            remaining_vertices.remove(V_idx)

            if len(remaining_vertices)>0:
                for i in remaining_vertices:
                    self.rec_BF_func(remaining_vertices,current_route,i)

            else:
                result = self.compute_distance(current_route)
                print(current_route)
                if result<self.best_lengthDFS_BF:
                    self.best_route=current_route
                    self.best_lengthDFS_BF = result
        else:
            result = self.compute_distance(current_route)
            if result<self.best_lengthDFS_BF:
                self.best_route=current_route
                self.best_lengthDFS_BF = result
