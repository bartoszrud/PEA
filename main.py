import time
import unittest

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

from classes import TSP as t
from classes import BB as b
from classes import DP


def time_testing( n, path, data_numbers):
    results = {}
    number_of_instances = len(data_numbers)
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



    sum_index = 0

    for z in data_numbers:
        ts = t.TSP()
        ts.read_from_file(path+'data{}.txt'.format(z))
        # for i in ts.graph_matrix:
        #     print(i)

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

            if z<13:
                start = time.time()
                ts.DFS_based()
                end = time.time()
                sum_BF[sum_index]+=(end-start)


        results["Problem size"].append(z)
        if z<13:
            results["Brute Force"].append(sum_BF[sum_index]/n)
        else:
            results["Brute Force"].append(None)


        results["Branch and bound(MST)"].append(sumBB_sym[sum_index]/n)
        results["Branch and bound(two minimum edges)"].append(sumBB_asym[sum_index]/n)
        results["Simple branch and bound"].append(sumBB_simple[sum_index]/n)
        results["Dynamic programming"].append(sum_dp[sum_index]/n)
        sum_index+=1


    return results

def make_figure(df,main_title):

    x_axis = df["Problem size"]
    figure = go.Figure(layout=go.Layout(
        title=go.layout.Title(text=main_title),
        yaxis_title= "Czas[s]",
        xaxis_title= "Liczba wierzchołków w grafie",
        font=dict(
        family="Courier New, monospace",
        size=20,
        color="#7f7f7f"
    )
    ))
    figure.add_trace(go.Scatter(x=x_axis, y=df["Dynamic programming"],
                        mode='markers',
                        name='Dynamic programming',
                        marker = dict(size = 12)
                        ))


    figure.add_trace(go.Scatter(x=x_axis, y=df["Branch and bound(two minimum edges)"],
                        mode='markers',
                        name="Branch and bound(two minimum edges)",
                        marker = dict(size = 12)
                        ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Branch and bound(MST)"],
                        mode='markers',
                        name="Branch and bound(MST)",
                        marker = dict(size = 12)
                        ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Brute Force"],
                        mode='markers',
                        name="Brute Force",
                        marker = dict(size = 12)
                        ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Simple branch and bound"],
                        mode='markers',
                        name="Simple branch and bound",
                        marker = dict(size = 12)
                        ))


    pio.write_html(figure, file='test_plot.html', auto_open=True)

    figure.show()



# x = t.TSP()
# x.read_from_file('data/SMALL/data10.txt')
# for i in x.graph_matrix:
#     print(i)
# #
# branch_and_bound = b.BB(x)
#





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
result= time_testing( 1,  'data/SMALL/', [10])
df = pd.DataFrame(result)
print(df.head())
df.to_csv("Test.csv")
# df.to_latex("Test.tex", bold_rows = True)
make_figure(df,"TEST")
