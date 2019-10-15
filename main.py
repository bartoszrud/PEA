from classes import TSP as t

x = t.TSP()
x.read_from_file('data/data10.txt')
for i in x.graph_matrix:
    print(i)

print(type(x.graph_matrix[1][1]))

x.DFS_based()
print(x.best_route)
print(x.best_lengthDFS_BF)
print(x.compute_distance([0,1,2,3,4,5,6,7,8,9]))
best_p, best_l = x.permutation_based_BF_alg()
print("Permutation based method, best route: {} , best length: {}".format(best_p, best_l))
