from flask import Blueprint, render_template,request,jsonify,json,redirect,flash,url_for
from flask_login import login_required, current_user
from .models import Product, Order, ProductOrdered
from wtforms import Form, StringField, validators,FloatField,IntegerField,SelectField
from flask_wtf import FlaskForm
from pprint import PrettyPrinter 
from datetime  import  datetime as dt
orders=Blueprint('orders',__name__)
class OrderViews():
    def  __init__(self):
        self.current_product=Product()
        
    @orders.route("/order")
    def order(self):
            self.order=Order()
            
            return render_template("order.html",user=current_user,products=products)
    @orders.route("/saveproduct", methods=["POST"])
    def saveproduct(self):
        data=request.json
        prod_ord=ProductOrdered.objects(product=self.current_product,quant=data["quant"])
        neworder=Order(date=dt.now().strftime("%Y-%m-%d %H:%M:%S"))
        neworder.save()
    @orders.route("/saveorder", methods=["POST"])
    def saveorder():
        return render_template('orders.html',user=current_user,orders=Order.objects()) 
        
    @orders.route("/search", methods=["GET","POST"])
    def search():
        data=request.json
        try:
            if(data["id"]==""):    
                products=Product.objects(name__iregex=f'^.*{data['name']}.*$',lab__iregex=f'^.*{data['lab']}.*$')
            else:
                products=Product.objects(cb__iregex=f'^.*{data['id']}.*$')
            labs=products.distinct("lab")
            names=[product.name for product in products]
            ids=[product.cb for product in products]
            return jsonify(
                    {
                    'name':names,
                    'lab':labs,
                    'id':ids
                    })
        except Exception as err:
            return jsonify(error={"error":"No se encontro ningún producto"})

    @orders.route("/autocomplete",methods=["POST"])
    def autocomplete(self):
        print("ENTROOO")
        data = request.json
        str=jsonify({'error': "No se ha encontrado un producto, faltan mas campos por completar"})
        print(data)
        if data["id"]!="":
            products = Product.objects(cb=data["id"])
        else: 
            products = Product.objects(name=data["name"], lab=data["lab"])
        print(products)
        if (products.count())==1:
            product=products.first().to_json()
            self.current_product=product
            return product
        else:
            return str