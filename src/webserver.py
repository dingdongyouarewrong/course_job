from flask import Flask, request, jsonify
from src.recommendations_package.get_rec import get_user_recomendations
from src.recommendations_package.database_utils import get_connection

app = Flask(__name__)
from flask_cors import CORS
CORS(app)


@app.route("/get_rec", methods=["POST","GET"])
def get_rec():
    data = request.get_json()
    if int(data.get("user_id"))<0 or int(data.get("user_id"))>100:
        return jsonify("WRONG NUMBER")
    response = jsonify(get_user_recomendations(data.get("user_id")))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # try:
    #     data = request.get_json()
    #     response = jsonify(get_user_recomendations(data.get("user_id")))
    #     response.headers.add('Access-Control-Allow-Origin', '*')
    #     return response
    # except Exception:
    #     response = jsonify("")
    #     response.headers.add('Access-Control-Allow-Origin', '*')
    #     return response
    # return jsonify(get_user_recomendations(data.get("user_id")))


@app.route("/set_rate", methods=["POST"])
def set_rate():
    data = request.get_json()
    rate = data.get("rate")
    user_id = data.get("user_id")
    obj_id = data.get("obj_id")
    obj_title = data.get("obj_title")
    conn = get_connection()
    cursor = conn.cursor()
    print(cursor.execute("select * from rates").fetchall()[0])
    q = "INSERT INTO rates (rate, user_id, obj_id, obj_title) VALUES('{}', '{}', '{}', '{}')".format(
        rate, user_id, obj_id, obj_title
    )
    cursor.execute(q)
    q = "SELECT * FROM rates WHERE user_id=555"
    cursor.execute(q)
    print(cursor.fetchall())
    cursor.close()

    return jsonify("now it's really good")


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
