import time
import unittest

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from classes import TSP as t
from classes import BB as b
from classes import DP


def time_testing( n, problem_size):
    results = {}
    number_of_instances = problem_size - 10
    sumBB_simple = [0 for i in range(number_of_instances)]
    sumBB_sym = [0 for i in range(number_of_instances)]
    sumBB_asym = [0 for i in range(number_of_instances)]
    sum_BF = [0 for i in range(number_of_instances)]
    sum_dp = [0 for i in range(number_of_instances)]

    results["Problem size"]= []
    results["Brute Force"]= []
    results["Branch and bound(MST)"] = []
    results["Branch and bound(two minimum edges)"] = []
    results["Simple branch and bound"] = []
    results["Dynamic programming"] =[]



    for z in range(10,problem_size):
        ts = t.TSP()
        ts.read_from_file('data/SMALL/data{}.txt'.format(z))
        for i in ts.graph_matrix:
            print(i)

        sum_index = z-10
        branch_and_bound = b.BB(ts)
        dp = DP.DP(ts)

        for i in range(n):
            start1 = time.time()
            branch_and_bound.simple_BB()
            end1 = time.time()
            sumBB_simple[sum_index]+= end1-start1


            start = time.time()
            branch_and_bound.MST_BB_symmetric()
            end = time.time()
            sumBB_sym[sum_index]+=(end-start)

            start = time.time()
            branch_and_bound.BB_asymmetric()
            end = time.time()
            sumBB_asym[sum_index] += (end-start)

            start = time.time()
            length_dp , route_dp= dp.dp_method()
            end = time.time()
            sum_dp[sum_index]+=(end-start)

            start = time.time()
            ts.DFS_based()
            end = time.time()
            sum_BF[sum_index]+=(end-start)


        results["Problem size"].append(z)
        results["Brute Force"].append(sum_BF[sum_index]/n)
        results["Branch and bound(MST)"].append(sumBB_sym[sum_index]/n)
        results["Branch and bound(two minimum edges)"].append(sumBB_asym[sum_index]/n)
        results["Simple branch and bound"].append(sumBB_simple[sum_index]/n)
        results["Dynamic programming"].append(sum_dp[sum_index]/n)


    return results

def make_figure(df):

    x_axis = df["Problem size"]
    figure = go.Figure()
    figure.add_trace(go.Scatter(x=x_axis, y=df["Dynamic programming"],
                        mode='markers',
                        name='Dynamic programming'))


    figure.add_trace(go.Scatter(x=x_axis, y=df["Branch and bound(two minimum edges)"],
                        mode='markers',
                        name="Branch and bound(two minimum edges)"))

    figure.show()



# x = t.TSP()
# x.read_from_file('data/SMALL/data10.txt')
# for i in x.graph_matrix:
#     print(i)
#
# branch_and_bound = b.BB(x)
#
# print(type(x.graph_matrix[1][1]))




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
# start = time.time()
# branch_and_bound.BB_asymmetric()
# end = time.time()
# print("Time with lower bound based on minimum edges= {}".format(end-start))
# print(branch_and_bound.best_route)
# print(branch_and_bound.best_distance)
#
# dpz = DP.DP(x)
# dst , i= dpz.dp_method()
# print(dst)
# print(i)



# Very simple tets of DP algorithm
# class TestTSP(unittest.TestCase):
#     def test_distance(self):
#         self.assertEqual(dst, branch_and_bound.best_distance)
#
#     def test_route(self):
#         self.assertEqual(i[0], 0)
#
#     def test_route_disance(self):
#         self.assertEqual(x.compute_distance(i), branch_and_bound.best_distance)
#
#     def test_if_duplicates(self):
#         self.assertEqual(len(set(i)), dpz.graph_size)
#
#
#
# if __name__ == '__main__':
#     unittest.main()
result= (time_testing( 1,14))
df = pd.DataFrame(result)
print(df)
make_figure(df)
