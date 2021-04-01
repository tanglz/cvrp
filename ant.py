import numpy as np

class Ant:
    startPoint = 1
    vertices = list()
    edges = {}
    pheromones = {}
    maxCapacity = 0
    demand = 0

    alpha = 0
    beta = 0

    solution = list()

    def __init__(self, vertices, edges, maxCapacity, demand, pheromones, alpha, beta, startPoint=1):
        self.startPoint = startPoint
        self.vertices = vertices
        self.edges = edges
        self.maxCapacity = maxCapacity
        self.demand = demand
        self.pheromones = pheromones
        self.alpha = alpha
        self.beta = beta
        self.solution = list()

    def get_solution(self):
        """
        State transition
        """
        # print('Run task (%s)...' % os.getpid())
        path_list = list()
        while len(self.vertices) > 0:
            path = list()
            city = np.random.choice(self.vertices)
            capacity = self.maxCapacity - self.demand[city]

            path.append(city)
            self.vertices.remove(city)

            while len(self.vertices) > 0:
                prob = list()
                for x in self.vertices:
                    p = ((self.pheromones[(min(x, city), max(x, city))]) ** self.alpha) * (
                            (1 / self.edges[(min(x, city), max(x, city))]) ** self.beta)
                    prob.append(p)

                probability = (prob / np.sum(prob))

                city = np.random.choice(self.vertices, p=probability)
                capacity = capacity - self.demand[city]

                if capacity > 0:
                    path.append(city)
                    self.vertices.remove(city)
                else:
                    break
            path_list.append(path)

        """
            get total distance
        """
        distance = 0
        for i in path_list:
            a = self.startPoint
            for j in i:
                b = j
                distance = distance + self.edges[(min(a, b), max(a, b))]
                a = b
            b = 1
            distance = distance + self.edges[(min(a, b), max(a, b))]

        self.solution = (path_list, distance)
        return self.solution
