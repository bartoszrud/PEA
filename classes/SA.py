import numpy as np

class SA:
    def __init__(self,tsp):
        self.graph_matrix = tsp.graph_matrix
        self.graph_size = tsp.size
        self.tsp = tsp


    def compute_new_distance(self):
        pass

    def logarithmic(self,temp0,parameter,iter):
        temp = temp0/(parameter + np.log(iter))
        return temp

    def linear(self,temp0,parameter,iter):
        temp = temp0/(parameter+iter)
        return temp

    def geometric(self,temp0,parameter,iter):
        temp = temp0*(parameter**iter)
        return temp

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



    def start_annealing(self,initial_temp, max_iter,movement = "swap",
                        initial_solution = "greedy",cooling_schedule = "log",cooling_parameter = 0.999, inner_loop =2 ):
        """Method for performing simulated annealing.
                            :param initial_temp: Initial temperature
                            :type initial_temp: int
                            :param max_iter: Number of algorithm iterations in main loop
                            :type max_iter: int
                            :param movement: type of movement as a neighbourhood
                            :type movement: string
                            :param initial_solution: method for generating initial solution
                            :type initial_solution: string
                            :param cooling_schedule: Type of cooling schedule (logarithmic, geometric or linear)
                            :type cooling_schedule: string
                            :param cooling_parameter: Cooling parameter 'a' for each method
                            :type cooling_parameter: float
                            :param inner_loop: Iterations in inner loop = inner_loop*graph_size
                            :type inner_loop: int
                            
                            :return Tuple. The shortest distance and the shortest route founded
                            :rtype: Tuple[int, list]
        """
        temperature = initial_temp

        if initial_solution == "random":
            self.best_route = [0] + list(np.random.permutation([x for x in range(1,self.graph_size)]))
        elif initial_solution == "greedy":
            self.best_route = self.greedy_solution()
        elif initial_solution == "natural":
            self.best_route = list(np.arange(self.graph_size))
        else:
            raise ValueError("Incorrect value of initial_solution parameter!")



        if movement == "swap":
            self.movement = self.swap
        elif movement == "insert":
            self.movement = self.insert
        elif movement == "invert":
            self.movement = self.invert
        else:
            raise ValueError("Incorrect value of movement parameter!")

        if cooling_schedule == "log":
            self.cooling_schedule = self.logarithmic
        elif cooling_schedule == "geo":
            if cooling_parameter <= 0 or cooling_parameter>1:
                raise ValueError("Incorrect value of cooling_parameter parameter!")

            self.cooling_schedule = self.geometric
        elif cooling_schedule == "lin":
            self.cooling_schedule = self.linear
        else:
            raise ValueError("Incorrect value of cooling_schedule parameter!")




        self.best_distance = self.tsp.compute_distance(self.best_route)
        self.current_route = self.best_route[:]
        self.current_distance = self.best_distance


        for z in range(max_iter):
            if(temperature<1):
                break
            for _ in range(self.graph_size*2):
                i, j = np.random.random_integers(self.graph_size-1, size=(2))
                self.potential_solution = self.movement(i,j)[:]
                self.potential_distance = self.tsp.compute_distance(self.potential_solution)

                if self.potential_distance < self.current_distance:
                    self.current_route = self.potential_solution[:]
                    self.current_distance = self.potential_distance
                elif np.random.random() < np.exp(-(self.potential_distance - self.current_distance)/temperature):
                    # print(np.exp(-(self.potential_distance - self.current_distance)/temperature))
                    self.current_route = self.potential_solution[:]
                    self.current_distance = self.potential_distance

                if self.current_distance < self.best_distance:
                    self.best_route = self.current_route[:]
                    self.best_distance = self.current_distance

            temperature = self.cooling_schedule(initial_temp,cooling_parameter, (z+1))



        return self.best_distance, self.best_route
