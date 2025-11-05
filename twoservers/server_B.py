from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/new", methods = ["POST"])
def new_json():
    data = request.get_json()
    data["name"] = data["name"]+f" "+ data["surname"]
    del data["surname"]
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5001)