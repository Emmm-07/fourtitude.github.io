from flask import Flask, request, render_template



app = Flask(__name__)


@app.route('/')
def calculator():
    return render_template('calculator.html')


@app.route('/calculate', methods=['POST'])                  #a decorator used to define a route for handling HTTP POST requests to the '/calculate' URL path.
def calculate():
    num1 = float(request.form['num1'])                          #request.form()   para kunin yung variable num1 na nasa form
    num2 = float(request.form['num2'])
    operator = request.form['operator']

    result = 0

    if operator == 'add':
        result = num1 + num2
    elif operator == 'subtract':
        result = num1 - num2
    elif operator == 'multiply':
        result = num1 * num2
    elif operator == 'divide':
        if num2 != 0:
            result = num1 / num2
        else:
            return "Error: Cannot divide by zero!"
    print(f'hello {num1} + {num2} = {result}')
    print(num1, "+", num2, " = ", result)
    return render_template('calculator.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)