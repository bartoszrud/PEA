
class BB:

    def __init__(self,tsp):
        self.graph_matrix = tsp.graph_matrix
        self.graph_size = tsp.size
        self.tsp = tsp

    def set_upper_bound(self,value):
        self.upper_bound = value



    def simple_BB(self):

        self.upper_bound = self.tsp.compute_distance([x for x in range(self.graph_size)])
        self.best_distance = self.tsp.compute_distance([x for x in range(self.graph_size)])
        self.best_route = [x for x in range(self.graph_size)]
        current_perm = []
        remaining = [i for i in range(self.graph_size)]
        self.BB_finding(remaining,current_perm, 0)


    def BB_finding(self, remaining_Vs, current_solution, V_idx):


        current_route = current_solution[:]
        remaining_vertices = remaining_Vs[:]
        # print(current_route)
        if len(remaining_vertices)>0:
            current_route.append(V_idx)
            # print(remaining_vertices)
            # print(V_idx)
            remaining_vertices.remove(V_idx)

            if len(remaining_vertices)>0:
                for i in remaining_vertices:
                    next_route = current_route[:]
                    next_route.append(i)
                    if(self.tsp.compute_partial_length(next_route)<self.upper_bound):
                        # print(next_route)
                        self.BB_finding(remaining_vertices,current_route,i)

            else:
                result = self.tsp.compute_distance(current_route)
                if result<self.best_distance:
                    self.best_route=current_route
                    self.best_distance = result
                    self.upper_bound = result
        else:
            result = self.tsp.compute_distance(current_route)
            if result<self.best_distance:
                self.best_route=current_route
                self.best_distance = result
                self.upper_bound = result
