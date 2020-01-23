import numpy as np
import pandas as pd
from classes import SA


class GeneticAlgorithm:

    def __init__(self, tsp):
        self.graph_matrix = tsp.graph_matrix
        self.graph_size = tsp.size
        self.tsp = tsp

    # MUTATIONS
    def insertion(self, i, j, individual):
        # i-th element to j-th position
        list1 = individual[:]
        x = list1.pop(i)
        list1.insert(j, x)
        return list1

    def inversion(self, i, j, individual):
        if i > j:
            x = j
            j = i
            i = x

        list1 = individual[:]
        part1 = list1[:i]
        part2 = list1[i:(j + 1)]
        part3 = list1[(j + 1):]
        part2.reverse()
        list2 = part1 + part2 + part3
        return list2

    def transposition(self, i, j, individual):
        # when i = begining of subsequence and j = end of subsequence
        # then transposition = displacement
        list1 = individual[:]
        list1[i] = individual[j]
        list1[j] = individual[i]

        return list1

    def random_pop_generation(self, for_uniformity):
        initial_population = []
        for i in range(self.population_size):
            new_individual = [0] + list(np.random.permutation([x for x in range(1, self.graph_size)]))
            initial_population.append(new_individual)

        return initial_population

    def hybrid_pop_generation(self, percentage_from_SA):
        population_from_sa = int((percentage_from_SA * self.population_size) / 100)
        initial_population = []
        for i in range(population_from_sa):
            sim_ann = SA.SA(self.tsp)
            # Parameters based on experiments from previous assignment
            dst, new_individual = sim_ann.start_annealing(10000, 10000, "insert", "random", "geo", 0.99, 6)
            initial_population.append(new_individual)

        for i in range(self.population_size - population_from_sa):
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
            subset_int = np.random.random_integers(0, self.population_size - 1, size=k)
            for x in subset_int:
                subset.append(self.population[x])

            subset = sorted(subset, key=self.sort_func)
            best_in_subset = subset[0]
            selected.append(best_in_subset)

        return selected

    def rank_routes(self, routes):
        routes = sorted(routes, key=self.sort_func)
        fitness = []
        for i in range(len(routes)):
            fitness.append(1 / self.tsp.compute_distance(routes[i]))

        return routes, fitness

    def roulette_selection(self, for_uniformity):
        # Float_max - distance might be an option
        routes = self.population[:]
        sorted_routes, fitness = self.rank_routes(routes)
        csum = np.cumsum(fitness)
        cumulative_percentage = 100 * (csum / np.sum(fitness))

        selected = []
        # self.histogram = []  # for visualization purpose
        for x in range(len(sorted_routes)):
            rand = 100 * np.random.random()
            for i in range(len(sorted_routes)):
                if rand <= cumulative_percentage[i]:
                    selected.append(sorted_routes[i])
                    # self.histogram.append(i)
                    break

        return selected

    def get_key_from_value(self, mydict, search_value):
        return next((k for k, value in mydict.items() if value == search_value), None)

    def PMX_crossover(self, parents):
        i = 0
        new_generation = []
        while i < len(parents):
            if np.random.random() < self.crossover_probability:
                parent1 = parents[i]
                parent2 = parents[i + 1]
                child1 = [-1 for q in range(self.graph_size)]
                child2 = [-1 for q in range(self.graph_size)]
                # print(child1)
                is_visited1 = [False for q in range(self.graph_size)]
                is_visited2 = [False for q in range(self.graph_size)]

                rand_sel = np.random.random_integers(1, self.graph_size - 1, 2)
                k1 = min(rand_sel)
                k2 = max(rand_sel)

                child1[k1:k2 + 1] = parent2[k1:k2 + 1]
                child2[k1:k2 + 1] = parent1[k1:k2 + 1]
                for j in range(k1, k2 + 1):
                    is_visited1[parent2[j]] = True
                    is_visited2[parent1[j]] = True

                # print(child1, child2)

                # from 0 to first crossing point
                for j in range(k1):
                    if not is_visited1[parent1[j]]:
                        child1[j] = parent1[j]
                        is_visited1[parent1[j]] = True

                    if not is_visited2[parent2[j]]:
                        child2[j] = parent2[j]
                        is_visited2[parent2[j]] = True

                #     from second crossing point to end
                for j in range(k2 + 1, self.graph_size):
                    if not is_visited1[parent1[j]]:
                        child1[j] = parent1[j]
                        is_visited1[parent1[j]] = True

                    if not is_visited2[parent2[j]]:
                        child2[j] = parent2[j]
                        is_visited2[parent2[j]] = True

                vertex_to_check = 0
                contin = True

                for j in range(self.graph_size):
                    if child1[j] == -1:
                        vertex_to_check = j
                        while contin:

                            found_idx = parent2.index(parent1[vertex_to_check])
                            # Finding mapped value
                            if is_visited1[parent1[found_idx]] == False:
                                child1[j] = parent1[found_idx]
                                is_visited1[parent1[found_idx]] = True
                                contin = False

                                # if parent1[found_idx] already in child1 we are using double mapping
                            else:
                                vertex_to_check = found_idx

                        contin = True

                    if child2[j] == -1:
                        vertex_to_check = j
                        while contin:

                            found_idx = parent1.index(parent2[vertex_to_check])
                            # Finding mapped value
                            if is_visited2[parent2[found_idx]] == False:
                                child2[j] = parent2[found_idx]
                                is_visited1[parent2[found_idx]] = True
                                contin = False

                                # if parent1[found_idx] already in child1 we are using double mapping
                            else:
                                vertex_to_check = found_idx

                        contin = True

                new_generation.append(child1)
                new_generation.append(child2)


            else:
                new_generation.append(parents[i])
                new_generation.append(parents[i + 1])

            i += 2

        return new_generation

    def OX_crossover(self, parents):
        i = 0
        new_generation = []
        while i < len(parents) - 1:

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
                    child2_idx = 1

                else:
                    child1_idx = k2 + 1
                    child2_idx = k2 + 1

                # CHILD1
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

                # CHILD2
                for remaining in range(k2 + 1, self.graph_size):
                    if parent2[remaining] not in child2:
                        child2[child2_idx] = parent2[remaining]
                        child2_idx += 1
                        child2_idx %= self.graph_size
                        if child2_idx == 0:
                            child2_idx += 1

                for r2 in range(k2 + 1):
                    if ((parent2[r2] not in child2) and ((child2_idx) < k1 or (child2_idx > k2))):
                        child2[child2_idx] = parent2[r2]
                        child2_idx += 1
                        child2_idx %= self.graph_size
                        if child2_idx == 0:
                            child2_idx += 1

                new_generation.append(child1)
                new_generation.append(child2)
            else:
                new_generation.append(parents[i])
                new_generation.append(parents[i + 1])
            i += 2
        return new_generation

    def PMX_alg(self, iterations, population_size, crossover_probability, mutation_probability,
                mutation_type="insertion", selection_type="roulette", tournament_size=10, elite_size=10,
                initial_population_generation="random", percentage_for_hybrid_generation=10):

        if mutation_type == "insertion":
            self.mutation = self.insertion
        elif mutation_type == "inversion":
            self.mutation = self.inversion
        elif mutation_type == "transposition":
            self.mutation = self.transposition
        else:
            raise ValueError("Incorrect value of mutation_type parameter!")

        if selection_type == "roulette":
            self.selection = self.roulette_selection
        elif selection_type == "tournament":
            self.selection = self.tournament_selection
        else:
            raise ValueError("Incorrect value of selection_type parameter!")

        if initial_population_generation == "random":
            self.initial_pop = self.random_pop_generation
        elif initial_population_generation == "hybrid":
            self.initial_pop = self.hybrid_pop_generation
        else:
            raise ValueError("Incorrect value of initial_population_generation parameter!")

        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.population_size = population_size
        self.population = self.initial_pop(percentage_for_hybrid_generation)
        self.best_route = sorted(self.population, key=self.sort_func)[0]
        self.best_distance = self.tsp.compute_distance(self.best_route)
        how_many_children = population_size - elite_size

        for i in range(iterations):
            self.population = sorted(self.population, key=self.sort_func)

            best_candidate = self.population[0]
            best_candidate_distance = self.tsp.compute_distance(best_candidate)
            if best_candidate_distance < self.best_distance:
                self.best_route = best_candidate
                self.best_distance = best_candidate_distance

            self.parents = self.selection(tournament_size)
            self.children = self.PMX_crossover(self.parents)
            to_mutate = np.random.random_integers(0, len(self.children) - 1,
                                                  size=int(mutation_probability * len(self.children)))
            # print(to_mutate)
            for x in to_mutate:
                rand_numbers = np.random.random_integers(1, self.graph_size - 1, size=2)
                point_i = min(rand_numbers)
                point_j = max(rand_numbers)
                self.children[x] = self.mutation(point_i, point_j, self.children[x])

            self.children = sorted(self.children, key=self.sort_func)

            new_population = self.population[:elite_size] + self.children[:how_many_children]
            self.population = new_population[:]

            if elite_size < 1:
                new_best_distance = self.tsp.compute_distance(self.population[0])
                if new_best_distance < self.best_distance:
                    self.best_distance = new_best_distance
                    self.best_route = self.population[0]

        self.population = sorted(self.population, key=self.sort_func)

        best_candidate = self.population[0]
        best_candidate_distance = self.tsp.compute_distance(best_candidate)
        if best_candidate_distance < self.best_distance:
            self.best_route = best_candidate
            self.best_distance = best_candidate_distance

        return self.best_distance, self.best_route

    def OX_alg(self, iterations, population_size, crossover_probability, mutation_probability,
               mutation_type="insertion", selection_type="roulette", tournament_size=10, elite_size=10,
               initial_population_generation="random", percentage_for_hybrid_generation=10):
        if mutation_type == "insertion":
            self.mutation = self.insertion
        elif mutation_type == "inversion":
            self.mutation = self.inversion
        elif mutation_type == "transposition":
            self.mutation = self.transposition
        else:
            raise ValueError("Incorrect value of mutation_type parameter!")

        if selection_type == "roulette":
            self.selection = self.roulette_selection
        elif selection_type == "tournament":
            self.selection = self.tournament_selection
        else:
            raise ValueError("Incorrect value of selection_type parameter!")

        if initial_population_generation == "random":
            self.initial_pop = self.random_pop_generation
        elif initial_population_generation == "hybrid":
            self.initial_pop = self.hybrid_pop_generation
        else:
            raise ValueError("Incorrect value of initial_population_generation parameter!")

        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.population_size = population_size
        self.population = self.initial_pop(percentage_for_hybrid_generation)
        # print(self.population)
        self.best_route = sorted(self.population, key=self.sort_func)[0]
        self.best_distance = self.tsp.compute_distance(self.best_route)
        how_many_children = population_size - elite_size

        for i in range(iterations):
            self.parents = self.selection(tournament_size)
            # print(parents)
            self.children = self.OX_crossover(self.parents)
            to_mutate = np.random.random_integers(0, len(self.children) - 1,
                                                  size=int(mutation_probability * len(self.children)))
            # print(to_mutate)
            for x in to_mutate:
                rand_numbers = np.random.random_integers(1, self.graph_size - 1, size=2)
                point_i = min(rand_numbers)
                point_j = max(rand_numbers)
                self.children[x] = self.mutation(point_i, point_j, self.children[x])

            self.children = sorted(self.children, key=self.sort_func)

            new_population = self.population[:elite_size] + self.children[:how_many_children]
            self.population = new_population[:]

            if elite_size < 1:
                new_best_distance = self.tsp.compute_distance(self.population[0])
                if new_best_distance < self.best_distance:
                    self.best_distance = new_best_distance
                    self.best_route = self.population[0]

        self.population = sorted(self.population, key=self.sort_func)
        best_candidate = self.population[0]
        best_candidate_distance = self.tsp.compute_distance(best_candidate)
        if best_candidate_distance < self.best_distance:
            self.best_route = best_candidate
            self.best_distance = best_candidate_distance

        # print(len(self.population))
        return self.best_distance, self.best_route
