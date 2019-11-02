

class DP:
    def __init__(self,tsp):
            self.graph_matrix = tsp.graph_matrix
            self.graph_size = tsp.size
            self.tsp = tsp

    def dp_method(self):
        self.route = [0  for i in range(self.graph_size)]
        Table_of_results =[[float("inf")] * (2** self.graph_size)
                            for _ in range(self.graph_size)]
        # First index is end point of our route
        # second index is representation of our set
        Table_of_results[0][1] = 0
        list_of_previous = {1:(0,0)} # s, s XOR i, last_node

        for s in range(1 << self.graph_size):
            actual_size = sum(((s>>j) & 1) for j in range(self.graph_size))
            if actual_size <= 1 or not (s&1):
                # If set contains less than 2 elements or does not contain 0 we skip this set
                continue

            for i in range(1,self.graph_size):
                if not ((s >> i) & 1):
                    continue

                    #We check if our end point 'i' is in our set
                for j in range(self.graph_size):
                    if i == j or not ((s>>j)&1):
                        continue
                        #If i is equals j or j is not in our set we skip that

                    # Now j is our second to last node
                    candidate = Table_of_results[j][s ^ (1<<i)] + self.graph_matrix[j][i]
                    Table_of_results[i][s] = min(Table_of_results[i][s],candidate)
                    if candidate == Table_of_results[i][s]:
                        list_of_previous[s]=((s ^ (1<<i),i))





        self.best_distance = min(Table_of_results[i][(2** self.graph_size)-1]
         + self.graph_matrix[i][0] for i in range(1,self.graph_size))
        last_node = 0

        # for i in range(1,self.graph_size):
        #     if (Table_of_results[i][(2** self.graph_size)-1]
        #     + self.graph_matrix[i][0] == self.best_distance):
        #         self.route[self.graph_size-1] = i
        #         break


        start =((2** self.graph_size)-1)

        for z in range(self.graph_size):
            (s_prev , last_node) = list_of_previous[start]
            self.route[self.graph_size-z-2] = last_node
            start = s_prev



        for i in range(1,self.graph_size):
             if (Table_of_results[i][(2** self.graph_size)-1]
              + self.graph_matrix[i][0] == self.best_distance):
                self.route[self.graph_size-1] = i
                break



        return self.best_distance, self.route, list_of_previous
