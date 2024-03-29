from mongoengine import *

class Leek(Document):
    leek_id = StringField(required=True, unique=True, primary_key=True)
    farmer_id = StringField()
    farmer_name = StringField()
    farmer_team = StringField()
    level = IntField()
    life = IntField()
    strength = IntField()
    agility = IntField()
    wisdom = IntField()
    frequency = IntField()
    action_point = IntField()
    movement_point = IntField()
    cores = IntField()
    weapons = ListField(IntField())
    chips = ListField(IntField())
    nb_victory = IntField()
    nb_defeat = IntField()
    nb_draw = IntField()
