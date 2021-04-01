import json
import time

from celery import Celery

from acovrp import AcoVrp
from functions import dataset

CELERY_ACCEPT_CONTENT = ['json', 'pickle']
app = Celery('tasks', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')
app.conf.update(CELERY_ACCEPT_CONTENT=['json', 'pickle'],
                CELERY_TASK_SERIALIZER='json',
                CELERY_RESULT_SERIALIZER='json',
                CELERY_TASK_TRACK_STARTED=True)


@app.task(name='mytask.regular_aco',bind=True)
def regular_aco(self,datasets, max_nfc, ants):
    vehicle_capacity, graph, delivery_demand, optimal = dataset(datasets)
    alpha = 2
    beta = 5
    sigma = 3
    rho = 0.8
    theta = 80
    num_ants = ants
    MAX_NFC = max_nfc
    start_time = time.time()
    vrp = AcoVrp(alpha, beta, sigma, rho, theta, num_ants, vehicle_capacity, delivery_demand, MAX_NFC)
    vrp.set_graph(graph)
    bestSol = vrp.process2()
    end_time = time.time()
    routes = bestSol[0]
    rs = []
    for route in routes:
        r = []
        for city in route:
            r.append(city.item())
        rs.append(r)
    result = {'cost': end_time - start_time, 'distance': bestSol[1], 'routes': rs}
    print('test:' + self.AsyncResult(self.request.id).state)
    return result
