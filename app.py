from flask import Flask,render_template,request
from dotenv import load_dotenv
from pathlib import Path
from flask_pymongo import PyMongo
import os
from json import dumps
import dns
env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

app.config["MONGO_URI"]=os.getenv("MONGO_URI")
mongo = PyMongo(app)
table = mongo.db.paxkage_list
#home page declaration
@app.route('/')
def Home():
    return render_template("index.html")
#result page for searched item
@app.route('/result',methods=["POST","GET"])
def result_func():
    #get input from form   
    name=request.form.get("libname")
    result=table.find({"Name":name})
    result_list = []
    for item in result:
        result_list.append(item)
    print(result_list)
    return render_template("result.html",name=name,result_list=result_list)
@app.route('/addonlyforadmin',methods=["POST","GET"])
def add():
    Name = request.form.get("Name")
    version = request.form.get("version")
    added = request.form.get("added")
    dropped = request.form.get("dropped")
    obj = {
        "Name" : Name,
        "version" : version,
        "added" : added,
        "dropped" : dropped
    }
    table.insert_one(obj)
    return render_template("add.html")

if __name__=="__main__":
    app.run(host="0.0.0.0",port="5002",debug=True)