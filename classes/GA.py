class GeneticAlgorithm:

    def __init__(self,tsp):
        self.graph_matrix = tsp.graph_matrix
        self.graph_size = tsp.size
        self.tsp = tsp


    #MUTATIONS
    def insertion(self,i,j,individual):
        # i-th element to j-th position
        list = individual[:]
        x = list.pop(i)
        list.insert(j,x)
        return list

    def inversion(self,i,j,individual):
        if i>j:
            x = j
            j=i
            i=x

        list = individual[:]
        part1 = list[:(i)]
        part2 = list[(i):(j+1)]
        part3 = list[(j+1):]
        part2.reverse()
        list2 = part1 +part2+part3
        return list2

    def transposition(self,i,j,individual):
        #when i = begining of subsequence and j = end of subsequence
        # then transposition = displacement
        list = individual[:]
        list[i] = individual[j]
        list[j] = individual[i]

        return list
