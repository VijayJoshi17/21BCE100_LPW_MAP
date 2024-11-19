from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
from pymongo import MongoClient

app = Flask(__name__)
database_name = "mydb"
mongo_uri = "mongodb+srv://21bce100:Vijay123@cluster0.535qw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)

db = client[database_name]

@app.route('/create', methods=["POST"]) 
def create():
    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")
    db.exam.insert_one({"name": name, "age": age, "gender": gender})
    return jsonify({"code": 200, "response": "Account created"})

@app.route("/readall", methods=["GET"])
def readall():
    data = db.exam.find({}, {"_id": 0})
    return jsonify({"code": 200, "response": list(data)})

@app.route("/read", methods=["GET"])
def read():
    name = request.args.get("name")  
    data = db.exam.find({'name': name}, {"_id": 0})
    return jsonify({"code": 200, "response": list(data)})

@app.route('/update', methods=["PUT", "POST"])
def update():
    name = request.form.get("name")
    data = db.exam.find_one({'name': name})
    if data:
        age = request.form.get("age")
        db.exam.update_one({'name': name}, {'$set': {'age': age}})
        return jsonify({"code": 200, "response": "Account updated"})
    else:
        return jsonify({"code": 404, "response": "Account not found"})

@app.route('/delete', methods=["DELETE", "POST"])
def delete():
    name = request.form.get("name")
    data = db.exam.find_one({'name': name})
    if data:
        db.exam.delete_one({'name': name})
        return jsonify({"code": 200, "response": "Account deleted"})
    return jsonify({"code": 404, "response": "Account not found"})

@app.teardown_appcontext
def close_client(exception):
    client.close()

if __name__ == '__main__':
    app.run(debug=True)
