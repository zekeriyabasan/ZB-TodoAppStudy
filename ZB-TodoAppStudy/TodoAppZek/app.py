from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
from flask_pymongo import PyMongo
import json
import os

from bson.objectid import ObjectId
from flask import jsonify, request

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/todo"
mongo = PyMongo(app)

title = "TODO sample application with Flask and MongoDB"
heading = "TODO Reminder with Flask and MongoDB"

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
		todoList.append({"_id":str(todo["_id"]),"name":todo["name"],
				   "desc":todo["desc"],"created_at":todo["created_at"],
				   "updated_at":todo["updated_at"],"done":todo["done"]})

	return jsonify({"results":todoList})

#--------------------------ADD TODO---------------------------------------------------------
@app.route("/addTodo", methods=['POST'])
def addTodo():
	#Adding a Task
	name = request.json["name"]
	desc = request.json["desc"]
	created_at = request.json["created_at"]
	

	try:
		todos.insert({ "name":name, "desc":desc, "created_at":created_at,"updated_at":"", "done":"no"})
		return "Added a todo"
	except:
		return "Could not add todo"

#-------------------------UPDATE TODO-------------------------------------
@app.route("/updateTodo/<id>", methods=['PUT'])
def updateTodo(id):
	name = request.json["name"] ## son
	desc = request.json["desc"]
	updated_at = request.json["updated_at"]
	try:
		todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc,"updated_at":updated_at }})
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
	todos_l = todos.find({"done":"no"})
	a2 = "active"
	return render_template('index.html',a2=a2,todos=todos_l,t=title,h=heading)


@app.route("/completed")
def completed():
	#Display the Completed Tasks
	todos_l = todos.find({"done":"yes"})
	a3 = "active"
	return render_template('index.html',a3=a3,todos=todos_l,t=title,h=heading)

@app.route("/done")
def done():
	#Done-or-not ICON
	id = request.values.get("_id")
	task = todos.find({"_id":ObjectId(id)})
	if(task[0]["done"] == "yes"):
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
	else:
		todos.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
	redir = redirect_url()	

	return redirect(redir)

@app.route("/action", methods=['POST'])
def action():
	#Adding a Task
	name = request.values.get("name")
	desc = request.values.get("desc")
	created_at = request.values.get("created_at")
	updated_at = request.values.get("updated_at")
	todos.insert({ "name":name, "desc":desc, "created_at":created_at, "updated_at":updated_at, "done":"no"})
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
	name = request.values.get("name")
	desc = request.values.get("desc")
	created_at = request.values.get("created_at")
	updated_at = request.values.get("updated_at")
	id = request.values.get("_id")
	todos.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "desc":desc, "created_at":created_at, "updated_at":updated_at }})
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
