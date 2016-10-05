import sys
sys.path.append('/opt/anaconda3/bin')
#####################################
from FlaskApp import app
from flask import Flask, render_template, Markup, redirect
from CommonMark import commonmark
from mongoengine import connect
from mongoengine import Document, StringField, DateTimeField, ListField

from FlaskApp.model import Post, Random
from FlaskApp.helpers import add_underscore, remove_underscore


db = connect('blog_posts') # connect to mongo

# Shold be able to do this better
static = "/var/www/FlaskApp/FlaskApp/static/"
posts_dir = static + "posts/"

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
