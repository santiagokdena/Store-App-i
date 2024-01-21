from models import Product 
from flask_mongoengine import MongoEngine


def get_all_products(string):
    
    pipeline_name=[
        {
            
        "$search":{
        "index":"product_search",
        "autocomplete":{
            "query":string,
            "path":"name",
            "tokenOrder":"sequential",
            "fuzzy":{}
        }
        }
        },
        {
        '$project':{
            'name':1,'_id':0}
        }]
    response=Product.objects().aggregate(pipeline_name)
    response=list(response)
    print(response)    
    
get_all_products('G')