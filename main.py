from classes import TSP as t

x = t.TSP()
x.read_from_file('data/data12.txt')
for i in x.graph_matrix:
    print(i)

print(type(x.graph_matrix[1][1]))
# print(x.compute_distance([0,1,2,3,4,5,6,7,8,9]))
best_p, best_l = x.permutation_based_BF_alg()
print(best_p, best_l)
