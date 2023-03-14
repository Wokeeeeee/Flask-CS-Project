import os
import webbrowser

import numpy as np
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask.templating import render_template_string
from flask_cors import CORS

from astar import CostMap, A_star_path_planning
from lanchest import lanchestLaw
from shortestPath import *
from simplex import *
from maxStream import *
from transportation import *
from counterStrategy import *



app = Flask(__name__)
CORS(app, resources=r'/*', supports_credentials=True)


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route("/simplex/direct", methods=['POST'])
def simplexDirect():
    data = request.get_json()
    target = data.get("target")
    matrix = data.get("matrix")
    datar = format_date(target, matrix)
    fast_r = fast_calculate(datar)
    # 如果有可行解再求解，没有就算了
    print(type(fast_r["status"]))
    print(fast_r["status"] == 0)

    dset, oiset, format = [], [], []
    if fast_r["status"] == 0:
        dset, oiset, format = solve(datar)
    # dset=deformat_data(dset)
    # 转一下dset的数据结构
    return jsonify({
        'code': 200,
        'message': fast_r["message"],
        'status': fast_r["status"],
        'x': np.round(fast_r["x"], 2).tolist(),
        'max': -fast_r["fun"],
        'success': fast_r["success"],
        "format": format,
        "d_set": dset,
        "oi_set": oiset
    })


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


@app.route("/simplex/details", methods=['POST'])
def simplexDetails():
    data = request.get_json()
    target = data.get("target")
    matrix = data.get("matrix")
    datar = format_date(target, matrix)
    print(datar)
    dset, oiset, format = solve(datar)
    print(dset)
    print(type(oiset))
    print(format)
    return jsonify({
        'code': 200,
        "format": format.tolist(),
        "d_set": dset,
        "oi_set": oiset
    })


@app.route("/maxflow", methods=['POST'])
def maxFlowAndGraph():
    data = request.get_json()
    node_number = int(data.get("node_number"))
    edges = transferStrToInt(data.get("edges"))
    src = int(data.get("src"))
    des = int(data.get("des"))
    max_flow = MaxFlow(node_number)
    max_flow.init_residual(edges)
    result, max_graph, r_set = max_flow.maxflow(src, des)
    tuple_ = max_flow.transferToTuple() if result != 0 else []
    return jsonify({
        "result": result,
        "tuple": tuple_,
        "r_set": r_set
    })


@app.route("/shortestPath", methods=['POST'])
def shortestPath():
    # #     start = '1'
    # #     goal = '6'
    # #     dijk = Dijkstra(g, start, goal)
    # #     print(dijk.shortest_path())
    data = request.get_json()
    edges = data.get("edges")
    src = data.get("src")
    des = data.get("des")
    dijk = Dijkstra(data_format(edges), src, des)
    path, min, opens, closes = dijk.shortest_path()
    return jsonify({
        "path": path,
        "min": min,
        "opens": opens,
        "closes": closes
    })


@app.route("/transportation", methods=['POST'])
def transportationProblem():
    data = request.get_json()
    matrix = data.get("matrix")
    [c, a, b] = TP_split_matrix(matrix)
    c, x, total_cost, x_set, message_set, c_set = TP_vogel([c, a, b])
    # [c,x]=TP_vogel([c,a,b])
    s, message = TP_potential(c, x)
    # 暂时没有想好迭代表该怎么传回去
    success = s is not None
    return jsonify({
        "success": success,
        "message": message,
        "cost": total_cost,
        "matrix": x.tolist(),
        "x_set": x_set,
        "message_set": message_set,
        "c_set": c_set
    })


@app.route("/counter", methods=['POST'])
def counterStrategy():
    data = request.get_json()
    matrix = data.get("matrix")
    method = data.get("method")
    result, message, col, row = [], '', [], []
    if method == "pure":
        # (1, (0, 1))
        result, col, row, message = bestPure(matrix)
    elif method == "mixed":
        # [[ 7.  3. -1.]
        #  [ 4.  6. -1.]
        #  [ 1.  1.  0.]]
        result, col, row = bestMixed(matrix)
        message = "解答成功"

    return jsonify({
        "result": result,
        "message": message,
        "col": col,
        "row": row
    })


@app.route("/lanchester", methods=['POST'])
def lanchesterLaw():
    data = request.get_json()
    R0 = float(data.get("R0"))
    B0 = float(data.get("B0"))
    a = float(data.get("a"))
    b = float(data.get("b"))
    mode = data.get("mode")
    winner, R, B, t = lanchestLaw(R0, B0, a, b, mode)
    return jsonify({
        "winner": winner,
        "R": R,
        "B": B,
        "t": int(t)
    })


@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500


if __name__ == "__main__":
    webbrowser.open('http://localhost:5000')
    app.run(host='localhost', port=5000)
