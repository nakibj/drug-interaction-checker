from flask import Flask, render_template, request
from drug_checker import check_interactions

app = Flask(__name__)

@app.route('/')

def home():
    return render_template('index.html')

@app.route('/check', methods = ['POST'])
def check():
    drug_a = request.form['drug_a']
    drug_b = request.form['drug_b']

    result = check_interactions(drug_a, drug_b)

    return render_template('results.html', result = result)

if __name__ == '__main__':
    app.run(debug = True)