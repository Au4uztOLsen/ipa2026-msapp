from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId
app = Flask(__name__)

client = MongoClient("mongodb://mongo:27017/")
mydb = client["mydatabase"]
mycol = mydb["routerlists"]

@app.route("/")
def main():
    return render_template("index.html", data=list(mycol.find()))

@app.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    yourname = request.form.get("yourname")
    message = request.form.get("message")
    router_list = {"ip_address": ip,"username": yourname,"password": message}

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