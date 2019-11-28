import numpy as np

class SA:
    def __init__(self,tsp):
        self.graph_matrix = tsp.graph_matrix
        self.graph_size = tsp.size
        self.tsp = tsp


    def compute_new_distance(self):
        pass

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
    #        print(route, "  :  ", vertices)

        return route






    def start_annealing(initial_temp,max_iter,initial_solution = "greedy",cooling_schedule = "log" ):
        self.initial_temp = initial_temp

        if initial_solution == "random":
            self.best_route = np.random.permutation(10)
        elif initial_solution == "greedy":
            self.best_route = greedy_solution()
        elif initial_solution == "natural":
            self.best_route = np.arrange(self.graph_size)
        else:
            raise ValueError("Incorrect value")

        self.best_distance = self.tsp.compute_distance(self.best_route)
        self.current_route = self.best_route[:]
        self.current_distance =self.best_distance
        self.poten

        for i in range(max_iter):
            for _ in range(self.graph_size):







        return self.best_distance
