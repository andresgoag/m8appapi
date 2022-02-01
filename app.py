from bson.json_util import dumps, ObjectId
from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from flask_cors import CORS
from config import Config

from datetime import datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    mongo = PyMongo(app)

    @app.route('/test')
    def test():
        res = {"data": "Test message, api is working"}
        return jsonify(res), 200

    @app.route("/add_application", methods=['POST'])
    def add_application():
        data = request.get_json()
        data['status'] = "new"
        data['date'] = datetime.now().strftime("%Y-%m-%d")
        result = mongo.db.applications.insert_one(data)
        return jsonify({"id": str(result.inserted_id)})

    @app.route("/get_applications")
    def get_applications():
        result = mongo.db.applications.find({})
        return Response(dumps(result), mimetype='application/json')

    @app.route("/update_application", methods=["PUT"])
    def update_application():
        data = request.get_json()
        mongo.db.applications.update_one({'_id':ObjectId(data['id'])}, {"$set": {"status": data['action']}})
        return jsonify(result="ok")

    @app.route("/delete_application", methods=["DELETE"])
    def delete_application():
        data = request.get_json()
        print(data)
        mongo.db.applications.delete_one({'_id':ObjectId(data['id'])})
        return jsonify(result="ok")

    return app