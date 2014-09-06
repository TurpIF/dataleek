from mongoengine import *
import datetime

class LeekCrawl(Document):
    leek_id = StringField(required=True, unique=True, primary_key=True)
    crawl = StringField()
    last_updated = DateTimeField(default=datetime.datetime.now)
