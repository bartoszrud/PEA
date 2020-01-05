import numpy as np


class GeneticAlgorithm:

    def __init__(self, tsp):
        self.graph_matrix = tsp.graph_matrix
        self.graph_size = tsp.size
        self.tsp = tsp

    # MUTATIONS
    def insertion(self, i, j, individual):
        # i-th element to j-th position
        list = individual[:]
        x = list.pop(i)
        list.insert(j, x)
        return list

    def inversion(self, i, j, individual):
        if i > j:
            x = j
            j = i
            i = x

        list = individual[:]
        part1 = list[:(i)]
        part2 = list[(i):(j + 1)]
        part3 = list[(j + 1):]
        part2.reverse()
        list2 = part1 + part2 + part3
        return list2

    def transposition(self, i, j, individual):
        # when i = begining of subsequence and j = end of subsequence
        # then transposition = displacement
        list = individual[:]
        list[i] = individual[j]
        list[j] = individual[i]

        return list

    def random_pop_generation(self, no):
        initial_population = []
        for i in range(no):
            new_individual = [0] + list(np.random.permutation([x for x in range(1, self.graph_size)]))
            initial_population.append(new_individual)

        return initial_population

    def sort_func(self, to_sorting):
        comp_element = self.tsp.compute_distance(to_sorting)
        return comp_element

    def tournament_selection(self, k):
        np.random.random_integers(1, 6, k)
        selected = []

        for i in range(self.population_size):
            subset = []
            subset_int = np.random.random_integers(1, self.population_size - 1, k)
            for x in subset_int:
                subset.append(self.population[x])

            subset = sorted(subset, key=self.sort_func)
            best_in_subset = subset[0]
            selected.append(best_in_subset)

        return selected

    def get_key_from_value(self, mydict, search_value):
        return next((k for k, value in mydict.items() if value == search_value), None)

    def PMX_crossover(self, parents):
        # TO REFACTOR!
        i = 0
        new_generation = []
        while i < len(parents):
            map_table = {}
            if np.random.random() < self.crossover_probability:
                parent1 = parents[i]
                parent2 = parents[i + 1]
                child1 = [-1 for q in range(self.graph_size)]
                child2 = [-1 for q in range(self.graph_size)]
                # print(child1)

                k1, k2 = np.random.random_integers(1, self.graph_size - 1, 2)
                if (k1 > k2):
                    temporary = k2
                    k2 = k1
                    k1 = temporary

                child1[k1:k2 + 1] = parent2[k1:k2 + 1]
                child2[k1:k2 + 1] = parent1[k1:k2 + 1]
                print(child1, child2)
                part1 = parent1[k1:k2 + 1]
                part2 = parent2[k1:k2 + 1]
                for m in range(k1, k2 + 1):
                    map_table[parent1[m]] = parent2[m]
                    map_table[parent2[m]] = parent1[m]
                print(map_table)

                # From 0 to k1-1

                for z in range(k1):
                    if parent1[z] not in child1:
                        child1[z] = parent1[z]
                    else:
                        new_candidate = parent1[z]
                        control_counter = 0
                        while (new_candidate not in child1) == False:
                            try:
                                new_candidate = map_table[new_candidate]
                            except Exception as e:
                                pass
                            print(child1, new_candidate, z)
                            if new_candidate not in child1:
                                child1[z] = new_candidate
                                break

                            control_counter += 1
                            if control_counter % 3 == 0:
                                old_candidate = new_candidate
                                double_mapping = self.get_key_from_value(map_table, old_candidate)
                                if isinstance(double_mapping, int):
                                    new_candidate = double_mapping
                                    print(new_candidate)

                                if new_candidate not in child1:
                                    child1[z] = new_candidate
                                    break
                                else:
                                    old_candidate = new_candidate
                                    double_mapping = self.get_key_from_value(map_table, old_candidate)
                                    if isinstance(double_mapping, int):
                                        new_candidate = double_mapping
                                        print(new_candidate)

                                    if new_candidate not in child1:
                                        child1[z] = new_candidate
                                        break

                            if control_counter > self.graph_size * 2:
                                for whatever in parent1:
                                    if whatever not in child1:
                                        child1[z] = whatever
                                        break
                                break

                # From k2+1 to graph_size-1
                for z in range(k2 + 1, self.graph_size):
                    if parent1[z] not in child1:
                        child1[z] = parent1[z]
                    else:
                        new_candidate = parent1[z]
                        control_counter = 0
                        while (new_candidate not in child1) == False:
                            new_candidate = map_table[new_candidate]
                            print(child1, new_candidate, z)
                            if new_candidate not in child1:
                                child1[z] = new_candidate
                                break

                            control_counter += 1
                            if control_counter % 3 == 0:
                                old_candidate = new_candidate
                                double_mapping = self.get_key_from_value(map_table, old_candidate)
                                if isinstance(double_mapping, int):
                                    new_candidate = double_mapping
                                    print(new_candidate)

                                if new_candidate not in child1:
                                    child1[z] = new_candidate
                                    break
                                else:
                                    old_candidate = new_candidate
                                    double_mapping = self.get_key_from_value(map_table, old_candidate)
                                    if isinstance(double_mapping, int):
                                        new_candidate = double_mapping
                                        print(new_candidate)

                                    if new_candidate not in child1:
                                        child1[z] = new_candidate
                                        break

                            if control_counter > self.graph_size:
                                for whatever in parent1:
                                    if whatever not in child1:
                                        print("Cokolwiek: ", whatever)
                                        child1[z] = whatever
                                        break
                                break

                new_generation.append(child1)
                # new_generation.append(child2)

                print("GOTOWE", child1)


            else:
                new_generation.append(parents[i])
                new_generation.append(parents[i + 1])

            i += 2

        return new_generation

    def OX_crossover(self, parents):
        i = 0
        new_generation = []
        while i < len(parents):

            if np.random.random() < self.crossover_probability:
                parent1 = parents[i]
                parent2 = parents[i + 1]
                child1 = [-1 for q in range(self.graph_size)]
                child2 = [-1 for q in range(self.graph_size)]
                child1[0] = 0
                child2[0] = 0
                # print(child1)

                k1, k2 = np.random.random_integers(1, self.graph_size - 1, 2)
                if (k1 > k2):
                    temporary = k2
                    k2 = k1
                    k1 = temporary

                child1[k1:k2 + 1] = parent2[k1:k2 + 1]
                child2[k1:k2 + 1] = parent1[k1:k2 + 1]

                if k2 == self.graph_size - 1:
                    child1_idx = 1

                else:
                    child1_idx = k2 + 1

                for remaining in range(k2 + 1, self.graph_size):
                    if parent1[remaining] not in child1:
                        child1[child1_idx] = parent1[remaining]
                        child1_idx += 1
                        child1_idx %= self.graph_size
                        if child1_idx == 0:
                            child1_idx += 1

                for r2 in range(k2 + 1):
                    if ((parent1[r2] not in child1) and ((child1_idx) < k1 or (child1_idx > k2))):
                        child1[child1_idx] = parent1[r2]
                        child1_idx += 1
                        child1_idx %= self.graph_size
                        if child1_idx == 0:
                            child1_idx += 1

                new_generation.append(child1)

            i += 2
        return new_generation

    def PMX_alg(self, population_size, crossover_probability, mutation_probability):
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.population_size = population_size
        self.population = self.random_pop_generation(population_size)
        self.parents = self.tournament_selection(5)
        self.new_population = self.PMX_crossover(self.parents)

    def OX_alg(self, population_size, crossover_probability, mutation_probability):
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.population_size = population_size
        self.population = self.random_pop_generation(population_size)
        self.parents = self.tournament_selection(5)
        # print(parents)
        self.new_population = self.OX_crossover(self.parents)
        print(self.new_population)
