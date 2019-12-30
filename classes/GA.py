import numpy as np

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

    def random_pop_generation(self, no):
        initial_population = []
        for i in range(no):
            new_individual = [0] + list(np.random.permutation([x for x in range(1,self.graph_size)]))
            initial_population.append(new_individual)

        return initial_population

    def sort_func(self, to_sorting):
        comp_element = self.tsp.compute_distance(to_sorting)
        return comp_element


    def tournament_selection(self,k):
        np.random.random_integers(1, 6, k)
        selected = []

        for i in range(self.population_size):
            subset = []
            subset_int = np.random.random_integers(1, self.population_size, k)
            for x in subset_int:
                subset.append(self.population[x])

            subset = sorted(subset, key = self.sort_func)
            best_in_subset = sorted[0]
            selected.append(best_in_subset)


    def PMX_alg(self, population_size):
        self.population_size = population_size
        self.population = random_pop_generation(population_size)
