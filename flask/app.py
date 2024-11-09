from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

units = {
    "temperature": ["Celsius", "Fahrenheit", "Kelvin"],
    "distance": ["meters", "kilometers", "miles"],
    "weight": ["grams", "kilograms", "pounds"],
    "energy": ["joules", "kilojoules", "calories"],
    "time": ["seconds", "minutes", "hours"],
    "speed": ["mps", "kmph", "mph"],
    "volume": ["liters", "milliliters", "gallons"],
}

def convert_unit(category, value, from_unit, to_unit):
    conversion_factors = {
        "distance": {"meters": 1, "kilometers": 0.001, "miles": 0.000621371},
        "weight": {"grams": 1, "kilograms": 0.001, "pounds": 0.00220462},
        "energy": {"joules": 1, "kilojoules": 0.001, "calories": 0.239006},
        "time": {"seconds": 1, "minutes": 1/60, "hours": 1/3600},
        "speed": {"mps": 1, "kmph": 3.6, "mph": 2.23694},
        "volume": {"liters": 1, "milliliters": 1000, "gallons": 0.264172},
    }

    if category == "temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return value * 9/5 + 32
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        else:
            return value

    return value * (conversion_factors[category][to_unit] / conversion_factors[category][from_unit])

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        category = request.form['category']
        value = float(request.form['value'])
        from_unit = request.form['from_unit']
        to_unit = request.form['to_unit']
        result = round(convert_unit(category, value, from_unit, to_unit), 4)
    return render_template('index.html', result=result, units=units)

@app.route('/get_units/<category>', methods=['GET'])
def get_units(category):
    return jsonify(units.get(category, []))

if __name__ == '__main__':
    app.run(debug=True)
