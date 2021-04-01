import redis
from celery import Celery, states
from flask import Flask, request, url_for, redirect
from flask import render_template

from db_connector import init_db
from functions import dataset, plot_paths, show_routes
from models.task import Task

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'db+mysql://lisa:123456@localhost:3306/cvrp?charset=utf8mb4'

app.config['CELERY_ACCEPT_CONTENT'] = ['json', 'pickle']
app.config['CELERY_TASK_SERIALIZER'] = 'json'
app.config['CELERY_RESULT_SERIALIZER'] = 'json'
app.config['CELERY_TASK_TRACK_STARTED'] = True

celery = Celery('tasks', broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)


@app.context_processor
def host():
    return dict(host="http://127.0.0.1:5000/")


@app.route('/', methods=['GET'])
def welcome():
    return render_template('welcome.html')


@app.route('/ds/example', methods=['GET'])
def example():
    return render_template('/ds/example.html')


@app.route('/task/list', methods=['GET'])
def task_list():
    t = Task()
    res = t.query_all()
    return render_template('/task/list.html', tasks=res)


@app.route('/task/run', methods=['GET'])
def task_run():
    return render_template('/task/run.html')


@app.route('/result/display/<name>', methods=['GET'])
def result_display(name=None):
    # name = request.form['name']
    t = Task()
    task_list = t.query_by_name(name)
    page_result = list()
    for task in task_list:
        ds = task.dataset
        task_id = task.task_id
        res = celery.AsyncResult(task_id)
        result = res.result
        if result is None:
            print('not finished')
            continue
        routes = result['routes']
        image = show_routes(ds, routes, str(task_id))
        page_result.append({'url': 'img/' + image, 'result': result, 'task_id': task_id, 'ds': ds})
    return render_template('/result/display.html', page_result=page_result)


@app.route('/add_task', methods=['POST'])
def add_task():
    name = request.form['name']
    ds = request.form['dataset']
    max_nfc = int(request.form['max_nfc'])
    ants = int(request.form['ants'])
    for i in range(2):
        task = celery.send_task('mytask.regular_aco', args=[ds, max_nfc, ants])
        task_id = task.id
        if len(str(task_id)) > 0:
            t = Task(dataset=ds, max_nfc=int(max_nfc), ants=ants, status='INITIAL', strategy='multiprocessor', task_id=task_id,name =name)
            t.insert()
    return redirect(url_for('task_list'))


@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html')


@app.route('/add_task_performance_test', methods=['POST'])
def add_task_performance_test():
    tasks_number = int(request.form['tasks_number'])
    ds = request.form['dataset']
    max_nfc = int(request.form['max_nfc'])
    ants = int(request.form['ants'])
    for i in range(tasks_number):
        celery.send_task('mytask.regular_aco', args=[ds, max_nfc, ants])
    return 'success'

if __name__ == '__main__':
    init_db()
    app.run()
