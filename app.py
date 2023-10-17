from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('bmi_calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    height_in_meters = float(request.form.get('height')) / 100  # convert cm to meters
    weight = float(request.form.get('weight'))
    target_bmi = float(request.form.get('target_bmi'))

    bmi = round(weight / (height_in_meters**2), 2)

    # Calculate the weight for the target BMI using the formula: weight = BMI * height^2
    target_weight = target_bmi * (height_in_meters**2)
    difference = round(target_weight - weight, 2)

    return render_template('bmi_calculator.html', bmi=bmi, target_bmi=target_bmi, difference=difference)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)