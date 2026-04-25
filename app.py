from flask import Flask, render_template, request, jsonify
from sympy.logic.boolalg import truth_table, SOPform
from sympy.abc import A, B, C, D
from sympy import sympify

app = Flask(__name__)

def get_vars(num_vars):
    return [A, B] if num_vars == 2 else [A, B, C] if num_vars == 3 else [A, B, C, D]

def get_truth_table(expr_str, num_vars):
    variables = get_vars(num_vars)
    expr = sympify(expr_str)
    table = []
    for combo in truth_table(expr, variables):
        inputs = list(combo[0])
        output = int(bool(combo[1]))
        table.append(inputs + [output])
    return table

def minimize(table, num_vars):
    variables = get_vars(num_vars)
    ones = [i for i, row in enumerate(table) if row[-1] == 1]
    if not ones:
        return "0"
    if len(ones) == len(table):
        return "1"
    return str(SOPform(variables, ones))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    data = request.json
    expr_str = data['expression']
    num_vars = int(data['num_vars'])
    try:
        table = get_truth_table(expr_str, num_vars)
        minimized = minimize(table, num_vars)
        return jsonify({
            'table': table,
            'minimized': minimized,
            'num_vars': num_vars
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)