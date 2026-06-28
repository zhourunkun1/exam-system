from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

BANK = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    return jsonify({"msg": "ok", "your_answers": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
