from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route("/get", methods = ["POST"])
def return_data():
    data = request.get_json()
    answer = requests.post("http://127.0.0.1:5001/new", json=data)
    new_data = answer.json()
    return jsonify(new_data)

if __name__ == "__main__":
    app.run(port=5000)
