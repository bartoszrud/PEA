import time
import unittest

from classes import TSP as t
from classes import BB as b
from classes import DP


def time_testing(t,branch_and_bound, dp ):
    pass


x = t.TSP()
x.read_from_file('data/SMALL/data10.txt')
for i in x.graph_matrix:
    print(i)

branch_and_bound = b.BB(x)

print(type(x.graph_matrix[1][1]))




# print(branch_and_bound.graph_matrix[10][13])
# BF
# x.DFS_based()
# print(x.best_route)
# print(x.best_lengthDFS_BF)
# print(x.compute_distance([0,1,2,3,4,5,6,7,8,9,10,11]))
# best_p, best_l = x.permutation_based_BF_alg()
# print("Permutation based method, best route: {} , best length: {}".format(best_p, best_l))

#
# tree = branch_and_bound.min_spanning_tree([0,1,2,3,4,5,6,7,8,9,10,11])
# tree_weight = branch_and_bound.MST_weight(tree)
# print(2*tree_weight)

#BB
# start1 = time.time()
# branch_and_bound.simple_BB()
# end1 = time.time()
# print("Time without lower bound= {}".format(end1-start1))
# print(branch_and_bound.best_route)
# print(branch_and_bound.best_distance)

# start = time.time()
# branch_and_bound.MST_BB_symmetric()
# end = time.time()
# print("Time with lower bound based on MST= {}".format(end-start))
# print(branch_and_bound.best_route)
# print(branch_and_bound.best_distance)
#
#
start = time.time()
branch_and_bound.BB_asymmetric()
end = time.time()
print("Time with lower bound based on minimum edges= {}".format(end-start))
print(branch_and_bound.best_route)
print(branch_and_bound.best_distance)

dpz = DP.DP(x)
dst , i= dpz.dp_method()
print(dst)
print(i)



# Very simple tets of DP algorithm
class TestTSP(unittest.TestCase):
    def test_distance(self):
        self.assertEqual(dst, branch_and_bound.best_distance)

    def test_route(self):
        self.assertEqual(i[0], 0)

    def test_route_disance(self):
        self.assertEqual(x.compute_distance(i), branch_and_bound.best_distance)

    def test_if_duplicates(self):
        self.assertEqual(len(set(i)), dpz.graph_size)



if __name__ == '__main__':
    unittest.main()
