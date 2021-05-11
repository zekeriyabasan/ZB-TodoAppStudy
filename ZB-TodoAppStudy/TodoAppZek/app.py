from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
from flask_pymongo import PyMongo
import json
import os
import datetime

from bson.objectid import ObjectId
from flask import jsonify, request

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/todo"
mongo = PyMongo(app)

title = "TODO sample application with Flask and MongoDB"
heading = "ZB TODOAPP-- "

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.mymongodb    #Select the database
todos = db.todo #Select the collection name
def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')

#----------------------------CRUD
#OPERATIONS-------------------------------------

#----------------------------GET TODOS----------------------------
@app.route("/getTodos", methods=['GET'])
def getTodos():
	Todos = todos.find()
	todoList = []

	for todo in Todos:
		todoList.append({"_id":str(todo["_id"]),"Title":todo["Title"],
				   "desc":todo["desc"],"created_at":todo["created_at"],
				   "updated_at":todo["updated_at"],"is_completed":todo["is_completed"]})

	return jsonify({"results":todoList})

#--------------------------ADD TODO---------------------------------------------------------
@app.route("/addTodo", methods=['POST'])
def addTodo():
	#Adding a Task
	Title = request.json["Title"]
	desc = request.json["desc"]
	created_at = datetime.datetime.now()#request.json["created_at"]
	

	try:
		todos.insert({ "Title":Title, "desc":desc, "created_at":created_at,"updated_at":"", "is_completed":False})
		return "Added a todo"
	except:
		return "Could not add todo"

#-------------------------UPDATE TODO-------------------------------------
@app.route("/updateTodo/<id>", methods=['PUT'])
def updateTodo(id):
	Title = request.json["Title"] ## son
	desc = request.json["desc"]
	updated_at = datetime.datetime.now()#request.json["updated_at"]
	is_completed = request.json["is_completed"]
	try:
		todos.update({"_id":ObjectId(id)}, {'$set':{ "Title":Title, "desc":desc,"updated_at":updated_at ,"is_completed":is_completed}})
		return "Updated todo"

	except:
		return "Update operation failed"

#------------------DELETE TODO------------------------------------------
@app.route("/deleteTodo",methods=["DELETE"])
def delete():
	key = request.json["_id"]
	try:
		todos.remove({"_id":ObjectId(key)})
		return "Deleted todo"
	except:
		return "Delete operation failed"

	#Deleting a Task with various references
	return jsonif({"id":key})

#-------------------------------------------------------------------------


@app.route("/list")
def lists():
	#Display the all Tasks
	todos_l = todos.find()
	a1 = "active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)


@app.route("/")
@app.route("/uncompleted")
def tasks():
	#Display the Uncompleted Tasks
	todos_l = todos.find({"is_completed":False})
	a2 = "active"
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/completed")
def completed():
	#Display the Completed Tasks
	todos_l = todos.find({"is_completed":True})
	a3 = "active"
	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/is_completed")
def done():
	#Done-or-not ICON
	id = request.values.get("_id")
	task = todos.find({"_id":ObjectId(id)})
	if(task[0]["is_completed"] == True):
		todos.update({"_id":ObjectId(id)}, {"$set": {"is_completed":False}})
	else:
		todos.update({"_id":ObjectId(id)}, {"$set": {"is_completed":True}})
	redir = redirect_url()	

	return redirect(redir)

@app.route("/action", methods=['POST'])
def action():
	#Adding a Task
	Title = request.values.get("Title")
	desc = request.values.get("desc")
	created_at = datetime.datetime.now()#request.values.get("created_at")
	#updated_at = ""#datetime.datetime.now()#request.values.get("updated_at")
	todos.insert({ "Title":Title, "desc":desc, "created_at":created_at, "is_completed":False})
	return redirect("/list")


@app.route("/remove")
def remove():
	#Deleting a Task with various references
	key = request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update():
	id = request.values.get("_id")
	task = todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)



@app.route("/action3", methods=['POST'])
def action3():
	#Updating a Task with various references
	Title = request.values.get("Title")
	desc = request.values.get("desc")
	#created_at = request.values.get("created_at")
	updated_at = datetime.datetime.now()#request.values.get("updated_at")
	id = request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "Title":Title, "desc":desc, "updated_at":updated_at }})
	return redirect("/")

@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key = request.values.get("key")
	refer = request.values.get("refer")
	if(key == "_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

if __name__ == "__main__":

    app.run()
