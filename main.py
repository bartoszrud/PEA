from classes import TSP as t
from classes import BB as b


x = t.TSP()
x.read_from_file('data/data18.txt')
for i in x.graph_matrix:
    print(i)

branch_and_bound = b.BB(x)

print(type(x.graph_matrix[1][1]))


# BF
# x.DFS_based()
# print(x.best_route)
# print(x.best_lengthDFS_BF)
# print(x.compute_distance([0,1,2,3,4,5,6,7,8,9]))
# best_p, best_l = x.permutation_based_BF_alg()
# print("Permutation based method, best route: {} , best length: {}".format(best_p, best_l))


#BB
branch_and_bound.simple_BB()
print(branch_and_bound.best_route)
print(branch_and_bound.best_distance)
# [0, 3, 4, 2, 8, 7, 6, 9, 1, 5]
