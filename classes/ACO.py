class ACO:
    class Ant:
        def __init__(self, first_city, no_of_cities):
            self.visited = [False for i in no_of_cities]
            self.route = []
            self.current_city = first_city
            self.visited[self.current_city] = True
            self.route.append(first_city)

        def move(self, city):
            self.current_city = city
            self.visited[self.current_city] = True
            self.route.append(city)

    def __init__(self, tsp):
        self.graph_matrix = tsp.graph_matrix
        self.graph_size = tsp.size
        self.tsp = tsp
        self.pher_matrix = []
        for i in range(self.graph_size):
            row = [0 for x in range(self.graph_size)]
            self.pher_matrix.append(row)

    def update_pheromone(self, i, j, delta=0):
        self.pher_matrix[i][j] *= ro
        self.pher_matrix[i][j] += delta
