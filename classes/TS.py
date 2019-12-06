import numpy as np

class TS:

    def __init__(self,tsp):
        self.graph_matrix = tsp.graph_matrix
        self.graph_size = tsp.size
        self.tsp = tsp
        self.tabu_list = []
        self.tabu_matrix = []

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
        return y-x




    def start_search(self,max_iter,initial_solution = "random",
                     movement = "swap", tabu_time = 8, CE_iter =100):
        """Method for performing tabu search.

            :param max_iter: Number of algorithm iterations in main loop
            :type max_iter: int
            :param initial_solution: method for generating initial solution
            :type initial_solution: string
            :param movement: type of movement as a neighbourhood
            :type movement: string
            :param tabu_time: Time on tabu list = (graph_size/tabu_time)
            :type tabu_time: float
            :param CE_iter: Number of iterations without improvement before new solution will be randomly chosen
            :type CE_iter: int

            :return Tuple. The shortest distance and the shortest route founded
            :rtype: Tuple[int, list]
        """

        self.tabu_time = int(self.graph_size/ tabu_time)

        if initial_solution == "random":
            self.best_route = [0] + list(np.random.permutation(
                                        [x for x in range(1,self.graph_size)]))
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


        iter_without_improvement = 0

        for _ in range(max_iter):

            next_distance = -1
            next_route = []
            new_tabu = []

            for i in range(1,self.graph_size):
                for j in range(i+1,self.graph_size):
                    in_tabu = False
                    # if (i == j) or (i == 0) or (j==0):
                    #     continue
                    self.neighbour_route = self.movement(i,j)
                    self.neighbour_distance = self.tsp.compute_distance(
                                                        self.neighbour_route)

                    for tabu in self.tabu_list:
                        if (i,j) == tabu[0]:
                            in_tabu = True
                            break

                    # Aspiration check
                    if in_tabu == True and self.neighbour_distance>=self.best_distance:
                        continue

                    if((next_distance == -1) or (self.neighbour_distance < next_distance)):
                        next_route = self.neighbour_route[:]
                        next_distance = self.neighbour_distance
                        next_tabu = [(i,j),self.tabu_time]

            if next_distance<self.best_distance:
                self.best_distance = next_distance
                self.best_route = next_route[:]
            else:
                iter_without_improvement +=1


            for tabu in self.tabu_list:
                tabu[1] -= 1
                if tabu[1] == 0:
                    self.tabu_list.remove(tabu)

            self.tabu_list.append(next_tabu)
            # print(self.tabu_list)
            # print(len(self.tabu_list))


            # Critical event
            if iter_without_improvement<CE_iter:
                self.current_route = next_route[:]
                self.current_distance = next_distance
            else:
                self.current_route = [0] + list(np.random.permutation([x for x in range(1,self.graph_size)]))
                self.current_distance = self.tsp.compute_distance(self.current_route)
                if self.current_distance < self.best_distance:
                    self.best_route = self.current_route[:]
                    self.best_distance = self.current_distance

                iter_without_improvement = 0

        return self.best_distance, self.best_route



    def start_search_matrix(self,max_iter,initial_solution = "random",
                     movement = "swap", tabu_time = 8, CE_iter =100):
        """Method for performing tabu search.

            :param max_iter: Number of algorithm iterations in main loop
            :type max_iter: int
            :param initial_solution: method for generating initial solution
            :type initial_solution: string
            :param movement: type of movement as a neighbourhood
            :type movement: string
            :param tabu_time: Time on tabu list = (graph_size/tabu_time)
            :type tabu_time: float
            :param CE_iter: Number of iterations without improvement before new solution will be randomly chosen
            :type CE_iter: int

            :return Tuple. The shortest distance and the shortest route founded
            :rtype: Tuple[int, list]
        """

        self.tabu_time = int(self.graph_size/ tabu_time)

        if initial_solution == "random":
            self.best_route = [0] + list(np.random.permutation(
                                        [x for x in range(1,self.graph_size)]))
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

        for x in range(self.graph_size):
            int_row = [0 for z in range(self.graph_size)]
            self.tabu_matrix.append(int_row)



        iter_without_improvement = 0

        for iteration in range(max_iter):

            next_distance = -1
            next_route = []
            new_tabu = []

            for i in range(1,self.graph_size):
                for j in range(i+1,self.graph_size):
                    in_tabu = False
                    # if (i == j) or (i == 0) or (j==0):
                    #     continue
                    self.neighbour_route = self.movement(i,j)
                    self.neighbour_distance = self.tsp.compute_distance(
                                                        self.neighbour_route)

                    if self.tabu_matrix[i][j]>=iteration:
                        in_tabu = True


                    # Aspiration check
                    if in_tabu == True and self.neighbour_distance>=self.best_distance:
                        continue

                    if((next_distance == -1) or (self.neighbour_distance < next_distance)):
                        next_route = self.neighbour_route[:]
                        next_distance = self.neighbour_distance
                        next_tabu = [i,j,self.tabu_time+iteration]

            if next_distance<self.best_distance:
                self.best_distance = next_distance
                self.best_route = next_route[:]
            else:
                iter_without_improvement +=1




            self.tabu_matrix[next_tabu[0]][next_tabu[1]] = next_tabu[2]
            # print(self.tabu_list)
            # print(len(self.tabu_list))


            # Critical event
            if iter_without_improvement<CE_iter:
                self.current_route = next_route[:]
                self.current_distance = next_distance
            else:
                self.current_route = [0] + list(np.random.permutation([x for x in range(1,self.graph_size)]))
                self.current_distance = self.tsp.compute_distance(self.current_route)
                if self.current_distance < self.best_distance:
                    self.best_route = self.current_route[:]
                    self.best_distance = self.current_distance

                iter_without_improvement = 0

        return self.best_distance, self.best_route
