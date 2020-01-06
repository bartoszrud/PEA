import unittest
import numpy as np
from classes import TSP as t
from classes import GA

tsp = t.TSP()
tsp.read_from_file('data/dataEtap2/data16.txt')
gen = GA.GeneticAlgorithm(tsp)
population_number = 200
gen.OX_alg(100, population_number, 0.6, 0.1)
a = [1, 2, 3]
b = [1, 0, 3]
c = [2, 3, 4]
d = [a, b, c]


class MyTestCase(unittest.TestCase):
    def test_parents_len(self):
        for parent in gen.parents:
            self.assertEqual(len(parent), gen.graph_size)

    def test_parents_0idx(self):
        for parent in gen.parents:
            self.assertEqual(parent[0], 0)

    def test_children_0idx(self):
        for newone in gen.children:
            self.assertEqual(newone[0], 0)

    def test_children_pop(self):
        for newone in gen.children:
            self.assertNotIn(-1, newone)

    def test_children_duplicates(self):
        for newone in gen.children:
            for i in range(gen.graph_size):
                self.assertEqual(1, newone.count(i))

    def test_parents_duplicates(self):
        for newone in gen.parents:
            for i in range(gen.graph_size):
                self.assertEqual(1, newone.count(i))

    def test_population_number(self):
        self.assertEqual(len(gen.parents), population_number)

    def test_children_number(self):
        self.assertEqual(len(gen.population), population_number)

    def test_assert_sorting(self):
        self.assertGreater(tsp.compute_distance(gen.population[population_number - 1]),
                           tsp.compute_distance(gen.population[0]))


if __name__ == '__main__':
    unittest.main()
