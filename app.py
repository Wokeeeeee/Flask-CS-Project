import os

import numpy as np
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask.templating import render_template_string
from flask_cors import CORS

from astar import CostMap, A_star_path_planning
# from solve import *
from maxStream import *

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


# @app.route("/", methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         data = request.form.to_dict()
#         calculate_ds(data)
#         fast_calculate(data)
#         return render_template('solve.html', data=data)
#
#     else:
#         return render_template('index.html')


# @app.route("/simplex/direct", methods=['POST'])
# def simplexDirect():
#     data = request.get_json()
#     target = data.get("target")
#     matrix = data.get("matrix")
#     datar = format_date(target, matrix)
#     fast_r = fast_calculate(datar)
#     return jsonify({
#         'code': 200,
#         'message': fast_r["message"],
#         'status': fast_r["status"],
#         'x': fast_r["x"].tolist(),
#         'max': -fast_r["fun"],
#         'success': fast_r["success"]
#     })


@app.route("/astar", methods=['POST'])
def pathPlaning():
    data = request.get_json()
    size = data.get("size")
    src = data.get("src")
    des = data.get("des")
    blocks = data.get("blocks")
    astar_map = CostMap(np.zeros((size, size)))
    astar_map.obstacle_upload(blocks)
    path, close_list = A_star_path_planning(astar_map.map, src, des)
    return jsonify(
        {'path': path[1:-1],
         'close_list': close_list[1:-1]
         }
    )


#
# @app.route("/simplex/details", methods=['POST'])
# def simplexDetails():
#     data = request.get_json()
#     target = data.get("target")
#     matrix = data.get("matrix")
#     datar = format_date(target, matrix)
#     print(datar)
#     dset, oiset, format = solve(datar)
#     print(dset)
#     print(type(oiset))
#     print(format)
#     return jsonify({
#         'code': 200,
#         "format": format.tolist(),
#         "d_set": dset,
#         "oi_set": oiset
#     })


@app.route("/maxflow", methods=['POST'])
def maxFlowAndGraph():
    data = request.get_json()
    node_number = data.get("node_number")
    edges = data.get("edges")
    src = data.get("src")
    des = data.get("des")
    max_flow = MaxFlow(node_number)
    max_flow.init_residual(edges)
    result, max_graph = max_flow.maxflow(src, des)
    tuple_ = max_flow.transferToTuple() if result != 0 else []
    return jsonify({
        "result": result,
        "tuple": tuple_
    })


@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run()
