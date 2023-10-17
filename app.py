from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('bmi_calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    height = float(request.form.get('height')) / 100  # convert cm to meters
    weight = float(request.form.get('weight'))
    bmi = round(weight / (height**2), 2)
    return render_template('bmi_calculator.html', bmi=bmi)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)