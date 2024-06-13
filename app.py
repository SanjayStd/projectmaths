from flask import Flask, render_template, request, redirect, url_for
import sympy as sp
from math import sin, cos, tan, acos, asin, atan, cosh, sinh, tanh

app = Flask(__name__)

def symbolic_partial_differentiation(expression, variables):
    symbols = sp.symbols(variables)
    expr = sp.sympify(expression)
    derivatives = {}
    for var in variables:
        derivative = sp.diff(expr, var)
        derivatives[var] = derivative
    return derivatives

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def evaluate_expression(expression, x):
    sympy_expression = sp.sympify(expression)  # Convert the expression to a sympy expression
    return sympy_expression.evalf(subs={'x': x})

def evaluate_expression_derivative(expression, x):
    return sp.diff(expression, 'x').subs('x', x)

def newton_raphson_method(func, func_derivative, initial_guess, decimal_places, tolerance=1e-6, max_iterations=1000):
    x0 = initial_guess
    for _ in range(max_iterations):
        fx0 = func(x0)
        if abs(fx0) < tolerance:
            return round(x0, decimal_places)
        fprime_x0 = func_derivative(x0)
        if fprime_x0 == 0:
            print("Derivative is zero. Newton-Raphson method failed.")
            return None
        x1 = x0 - fx0 / fprime_x0
        if abs(x1 - x0) < tolerance:
            return round(x1, decimal_places)
        x0 = x1
    print("Newton-Raphson method did not converge within the maximum number of iterations.")
    return None

@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        expression = request.form['expression']
        decimal_places = int(request.form['decimal_places'])
        
        partial_derivatives = symbolic_partial_differentiation(expression, ['x'])
        
        while True:
            try:
                start = 0
                end = 100
                step = 1
                break
            except ValueError:
                print("Invalid input. Please enter a valid floating-point number.")

        midpoints = []

        prev_x = None
        prev_sign = None
        for x in range(int(start / step), int(end / step)):
            x_value = x * step
            current_value = evaluate_expression(expression, x_value)
            current_sign = sign(eval(str(current_value)))

            if prev_sign is not None and prev_sign != current_sign:
                if prev_x is not None:
                    midpoint = (prev_x + x_value) / 2
                    midpoints.append(midpoint)
                    break
                else:
                    print(f"Sign change detected at x = {x_value}")

            prev_x = x_value
            prev_sign = current_sign

        roots = []
        for midpoint in midpoints:
            root = newton_raphson_method(lambda x: evaluate_expression(expression, x),
                                          lambda x: evaluate_expression_derivative(expression, x),
                                          midpoint, decimal_places)
            if root is not None:
                roots.append(root)

        if not roots:
            return render_template('result.html', partial_derivatives=partial_derivatives, decimal_places=decimal_places, roots=roots, no_roots=True)
        else:
            return render_template('result.html', partial_derivatives=partial_derivatives, decimal_places=decimal_places, roots=roots, no_roots=False)

@app.route('/', methods=['GET'])
def index():
    return render_template('ui.html')

@app.errorhandler(NameError)
def handle_name_error(e):
    error_message = "NameError: name 'e' is not defined"
    return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
