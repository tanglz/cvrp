import asyncio
import time
from concurrent import futures
import billiard as multiprocessing
from ant import Ant
from functions import get_euclidean_distance


class AcoVrp:
    alpha = 2
    beta = 5
    sigma = 3
    rho = 0.8
    theta = 80
    num_ants = 2
    vehicle_capacity = 0
    delivery_demand = {}
    MAX_NFC = 100
    graph = {}
    pheromones = {}
    bestSolution = None

    def __init__(self, alpha, beta, sigma, rho, theta, num_ants, vehicle_capacity, delivery_demand, MAX_NFC):
        self.MAX_NFC = MAX_NFC
        self.num_ants = num_ants
        self.theta = theta
        self.rho = rho
        self.sigma = sigma
        self.beta = beta
        self.alpha = alpha
        self.vehicle_capacity = vehicle_capacity
        self.delivery_demand = delivery_demand

    def set_graph(self, graph):
        self.graph = graph

    def prepare_graph(self):
        vertices = list(self.graph.keys())
        vertices.remove(1)  # use 1 as deport

        edges = {}
        for pointA in self.graph.keys():
            for pointB in self.graph.keys():
                edges[(pointA, pointB)] = get_euclidean_distance(self.graph[pointA][0], self.graph[pointB][0],
                                                                 self.graph[pointA][1], self.graph[pointB][1])

        return vertices, edges

    def init_pheromone(self):

        pheromones = {}
        for p in self.graph.keys():
            for q in self.graph.keys():
                pheromones[(p, q)] = 1

        self.pheromones = pheromones
        return pheromones

    def sort_list(self, x):
        return x[1]

    def process(self):
        print(f"started at {time.strftime('%X')}")
        vertices, edges = self.prepare_graph()
        self.init_pheromone()
        NFC = 0
        # bestSol = None
        while (NFC < self.MAX_NFC):
            sols = list()
            # run per each ant
            for i in range(self.num_ants):
                ant = Ant(vertices.copy(), edges, self.vehicle_capacity, self.delivery_demand, self.pheromones, self.alpha,
                          self.beta)
                solution = ant.get_solution()
                sols.append(solution)
            self.update_bestSolution(sols)
            self.update_pheromone(sols)
            # print("generation:", NFC, " best:", int(self.bestSolution[1]), " path:", str(self.bestSolution[0]))
            NFC += 1
        print(f"finished at {time.strftime('%X')}")
        return self.bestSolution

    def process2(self):
        print(f"started at {time.strftime('%X')}")
        vertices, edges = self.prepare_graph()
        self.init_pheromone()
        NFC = 0
        p = multiprocessing.Pool(5)
        while NFC < self.MAX_NFC:
            sols = list()
            # start multi-processor
            sols = p.apply(self.group_ant_move, args=[vertices, edges, sols])
            # end
            self.update_bestSolution(sols)
            self.update_pheromone(sols)
            NFC += 1
        p.close()
        p.join()
        print(f"finished at {time.strftime('%X')}")
        return self.bestSolution

    def group_ant_move(self, vertices, edges, sols):
        group = int(self.num_ants/5)
        if group < 10:
            group = 10
        for i in range(group):
            ant = Ant(vertices.copy(), edges, self.vehicle_capacity, self.delivery_demand, self.pheromones, self.alpha,
                      self.beta)
            solution = ant.get_solution()
            sols.append(solution)
        return sols

    def update_pheromone(self, sols):
        """
        Update pheromones
        """
        sum = 0
        for i in sols:
            sum += i[1]
        avgSol = sum / len(sols)

        newPheromones = {}
        for (key, value) in self.pheromones.items():
            newPheromones[key] = (self.rho + self.theta / avgSol) * value

        # sort by total distance
        sols.sort(key=self.sort_list)

        if self.bestSolution is not None:
            for path in self.bestSolution[0]:
                for i in range(len(path) - 1):
                    newPheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))] = self.sigma / self.bestSolution[1] + newPheromones[min(path[i], path[i + 1]), max( path[i], path[i + 1])]
        # length of sols must greater than sigma
        for l in range(self.sigma):
            paths = sols[l][0]
            distance = sols[l][1]
            for path in paths:
                for i in range(len(path) - 1):
                    newPheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))] = (self.sigma - (l + 1) / distance ** (l + 1)) + newPheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))]

        self.pheromones = newPheromones

    def update_bestSolution(self, sols):
        # sort by total distance
        sols.sort(key=self.sort_list)
        if self.bestSolution is not None:
            if sols[0][1] < self.bestSolution[1]:
                self.bestSolution = sols[0]
        else:
            self.bestSolution = sols[0]
