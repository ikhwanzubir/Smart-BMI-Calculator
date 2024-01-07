from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', target_bmi=26.9)

@app.route('/panduan')
def panduan():
    return render_template('panduan.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/calculate', methods=['POST', 'GET'])
def calculate():
    try:
        height_in_cm = float(request.form.get('height'))  # convert cm to meters
        weight = float(request.form.get('weight'))
        target_bmi = float(request.form.get('target_bmi', 26.9))
    except (TypeError, ValueError):
        errormessage = "Sila isi tinggi dan berat"
        return render_template('index.html', errormessage=errormessage, target_bmi=26.9)

    height_in_meters = height_in_cm / 100

    bmi = round(weight / (height_in_meters**2), 2)

    mustgain = 0
    needtolose = 0
    cangain = 0
    cangainpercent = 0

    if bmi < 18.5:
      target_bmi_underweight = 18.5
      target_weight = target_bmi_underweight * (height_in_meters**2)
      target_weight_round = round(target_weight, 2)
      mustgain = round(target_weight - weight, 1)

      return render_template('index.html', height=height_in_cm, 
                           weight=weight, bmi=bmi, target_bmi=target_bmi_underweight,  
                           target_weight_round=target_weight_round, mustgain=mustgain)

    else:
      target_weight = target_bmi * (height_in_meters**2)
      target_weight_round = round(target_weight, 2)

      if target_weight > weight:
        needtolose = round(target_weight - weight, 1)

      if weight > target_weight:
        cangain = round(weight - target_weight, 1)
        cangainpercent = round((cangain / weight) * 100, 1)

      return render_template('index.html', height=height_in_cm, 
                           weight=weight, bmi=bmi, target_bmi=target_bmi,  
                           target_weight_round=target_weight_round, needtolose=needtolose,
                           cangain=cangain, cangainpercent=cangainpercent)
    
@app.route('/calculatetarget', methods=['POST', 'GET'])
def calculate_target():
    data = request.json

    # Extract and convert data
    height_in_cm = float(data.get('height'))  # Convert string to float
    weight = float(data.get('weight'))
    target_bmi = float(data.get('target_bmi', 26.9))

    height_in_meters = height_in_cm / 100

    target_weight = target_bmi * (height_in_meters ** 2)
    cangain = round(weight - target_weight, 1)

    selected_date_str = data['date']

    # Convert selected_date_str to a datetime object
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")

    selected_date_str_formatted = selected_date.strftime("%d-%m-%Y")

    # Calculate the number of weeks from today until selected_date
    today = datetime.today()
    delta = selected_date - today
    weeks = delta.days / 7

    daysneededminimal = 0
    minimaldate = 0

    if weeks <= 0:
        return jsonify({"error": "Sila pilih tarikh"})

    html_response = "html response"  # Initialize html_response
    html_minimaldate = "html minimal date"  # Initialize html_minimaldate

    # Calculate weight to lose per week
    weight_per_week = cangain / weeks

    if weight_per_week > 1.0:
      daysneededminimal = round(cangain / (1/7))
      minimaldate = today + timedelta(days=daysneededminimal)
      minimaldate_formatted = minimaldate.strftime("%d-%m-%Y")
      html_minimaldate = f"Tarikh yang dipilih tidak optimum.<br>Tarikh yang optimum ialah pada<br>{minimaldate_formatted} ({daysneededminimal} hari lagi)<br>dengan kadar penurunan 0.5 hingga 1.0 kg seminggu"
      html_response = ""
    else:
       html_response = f"Tarikh pilihan: {selected_date_str_formatted}<br>Hari tinggal: {delta.days}<br>Berat mesti diturunkan setiap minggu: {weight_per_week:.2f} kg"
       html_minimaldate = ""

    return jsonify(html=html_response, htmlminimaldate=html_minimaldate)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)