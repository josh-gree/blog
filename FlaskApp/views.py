import sys
sys.path.append('/opt/anaconda3/bin')
#####################################
import pickle
import pandas as pd

from FlaskApp import app
from flask import Flask, render_template, Markup, redirect, request, jsonify
from flask_restful import reqparse, abort, Api, Resource

from CommonMark import commonmark
from mongoengine import connect
from mongoengine import Document, StringField, DateTimeField, ListField
from pymongo import MongoClient
transactions = MongoClient().blog_posts.monzo_trans

from FlaskApp.model import Post, Random, MonzoTrans
from FlaskApp.helpers import add_underscore, remove_underscore

from datetime import datetime
from bson import json_util
import json

db = connect('blog_posts') # connect to mongo
client = MongoClient()
    
# Shold be able to do this better
static = "/var/www/FlaskApp/FlaskApp/static/"
posts_dir = static + "posts/"
templates = "/var/www/FlaskApp/FlaskApp/templates/"

api = Api(app)
def pipeline_agg(group,opp):
    return [{"$group": {"_id": "${}".format(group), "count": {"${}".format(opp): "$amount"}}}]

def pipeline_match(group,name):
    return [{"$match":{'{}'.format(group):'{}'.format(name)}}]

class allTrans(Resource):
    def get(self):
        data = []
        for trans in transactions.find():
            data.append(trans)
        return json.loads(json_util.dumps(data))

class grouptrans(Resource):
    def get(self, group, opp):
        return list(transactions.aggregate(pipeline=pipeline_agg(group,opp)))

class nametrans(Resource):
    def get(self, group, name):
        return json.loads(json_util.dumps(list(transactions.aggregate(pipeline=pipeline_match(group,name)))))

api.add_resource(allTrans, '/trans')
api.add_resource(grouptrans, '/trans/<group>/<opp>')
api.add_resource(nametrans, '/trans/named/<group>/<name>')
# index page will show most recent blogpost
@app.route("/")
def index():
    # Better way to select newest post?
    posts = [p for p in Post.objects]
    posts = list(reversed(sorted(posts,key = lambda x : x.date)))
    title = posts[0].title
    title = add_underscore(title)
    text = open(posts_dir + title + "/" + title + '.md').read()
    return render_template("blog_post.html",
                            content = commonmark(text),
                            title=remove_underscore(title),
                            jss=posts[0].js_resorces)

@app.route("/who_am_i")
def who_am_i():
    text = open(static + "who_am_i.md").read()
    return render_template("who_am_i.html",content = commonmark(text))

@app.route("/blog_posts/")
def blog_posts():
    posts = [p for p in Post.objects]
    titles = [add_underscore(p.title) for p in posts]
    description = [open(posts_dir + t + "/" + t + '.desc').read() for t in titles]
    posts = zip(posts,description)
    posts = reversed(sorted(posts,key = lambda x : x[0].date))

    return render_template("blog_posts.html",title="My Blog Posts",posts = posts)

@app.route('/colombia/')
def colombia():
    text = open(posts_dir + 'colombia.md').read()
    return render_template("colombia.html",content=commonmark(text))

@app.route('/blog_posts/<title>/')
def blog_post_(title):
    post = Post.objects(title = remove_underscore(title))[0]
    text = open(posts_dir + title + "/" + title + '.md').read()

    return render_template("blog_post.html",content = commonmark(text),title = post.title, jss = post.js_resorces)

@app.route("/random")
def random():
    rands = Random.objects()
    rands = reversed(rands)

    return render_template("randoms.html",title="Nothing to see here!",rands=rands)

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/monzo_webhook", methods=['GET','POST'])
def monzo_webhook():
    content = request.json
    amount = content['data']['amount']
    category = content['data']['category']
    time = content['data']['created'] # need to convert  to datetime
    time = datetime.strptime(time.split('.')[0],"%Y-%m-%dT%H:%M:%S")
    try:
        name = content['data']['merchant']['name']
    except Exception:
        name = None
    try:
        content['data']['decline_reason']
    except Exception:
        if (amount < 0) or (name != 'ATM'):
            MonzoTrans(category = category,amount=abs(amount)/100.0,time=time,name=name).save()

    return "Nothing to see..."

@app.route('/office_notebook')
def office_notebook():
    return redirect('http://9c7237d0.ngrok.io/')

@app.route('/stream/cats.json')
def stream_cats():
    
    #return 'Hello'
    db = client.blog_posts
    df = pd.DataFrame(list(db.monzo_trans.find()))[['amount','category','name','time']]
    
    return df.to_json(orient='records')
