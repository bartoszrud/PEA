
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

    def BB_asymmetric(self):

        self.upper_bound = self.tsp.compute_distance([x for x in range(self.graph_size)])
        self.best_distance = self.tsp.compute_distance([x for x in range(self.graph_size)])
        self.best_route = [x for x in range(self.graph_size)]
        current_perm = []
        remaining = [i for i in range(self.graph_size)]
        self.BB_with_two_min_edges_as_lower_bound(remaining,current_perm, 0)


    def MST_BB_symmetric(self):
        self.upper_bound = 2*(self.MST_weight(self.min_spanning_tree([x for x in range(self.graph_size)])))
        self.best_distance = self.tsp.compute_distance([x for x in range(self.graph_size)])
        self.best_route = [x for x in range(self.graph_size)]
        current_perm = []
        remaining = [i for i in range(self.graph_size)]
        self.BB_with_MST_as_lower_bound(remaining,current_perm, 0)


    def min_spanning_tree(self,V):
        remaining_Vs = V[:]
        Tree = []

        def func(tup):
            comp_element = self.graph_matrix[tup[0]][tup[1]]
            return comp_element

        if len(remaining_Vs)>1:
            visited = { x:False for x in remaining_Vs}
            v = remaining_Vs[0]
            visited[v]= True
            edges = []

            for i in range(len(V)):
                for u in remaining_Vs:
                    if visited[u] == False and u != v:
                        edges.append((v,u))


                edges = sorted(edges, key = func, reverse=True)

                leng = len(edges)

                for j in range(leng):
                    e = edges.pop()
                    u = e[1]
                    if visited[u] == False:
                        Tree.append(e)
                        visited[u] = True
                        v = u
                        break
        return Tree


    def MST_weight(self,Tree):
        sum = 0


        if len(Tree)>1:
            for x,y in Tree:
                sum = sum + self.graph_matrix[x][y]


        return sum

    def two_min_edges_bound(self,V):
        sum = 0

        for v in V:
            listv = self.graph_matrix[v][:]
            listv = sorted(listv)
            sum += listv[1] +listv [2]
            #list[0] will be always route to node v itself (-1)


        sum = sum/2
        return sum





    def BB_with_MST_as_lower_bound(self, remaining_Vs, current_solution, V_idx):
        # ONLY FOR UNDIRECTED GRAPH (PRIM ALG)
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
                    future_remaining = remaining_vertices[:]
                    future_remaining.remove(i)

                    # Lower bound as sum of  of the travelled distance so far
                    # and the lower estimation of the remaining distance based on MST

                    l_bound = ((self.tsp.compute_partial_length(next_route)) + (self.MST_weight(self.min_spanning_tree(future_remaining))))

                    if (l_bound<self.upper_bound):
                        # print(next_route)
                        self.BB_with_MST_as_lower_bound(remaining_vertices,current_route,i)


            else:
                result = self.tsp.compute_route(current_route)
                if result<self.best_distance:
                    self.best_route=current_route
                    self.best_distance = result
                    self.upper_bound = result
                    


    def BB_with_two_min_edges_as_lower_bound(self, remaining_Vs, current_solution, V_idx):
        # ONLY FOR UNDIRECTED GRAPH (PRIM ALG)
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
                    future_remaining = remaining_vertices[:]
                    future_remaining.remove(i)

                    # Lower bound as sum of  of the travelled distance so far
                    # and the lower estimation of the remaining distance based on MST

                    l_bound = (self.tsp.compute_partial_length(next_route) + self.two_min_edges_bound(future_remaining))

                    if (l_bound<self.upper_bound):
                        # print(next_route)
                        self.BB_with_two_min_edges_as_lower_bound(remaining_vertices,current_route,i)


            else:
                result = self.tsp.compute_route(current_route)
                if result<self.best_distance:
                    self.best_route=current_route
                    self.best_distance = result
                    self.upper_bound = result









    def BB_finding(self, remaining_Vs, current_solution, V_idx):
        # the simplest BB implementation without lower bound

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
                result = self.tsp.compute_route(current_route)
                if result<self.best_distance:
                    self.best_route=current_route
                    self.best_distance = result
                    self.upper_bound = result
