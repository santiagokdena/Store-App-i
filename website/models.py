from .__init__ import db
from flask_login import UserMixin
from bson.objectid import ObjectId
import mongoengine as me
    
class Product(db.Document):
    name=db.StringField(required=True)
    lab=db.StringField(required=True)
    price=db.FloatField(required=True,min_value=0) 
    cb=db.StringField(required=True,unique=True,pimary_key=True) 
    #details
    util=db.FloatField(required=True,min_value=0) 
    form=db.StringField(required=True)
    conc=db.StringField(required=True) 
    quant=db.IntField(required=True) 
class User(db.Document,UserMixin):
    # user_id= ObjectIdField(required=True, default=ObjectId, unique=True, primary_key=True)
    # meta = {'db': 'DRUGSTORE','collection': 'user'}
    user=db.StringField(unique=True)
    password=db.StringField()
#extended reference pattern
class ProductOrdered(me.EmbeddedDocument):
    quant=me.IntField(required=True) 
    product=me.ReferenceField('Product',fields={'name': 1, 'lab': 1, 'price': 1, 'cb': 1}, required=True)
    #referencias uniamente los campos basicos, no detalles.    .
    
#embedded pattern
class Order(db.Document):
    id=db.SequenceField(primary_key=True)
    date=db.DateTimeField()
    products=db.ListField(me.EmbeddedDocumentField(ProductOrdered))
    

    
