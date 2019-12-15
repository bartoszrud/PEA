from classes import TSP as t
from classes import SA
from classes import TS

import time

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import pandas as pd

def time_testing( n, path, data_numbers,opt):
    results = {}
    number_of_instances = len(data_numbers)
    sumSA_ivrt_t = [0 for i in range(number_of_instances)]
    sumSA_ins_t= [0 for i in range(number_of_instances)]
    sumSA_sw_t = [0 for i in range(number_of_instances)]

    sumSA_ivrt_e = [0 for i in range(number_of_instances)]
    sumSA_ins_e = [0 for i in range(number_of_instances)]
    sumSA_sw_e = [0 for i in range(number_of_instances)]

    sumTS_mat_ins_t = [0 for i in range(number_of_instances)]
    sumTS_list_t = [0 for i in range(number_of_instances)]
    sumTS_mat_ins_e = [0 for i in range(number_of_instances)]
    sumTS_list_e = [0 for i in range(number_of_instances)]

    sumTS_mat_inv_t = [0 for i in range(number_of_instances)]
    sumTS_mat_inv_e = [0 for i in range(number_of_instances)]
    sumTS_mat_sw_t = [0 for i in range(number_of_instances)]
    sumTS_mat_sw_e = [0 for i in range(number_of_instances)]

    results["Problem size"] = []
    results["Simulated annealing - invert time"] = []
    results["Simulated annealing - insert time"] = []
    results["Simulated annealing - swap time"] = []
    results["Simulated annealing - invert error"] = []
    results["Simulated annealing - insert error"] = []
    results["Simulated annealing - swap error"] = []
    results["Tabu search - list time"] = []
    results["Tabu search - list error"] = []
    results["Tabu search - matrix insert error"] = []
    results["Tabu search - matrix insert time"] = []
    results["Tabu search - matrix invert error"] = []
    results["Tabu search - matrix invert time"] = []
    results["Tabu search - matrix swap error"] = []
    results["Tabu search - matrix swap time"] = []




    sum_index = 0

    for z in data_numbers:
        tsp = t.TSP()
        tsp.read_from_file(path+'data{}.txt'.format(z))

        sim_annealing = SA.SA(tsp)
        tabu_s  = TS.TS(tsp)

        for i in range(n):
            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(7000,20000,"invert","random","lin",2,6)
            end1 = time.time()
            sumSA_ivrt_t[sum_index]+= end1-start1
            sumSA_ivrt_e[sum_index] += dist

            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(7000,20000,"insert","random","lin",2,6)
            end1 = time.time()
            sumSA_ins_t[sum_index]+= end1-start1
            sumSA_ins_e[sum_index] += dist

            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(7000,20000,"swap","random","lin",2,6)
            end1 = time.time()
            sumSA_sw_t[sum_index]+= end1-start1
            sumSA_sw_e[sum_index] += dist

            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search(3000,"greedy","insert",3,80)
            end1 = time.time()
            sumTS_list_t[sum_index]+= end1-start1
            sumTS_list_e[sum_index] += dist

            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(3000,"greedy","insert",3,80)
            end1 = time.time()
            sumTS_mat_ins_t[sum_index]+= end1-start1
            sumTS_mat_ins_e[sum_index] += dist

            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(3000,"greedy","invert",3,80)
            end1 = time.time()
            sumTS_mat_inv_t[sum_index]+= end1-start1
            sumTS_mat_inv_e[sum_index] += dist

            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(3000,"greedy","swap",3,80)
            end1 = time.time()
            sumTS_mat_sw_t[sum_index]+= end1-start1
            sumTS_mat_sw_e[sum_index] += dist

        results["Problem size"].append(z)



        results["Simulated annealing - invert time"].append(sumSA_ivrt_t[sum_index]/n)
        results["Simulated annealing - insert time"].append(sumSA_ins_t[sum_index]/n)
        results["Simulated annealing - swap time"].append(sumSA_sw_t[sum_index]/n)
        results["Simulated annealing - invert error"].append((((sumSA_ivrt_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Simulated annealing - insert error"].append((((sumSA_ins_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Simulated annealing - swap error"].append((((sumSA_sw_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)



        results["Tabu search - list time"].append(sumTS_list_t[sum_index]/n)
        results["Tabu search - list error"].append((((sumTS_list_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Tabu search - matrix insert error"].append((((sumTS_mat_ins_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Tabu search - matrix insert time"].append(sumTS_mat_ins_t[sum_index]/n)

        results["Tabu search - matrix invert error"].append((((sumTS_mat_inv_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Tabu search - matrix invert time"].append(sumTS_mat_inv_t[sum_index]/n)

        results["Tabu search - matrix swap error"].append((((sumTS_mat_sw_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Tabu search - matrix swap time"].append(sumTS_mat_sw_t[sum_index]/n)




        sum_index+=1
        if(sum_index%4 == 0):
            df = pd.DataFrame(results)
            df.to_csv("backup.csv")

    return results

def iterTS_testing( n, path, data_numbers,opt):
    results = {}
    number_of_instances = len(data_numbers)

    sumTS_1000_t = [0 for i in range(number_of_instances)]
    sumTS_1000_e = [0 for i in range(number_of_instances)]

    sumTS_2000_t = [0 for i in range(number_of_instances)]
    sumTS_2000_e = [0 for i in range(number_of_instances)]

    sumTS_3000_t = [0 for i in range(number_of_instances)]
    sumTS_3000_e = [0 for i in range(number_of_instances)]
    sumTS_4000_t = [0 for i in range(number_of_instances)]
    sumTS_4000_e = [0 for i in range(number_of_instances)]

    results["Problem size"] = []

    results["Tabu search - 1000 time"] = []
    results["Tabu search - 1000 error"] = []
    results["Tabu search - 2000 error"] = []
    results["Tabu search - 2000 time"] = []
    results["Tabu search - 3000 error"] = []
    results["Tabu search - 3000 time"] = []
    results["Tabu search - 4000 error"] = []
    results["Tabu search - 4000 time"] = []




    sum_index = 0

    for z in data_numbers:
        tsp = t.TSP()
        tsp.read_from_file(path+'data{}.txt'.format(z))

        tabu_s  = TS.TS(tsp)

        for i in range(n):


            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(1000,"greedy","insert",3,80)
            end1 = time.time()
            sumTS_1000_t[sum_index]+= end1-start1
            sumTS_1000_e[sum_index] += dist

            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(2000,"greedy","insert",3,80)
            end1 = time.time()
            sumTS_2000_t[sum_index]+= end1-start1
            sumTS_2000_e[sum_index] += dist

            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(3000,"greedy","insert",3,80)
            end1 = time.time()
            sumTS_3000_t[sum_index]+= end1-start1
            sumTS_3000_e[sum_index] += dist

            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(4000,"greedy","insert",3,80)
            end1 = time.time()
            sumTS_4000_t[sum_index]+= end1-start1
            sumTS_4000_e[sum_index] += dist

        results["Problem size"].append(z)

        results["Tabu search - 1000 time"].append(sumTS_1000_t[sum_index]/n)
        results["Tabu search - 1000 error"].append((((sumTS_1000_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)

        results["Tabu search - 2000 error"].append((((sumTS_2000_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Tabu search - 2000 time"].append(sumTS_2000_t[sum_index]/n)

        results["Tabu search - 3000 error"].append((((sumTS_3000_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Tabu search - 3000 time"].append(sumTS_3000_t[sum_index]/n)

        results["Tabu search - 4000 error"].append((((sumTS_4000_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Tabu search - 4000 time"].append(sumTS_4000_t[sum_index]/n)




        sum_index+=1
        if(sum_index%4 == 0):
            df = pd.DataFrame(results)
            df.to_csv("backup.csv")

    return results

def tabuTS_testing( n, path, data_numbers,opt):
    results = {}
    number_of_instances = len(data_numbers)

    sumTS_2_t = [0 for i in range(number_of_instances)]
    sumTS_2_e = [0 for i in range(number_of_instances)]

    sumTS_3_t = [0 for i in range(number_of_instances)]
    sumTS_3_e = [0 for i in range(number_of_instances)]

    sumTS_4_t = [0 for i in range(number_of_instances)]
    sumTS_4_e = [0 for i in range(number_of_instances)]
    sumTS_5_t = [0 for i in range(number_of_instances)]
    sumTS_5_e = [0 for i in range(number_of_instances)]

    results["Problem size"] = []

    results["Tabu search - 2 time"] = []
    results["Tabu search - 2 error"] = []

    results["Tabu search - 3 error"] = []
    results["Tabu search - 3 time"] = []

    results["Tabu search - 4 error"] = []
    results["Tabu search - 4 time"] = []

    results["Tabu search - 5 error"] = []
    results["Tabu search - 5 time"] = []




    sum_index = 0

    for z in data_numbers:
        tsp = t.TSP()
        tsp.read_from_file(path+'data{}.txt'.format(z))

        tabu_s  = TS.TS(tsp)

        for i in range(n):


            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(3000,"greedy","insert",2,80)
            end1 = time.time()
            sumTS_2_t[sum_index]+= end1-start1
            sumTS_2_e[sum_index] += dist

            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(3000,"greedy","insert",3,80)
            end1 = time.time()
            sumTS_3_t[sum_index]+= end1-start1
            sumTS_3_e[sum_index] += dist

            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(3000,"greedy","insert",4,80)
            end1 = time.time()
            sumTS_4_t[sum_index]+= end1-start1
            sumTS_4_e[sum_index] += dist

            tabu_s  = TS.TS(tsp)
            start1 = time.time()
            dist , rt = tabu_s.start_search_matrix(3000,"greedy","insert",5,80)
            end1 = time.time()
            sumTS_5_t[sum_index]+= end1-start1
            sumTS_5_e[sum_index] += dist

        results["Problem size"].append(z)

        results["Tabu search - 2 time"].append(sumTS_2_t[sum_index]/n)
        results["Tabu search - 2 error"].append((((sumTS_2_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)

        results["Tabu search - 3 error"].append((((sumTS_3_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Tabu search - 3 time"].append(sumTS_3_t[sum_index]/n)

        results["Tabu search - 4 error"].append((((sumTS_4_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Tabu search - 4 time"].append(sumTS_4_t[sum_index]/n)

        results["Tabu search - 5 error"].append((((sumTS_5_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Tabu search - 5 time"].append(sumTS_5_t[sum_index]/n)




        sum_index+=1
        if(sum_index%4 == 0):
            df = pd.DataFrame(results)
            df.to_csv("backup.csv")

    return results


def cooling_testing(n,path,data_numbers,opt):

    results = {}
    number_of_instances = len(data_numbers)

    sumSA_geo_t = [0 for i in range(number_of_instances)]
    sumSA_lin_t= [0 for i in range(number_of_instances)]
    sumSA_log_t = [0 for i in range(number_of_instances)]
    sumSA_geo_e = [0 for i in range(number_of_instances)]
    sumSA_lin_e = [0 for i in range(number_of_instances)]
    sumSA_log_e = [0 for i in range(number_of_instances)]

    results["Problem size"] = []
    results["Simulated annealing - logarithmic time"] = []
    results["Simulated annealing - linear time"] = []
    results["Simulated annealing - geometric time"] = []
    results["Simulated annealing - logarithmic error"] = []
    results["Simulated annealing - linear error"] = []
    results["Simulated annealing - geometric error"] = []


    sum_index = 0

    for z in data_numbers:
        tsp = t.TSP()
        tsp.read_from_file(path+'data{}.txt'.format(z))

        sim_annealing = SA.SA(tsp)

        for i in range(n):
            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(7000,20000,"insert","random","geo",0.99,6)
            end1 = time.time()
            sumSA_geo_t[sum_index]+= end1-start1
            sumSA_geo_e[sum_index] += dist

            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(7000,20000,"insert","random","lin",2,6)
            end1 = time.time()
            sumSA_lin_t[sum_index]+= end1-start1
            sumSA_lin_e[sum_index] += dist

            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(7000,20000,"insert","random","log",2,6)
            end1 = time.time()
            sumSA_log_t[sum_index]+= end1-start1
            sumSA_log_e[sum_index] += dist


        results["Problem size"].append(z)

        results["Simulated annealing - geometric time"].append(sumSA_geo_t[sum_index]/n)
        results["Simulated annealing - linear time"].append(sumSA_lin_t[sum_index]/n)
        results["Simulated annealing - logarithmic time"].append(sumSA_log_t[sum_index]/n)
        results["Simulated annealing - geometric error"].append((((sumSA_geo_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Simulated annealing - linear error"].append((((sumSA_lin_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Simulated annealing - logarithmic error"].append((((sumSA_log_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)

        sum_index+=1

    return results

def temp_testing(n,path,data_numbers,opt):

    results = {}
    number_of_instances = len(data_numbers)

    sumSA_5000_t = [0 for i in range(number_of_instances)]
    sumSA_10000_t= [0 for i in range(number_of_instances)]
    sumSA_20000_t = [0 for i in range(number_of_instances)]
    sumSA_30000_t= [0 for i in range(number_of_instances)]
    sumSA_40000_t = [0 for i in range(number_of_instances)]
    sumSA_50000_t = [0 for i in range(number_of_instances)]

    sumSA_5000_e = [0 for i in range(number_of_instances)]
    sumSA_10000_e= [0 for i in range(number_of_instances)]
    sumSA_20000_e = [0 for i in range(number_of_instances)]
    sumSA_30000_e= [0 for i in range(number_of_instances)]
    sumSA_40000_e = [0 for i in range(number_of_instances)]
    sumSA_50000_e = [0 for i in range(number_of_instances)]

    results["Problem size"] = []
    results["Simulated annealing - 5000 time"] = []
    results["Simulated annealing - 10000 time"] = []
    results["Simulated annealing - 20000 time"] = []
    results["Simulated annealing - 30000 time"] = []
    results["Simulated annealing - 40000 time"] = []
    results["Simulated annealing - 50000 time"] = []

    results["Simulated annealing - 5000 error"] = []
    results["Simulated annealing - 10000 error"] = []
    results["Simulated annealing - 20000 error"] = []
    results["Simulated annealing - 30000 error"] = []
    results["Simulated annealing - 40000 error"] = []
    results["Simulated annealing - 50000 error"] = []


    sum_index = 0

    for z in data_numbers:
        tsp = t.TSP()
        tsp.read_from_file(path+'data{}.txt'.format(z))

        sim_annealing = SA.SA(tsp)

        for i in range(n):
            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(5000,20000,"insert","random","lin",2,6)
            end1 = time.time()
            sumSA_5000_t[sum_index]+= end1-start1
            sumSA_5000_e[sum_index] += dist

            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(10000,20000,"insert","random","lin",2,6)
            end1 = time.time()
            sumSA_10000_t[sum_index]+= end1-start1
            sumSA_10000_e[sum_index] += dist

            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(20000,20000,"insert","random","lin",2,6)
            end1 = time.time()
            sumSA_20000_t[sum_index]+= end1-start1
            sumSA_20000_e[sum_index] += dist

            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(30000,20000,"insert","random","lin",2,6)
            end1 = time.time()
            sumSA_30000_t[sum_index]+= end1-start1
            sumSA_30000_e[sum_index] += dist

            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(40000,20000,"insert","random","lin",2,6)
            end1 = time.time()
            sumSA_40000_t[sum_index]+= end1-start1
            sumSA_40000_e[sum_index] += dist

            start1 = time.time()
            dist , rt = sim_annealing.start_annealing(50000,20000,"insert","random","lin",2,6)
            end1 = time.time()
            sumSA_50000_t[sum_index]+= end1-start1
            sumSA_50000_e[sum_index] += dist

        results["Problem size"].append(z)

        results["Simulated annealing - 5000 time"].append(sumSA_5000_t[sum_index]/n)
        results["Simulated annealing - 10000 time"].append(sumSA_10000_t[sum_index]/n)
        results["Simulated annealing - 20000 time"].append(sumSA_20000_t[sum_index]/n)
        results["Simulated annealing - 30000 time"].append(sumSA_30000_t[sum_index]/n)
        results["Simulated annealing - 40000 time"].append(sumSA_40000_t[sum_index]/n)
        results["Simulated annealing - 50000 time"].append(sumSA_50000_t[sum_index]/n)

        results["Simulated annealing - 5000 error"].append((((sumSA_5000_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Simulated annealing - 10000 error"].append((((sumSA_10000_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Simulated annealing - 20000 error"].append((((sumSA_20000_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Simulated annealing - 30000 error"].append((((sumSA_30000_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Simulated annealing - 40000 error"].append((((sumSA_40000_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)
        results["Simulated annealing - 50000 error"].append((((sumSA_50000_e[sum_index]/n)-opt[sum_index])/opt[sum_index])*100)

        sum_index+=1

    return results

def make_figure_iterTS(df,main_title):

    x_axis = df["Problem size"]
    figure = go.Figure(layout=go.Layout(
        title=go.layout.Title(text=main_title),
        yaxis_title= "Średni błąd względny [%]",
        xaxis_title= "Liczba wierzchołków w grafie",
        font=dict(
        family="Courier New, monospace",
        size=20,
        color="#7f7f7f"
    )
    ))
    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - 1000 error"],
                        mode='markers+lines',
                        name='Tabu search - 1000',
                        marker = dict(size = 12)
                        ))


    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - 2000 error"],
                    mode='markers+lines',
                    name='Tabu search - 2000',
                    marker = dict(size = 12)
                    ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - 3000 error"],
                    mode='markers+lines',
                    name='Tabu search - 3000',
                    marker = dict(size = 12)
                    ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - 4000 error"],
                        mode='markers+lines',
                        name='Tabu search - 4000',
                        marker = dict(size = 12)
                        ))

    pio.write_html(figure, file='test_plot.html', auto_open=True)

    figure.show()


def make_figure_tabuTS(df,main_title):

    x_axis = df["Problem size"]
    figure = go.Figure(layout=go.Layout(
        title=go.layout.Title(text=main_title),
        yaxis_title= "Średni błąd względny [%]",
        xaxis_title= "Liczba wierzchołków w grafie",
        font=dict(
        family="Courier New, monospace",
        size=20,
        color="#7f7f7f"
    )
    ))
    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - 2 error"],
                        mode='markers+lines',
                        name='Tabu search - 2',
                        marker = dict(size = 12)
                        ))


    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - 3 error"],
                    mode='markers+lines',
                    name='Tabu search - 3',
                    marker = dict(size = 12)
                    ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - 4 error"],
                    mode='markers+lines',
                    name='Tabu search - 4',
                    marker = dict(size = 12)
                    ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - 5 error"],
                        mode='markers+lines',
                        name='Tabu search - 5',
                        marker = dict(size = 12)
                        ))

    pio.write_html(figure, file='test_plot.html', auto_open=True)

    figure.show()

def make_figure_time1(df,main_title):

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
    figure.add_trace(go.Scatter(x=x_axis, y=df["Simulated annealing - invert time"],
                        mode='markers+lines',
                        name='Simulated annealing - invert',
                        marker = dict(size = 12)
                        ))


    figure.add_trace(go.Scatter(x=x_axis, y=df["Simulated annealing - insert time"],
                    mode='markers+lines',
                    name='Simulated annealing - insert',
                    marker = dict(size = 12)
                    ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Simulated annealing - swap time"],
                    mode='markers+lines',
                    name='Simulated annealing - swap',
                    marker = dict(size = 12)
                    ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - list time"],
                        mode='markers+lines',
                        name='Tabu search - list',
                        marker = dict(size = 12)
                        ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - matrix insert time"],
                        mode='markers+lines',
                        name='Tabu search - matrix insert',
                        marker = dict(size = 12)
                        ))

    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - matrix invert time"],
                        mode='markers+lines',
                        name='Tabu search - matrix invert',
                        marker = dict(size = 12)
                        ))


    figure.add_trace(go.Scatter(x=x_axis, y=df["Tabu search - matrix swap time"],
                        mode='markers+lines',
                        name='Tabu search - matrix swap',
                        marker = dict(size = 12)
                        ))




    pio.write_html(figure, file='test_plot.html', auto_open=True)

    figure.show()




x = t.TSP()
x.read_from_file('data/dataEtap2/data13.txt')

# sim_ann = SA.SA(x)
# start = time.time()
# opt, route = sim_ann.start_annealing(7000,20000,"invert","greedy","lin",2,5)
# end = time.time()
# res = end-start
# print(opt, res, route)
#
# tabu_s = TS.TS(x)
# start = time.time()
# optTS, routeTS = tabu_s.start_search(3000,"greedy","invert",3,80)
# end = time.time()
# res = end-start
# print(optTS, res,routeTS)
# start = time.time()
# optTS2, routeTS2 = tabu_s.start_search_matrix(3000,"greedy","swap",3,80)
# end = time.time()
# res = end-start
# print(optTS2,res, routeTS2)
data = [11,13,14,16,17,18,21,24,26,29,34,39,42,48,53,58,65,70]
opt = [202,269,125,156,2085,187,2707,1272,937,1610,1286,1530,699,14422,6905,25395,1839,38673]

data2 = [11,13,14,16,17,18,21,24,26,29,34,39,42,48,53,58]
opt2 = [202,269,125,156,2085,187,2707,1272,937,1610,1286,1530,699,14422,6905,25395]

# result = time_testing( 1,  'data/dataEtap2/', data,opt)
cooling_result = cooling_testing( 20,  'data/dataEtap2/',data2,opt2)
print(cooling_result)
df = pd.DataFrame(cooling_result)
print(df.head())
df.to_csv("Etap2_cooling.csv")

iter_result = iterTS_testing( 20,  'data/dataEtap2/',data2,opt2)
print(iter_result)
df = pd.DataFrame(iter_result)
print(df.head())
df.to_csv("Etap2_TS_iter.csv")

tabu_result = tabuTS_testing( 20,  'data/dataEtap2/', data2,opt2)
print(tabu_result)
df = pd.DataFrame(tabu_result)
print(df.head())
df.to_csv("Etap2_TS_tabu.csv")

temp_result = temp_testing( 20,  'data/dataEtap2/', data2,opt2)
print(temp_result)
df = pd.DataFrame(temp_result)
print(df.head())
df.to_csv("Etap2_SA_temp.csv")

# make_figure_tabuTS(df,"Tabu length")

# df = pd.DataFrame(result)
# print(df.head())
# df.to_csv("Etap2_1.csv")
