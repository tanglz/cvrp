import time
from acovrp import AcoVrp
from functions import dataset, plot_paths
from multiprocessing import Pool
import numpy as np


if __name__ == '__main__':
    """
    PARAMS
    alpha:  relative importance of pheromone
    beta:   relative importance of heuristic information 
    sigma:  
    rho:    pheromone coefficient
    theta:
    num_ants: number of ants
    MAX_NFC: max number of function calls
    """

    vehicle_capacity, graph, delivery_demand, optimal = dataset('E-n101-k14.txt')
    alpha = 2
    beta = 5
    sigma = 3
    rho = 0.8
    theta = 80
    num_ants = 10
    MAX_NFC = 1
    start_time = time.time()
    vrp = AcoVrp(alpha, beta, sigma, rho, theta, num_ants, vehicle_capacity, delivery_demand, MAX_NFC)
    vrp.set_graph(graph)
    bestSol = vrp.process2()
    end_time = time.time()
    print(end_time - start_time)
    if bestSol is not None:
        plot_paths(graph, bestSol)
