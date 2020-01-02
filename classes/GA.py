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
            subset_int = np.random.random_integers(1, self.population_size-1, k)
            for x in subset_int:
                subset.append(self.population[x])

            subset = sorted(subset, key = self.sort_func)
            best_in_subset = subset[0]
            selected.append(best_in_subset)

        return selected

    def PMX_crossover(self,parents):
        i = 0
        new_generation = []
        while i<len(parents):
            if np.random.random() < self.crossover_probability:
                parent1 = parents[i]
                parent2 = parents[i+1]
                child1 = [-1 for q in range(self.graph_size)]
                child2 = [-1 for q in range(self.graph_size)]

                k1,k2 = np.random.random_integers(1, self.graph_size-1, 2)
                child1[k1:k2+1] =  parent2[k1:k2+1]
                child2[k1:k2+1] =  parent1[k1:k2+1]
                part1 = parent1[k1:k2+1]
                part2 = parent2[k1:k2+1]


                # From 0 to k1-1
                for z in range(k1):
                    if parent1[z] not in child1:
                        child1[z] = parent1[z]
                    else:
                        idx = parent2.index(parent1[z])
                        if  parent1[idx] not in child1:
                            child1[z] = parent1[idx]
                        else:
                            print(i)
                            raise ValueError("COS SIE NIE ZGADZA")

                    if parent2[z] not in child2:
                        child2[z] = parent2[z]
                    else:
                        idx = parent1.index(parent2[z])
                        if  parent2[idx] not in child2:
                            child2[z] = parent2[idx]
                        else:
                            print("ERROR")
                            raise ValueError("COS SIE NIE ZGADZA")

                # From k2+1 to graph_size-1
                for z in range(k2+1,self.graph_size):
                    if parent1[z] not in child1:
                        child1[z] = parent1[z]
                    else:
                        idx = parent2.index(parent1[z])
                        if  parent1[idx] not in child1:
                            child1[z] = parent1[idx]
                        else:
                            idx2 = parent2.index(parent1[idx])
                            if parent1[idx2] not in child1:
                                child1[z] = parent1[idx2]
                            else:
                                print("ERROR")
                                raise ValueError("COS SIE NIE ZGADZA")

                    if parent2[z] not in child2:
                        child2[z] = parent2[z]
                    else:
                        idx = parent1.index(parent2[z])
                        if  parent2[idx] not in child2:
                            child2[z] = parent2[idx]
                        else:
                            print("ERROR")
                            raise ValueError("COS SIE NIE ZGADZA")

                new_generation.append(child1)
                new_generation.append(child2)



            else:
                new_generation.append(parents[i])
                new_generation.append(parents[i+1])

            i+=2










    def PMX_alg(self, population_size, crossover_probability, mutation_probability):
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.population_size = population_size
        self.population = self.random_pop_generation(population_size)
        parents = self.tournament_selection(5)
        new_population = self.PMX_crossover(parents)
