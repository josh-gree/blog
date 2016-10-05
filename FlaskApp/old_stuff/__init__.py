"""
This file is part of the flask+d3 Hello World project.
"""
import json
import flask
from flask import request, jsonify, abort, make_response, url_for
import numpy as np


app = flask.Flask(__name__)
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route("/")
def index():
    """
    When you request the root path, you'll get the index.html template.
    """
    return flask.render_template("index.html")

@app.route("/speeches/all")
def speeches():
    return flask.render_template("speeches_all.html")

@app.route("/speeches/labour")
def speeches_lab():
    return flask.render_template("speeches_lab.html")

@app.route("/speeches/conservative")
def speeches_con():
    return flask.render_template("speeches_con.html")

@app.route("/speeches/libdem")
def speeches_libdem():
    return flask.render_template("speeches_libdem.html")

@app.route('/api/v1.0/tasks', methods=['GET'])
#@auth.login_required
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

@app.route('/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


#@app.route("/data")
#@app.route("/data/<int:ndata>")
#def data(ndata=100):
#    """
#     On request, this returns a list of ``ndata`` randomly made data points.
#     :param ndata: (optional)
#         The number of data points to return.
#     :returns data:
#         A JSON string of ``ndata`` data points.
#     """
#     x = 10 * np.random.rand(ndata) - 5
#     y = 0.5 * x + 0.5 * np.random.randn(ndata)
#     A = 10. ** np.random.rand(ndata)
#     c = np.random.rand(ndata)
#     return json.dumps([{"_id": i, "x": x[i], "y": y[i], "area": A[i],
#         "color": c[i]}
#         for i in range(ndata)])

# @app.route("/gdata")
# @app.route("/gdata/<float:mux>/<float:muy>")
# def gdata(ndata=100,mux=.5,muy=0.5):
#     """
#     On request, this returns a list of ``ndata`` randomly made data points.
#     about the mean mux,muy
#     :param ndata: (optional)
#         The number of data points to return.
#     :returns data:
#         A JSON string of ``ndata`` data points.
#     """

#     x = np.random.normal(mux,.5,ndata)
#     y = np.random.normal(muy,.5,ndata)
#     A = 10. ** np.random.rand(ndata)
#     c = np.random.rand(ndata)
#     return json.dumps([{"_id": i, "x": x[i], "y": y[i], "area": A[i],
#         "color": c[i]}
#         for i in range(ndata)])

if __name__ == "__main__":
    app.run()
