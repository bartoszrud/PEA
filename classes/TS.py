import numpy as np

class SA:

    def __init__(self,tsp):
        self.graph_matrix = tsp.graph_matrix
        self.graph_size = tsp.size
        self.tsp = tsp
        self.tabu_list = []

    def greedy_solution(self):
        vertices = [x for x in range(1,self.graph_size)]
        route = [0]
        for i in range(1,self.graph_size):
            lowest_weight = self.graph_matrix[route[i-1]][vertices[0]]
            nearest = vertices[0]
            for j in vertices:
                if self.graph_matrix[route[i-1]][j] < lowest_weight:
                    nearest = j
                    lowest_weight = self.graph_matrix[route[i-1]][j]
            route.append(nearest)
            vertices.remove(nearest)
        return route


    def swap(self,i,j):
        list = self.current_route[:]
        # print(self.current_route)
        list[i] = self.current_route[j]
        list[j] = self.current_route[i]
        # print(list)

        return list

    def insert(self,i,j):
        list = self.current_route[:]
        x = list.pop(i)
        list.insert(j,x)

        return list

    def invert(self,i,j):
        if i>j:
            x = j
            j=i
            i=x

        list = self.current_route[:]
        part1 = list[:(i)]
        part2 = list[(i):(j+1)]
        part3 = list[(j+1):]
        part2.reverse()
        list2 = part1 +part2+part3
        return list2


    def m_val(self,current,candidate):
        x = self.tsp.compute_distance(current)
        y = self.tsp.compute_distance(candidate)




    def start_search(self,max_iter,initial_solution = "random",movement = "swap"):
        if initial_solution == "random":
            self.best_route = [0] + list(np.random.permutation([x for x in range(1,self.graph_size)]))
        elif initial_solution == "greedy":
            self.best_route = self.greedy_solution()
        elif initial_solution == "natural":
            self.best_route = list(np.arange(self.graph_size))
        else:
            raise ValueError("Incorrect value")

        self.best_distance = self.tsp.compute_distance(self.best_route)

        if movement == "swap":
            self.movement = self.swap
        elif movement == "insert":
            self.movement = self.insert
        elif movement == "invert":
            self.movement = self.invert
        else:
            raise ValueError("Incorrect value")

        self.current_route = self.best_route[:]
        self.current_distance = self.best_distance

        for _ in range(max_iter):
            for i in range(self.graph_size):
                for j in range(self.graph_size):
                    if i == j:
                        continue
