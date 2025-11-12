import json

from flask import Flask, jsonify, request
import psycopg2
app = Flask(__name__)

def connect():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432,
    )


@app.route("/table", methods =["GET"])
def create_table():
    base = connect()
    cursor = base.cursor()
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS firsttable(
             id SERIAL PRIMARY KEY,
             data TEXT
              )
              """)
    base.commit()
    base.close()
    return jsonify({"message":"super"})

@app.route("/new", methods = ["POST"])
def new_json():
    data = request.get_json()
    data["name"] = data["name"]+f" "+ data["surname"]
    del data["surname"]

    base = connect()

    cursor = base.cursor()
    cursor.execute("INSERT INTO firsttable(data) VALUES(%s)", (json.dumps(data), ))
    base.commit()
    base.close()
    return jsonify(data)

@app.route("/el", methods = ["GET"])
def get_el():
    try:
        id = request.args.get("id")
        base = connect()
        curr = base.cursor()
        if id is None:
            curr.execute("SELECT * FROM firsttable")
            data = curr.fetchall()
            results = {}
            for i in data:
                results[i[0]] = json.loads(i[1])
            return jsonify(results)

        curr.execute("SELECT * FROM firsttable WHERE id = %s", (int(id),))
        data = curr.fetchone()
        base.close()
        result = json.loads(data[1])
        return jsonify(result)
    except Exception as e:
        return jsonify({"message":str(e)})

@app.route("/del", methods = ["POST"])
def del_el():
    id = request.args.get("id")
    base = connect()
    curr = base.cursor()
    curr.execute("DELETE FROM firsttable WHERE id = %s", (int(id),))
    base.commit()
    base.close()
    return jsonify({"message":"deleted"})


if __name__ == "__main__":
    app.run(port=5001)