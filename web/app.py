import os
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["routerlists"]
routerstatus = mydb["interface_status"]


@app.route("/")
def main():
    return render_template("index.html", data=list(mycol.find()))


@app.route("/router/<ip_address>")
def router_Status(ip_address):
    router_data = list(
        routerstatus.find({"router_ip": ip_address}).sort("_id", -1).limit(3)
    )
    return render_template(
        "router_detail.html", data=router_data, ip_address=ip_address
    )


@app.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    yourname = request.form.get("yourname")
    message = request.form.get("message")
    router_list = {"ip_address": ip, "username": yourname, "password": message}

    if (yourname and message) and ip:
        mycol.insert_one(router_list)
    return redirect(url_for("main"))


@app.route("/delete", methods=["POST"])
def delete_comment():
    doc_id = request.form.get("doc_id")
    if doc_id:
        try:
            mycol.delete_one({"_id": ObjectId(doc_id)})
        except Exception as e:
            print(f"Error deleting document: {e}")

    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
