from mongoengine import Document, StringField, DateTimeField, ListField

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
