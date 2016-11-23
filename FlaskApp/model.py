from mongoengine import Document, StringField, DateTimeField, ListField, IntField, FloatField

class Post(Document):
    title = StringField()
    content = StringField()
    description = StringField()
    date = DateTimeField()
    js_resorces = ListField(StringField())

class Random(Document):
    description = StringField()
    tag = StringField()

class SpotifyAuth(Document):
    username = StringField()
    access_token = StringField()
    refresh_token = StringField()

class MonzoTrans(Document):
    amount = FloatField()
    time = DateTimeField()
    category = StringField()
    name = StringField()
