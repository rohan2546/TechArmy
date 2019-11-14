import pymongo
import datetime
import json
from flask import Flask, render_template, request, url_for, redirect, abort, jsonify, make_response
from flask_cors import CORS, cross_origin
from bson import json_util
from bson.json_util import dumps,ObjectId
import random

app=Flask(__name__)


@app.route('/addProblem',methods=['POST','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def addProblem():
	if request.method == 'POST':
		post= request.json
		client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
		db=client.hack_se
		posts = db.problem
		post_id = posts.insert_one(post)
		client.close()
		return "added"

@app.route('/addContest',methods = ['POST','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def addContest():
	if request.method == 'POST':
		post = request.json
		client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
		db=client.hack_se
		posts = db.contest
		posts1 = db.problem
		posts2 = db.user
		pid = post["problem_id"]
		em = post["user"] 
		if (posts1.find({"problem_id":pid}) is not None) and (posts2.find({"email":em}) is not None):
			post_id=posts.insert_one(post)
			return "added"
		else:
			return "not added"
			
		client.close()
	else:
		return jsonify({}),405

@app.route('/addUser',methods= ['POST','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def addUser():
	if request.method == 'POST':
		post=request.json
		em = post["email"]
		client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
		db=client.hack_se
		posts = db.user
		if posts.find({"email": em}) is None:		
			post_id = posts.insert_one(post)
			return "added"
		else:
			return "user exists"
		
		client.close()
		
	else:
		return jsonify({}),405
		
@app.route('/getProblemDescription',methods= ['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getProblemDescription():
		if request.method == 'GET':
			client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
			db=client.hack_se
			pid=request.args.get('problem_id',type=str)
			ab=db.problem.find_one({"problem_id":pid})
			ab1=json.loads(json_util.dumps(ab))
			return ab1,201
		else:
			return jsonify({}),405

@app.route('/getTestCases',methods= ['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getTestCases():
		if request.method == 'GET':
			client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
			db=client.hack_se
			pid=request.args.get('problem_id',type=str)
			ab=db.problem.find_one({"problem_id":pid})
			ab1 = json.loads(json_util.dumps(ab))
			cd=ab1["Test_case"]

			return cd,201
		else:
			return jsonify({}),405

@app.route('/getBestScore',methods= ['GET','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getBestScore():
		if request.method == 'GET':
			client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
			db=client.hack_se
			pid=request.args.get('Contest_id',type=str)
			sid=request.args.get('Student_id',type=str)
			ab=db.contest.find_one({"Contest_id":pid})
			ab1 = json.loads(json_util.dumps(ab))
			cd=ab1["Student_list"]
			for key,val in cd.items():
				if key==sid:
					return val["Best_score"]
		else:
			return jsonify({}),405

@app.route('/addBestCode',methods= ['PUT','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def addBestCode():
		if request.method == 'PUT':
			client = pymongo.MongoClient("mongodb+srv://rohansharma1606:_kwB&9Q4GTZg2fA@se-6kdpi.mongodb.net/test?retryWrites=true&w=majority")
			db=client.hack_se
			post=request.json
			cid=post["Contest_id"]
			sid=post["Student_id"]
			ns=post["Best_score"]
			bc=post["Best_code"]
			bcl=post["Best_code_language"]
			ab=db.contest.find_one({"Contest_id":cid})
			ab1 = json.loads(json_util.dumps(ab))
			cd=ab1["Student_list"]
			new_val={}
			n_val={}
			for key,val in cd.items():
				if key==sid and ns>val["Best_score"]:
					new_val={"Student_id":sid,"Best_code":bc,"Best_score":ns,"Best_code_language":bcl}
                    old_val=val
			dict={"$set":new_val}
			myco=db.contest["Student_list"]
			mycol=myco[sid]
			
			
			
			db=db.contest
			
		else:
			return jsonify({}),405

if __name__ == '__main__':
	app.run(debug=True)