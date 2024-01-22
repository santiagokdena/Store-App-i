from flask import Blueprint, render_template,request,jsonify,json,redirect,flash,url_for
from flask_login import login_required, current_user
from .models import Product, Order, ProductOrdered
from wtforms import Form, StringField, validators,FloatField,IntegerField,SelectField
from flask_wtf import FlaskForm
from pprint import PrettyPrinter 
from datetime  import  datetime as dt
orders=Blueprint('orders',__name__)
@orders.route("/order/<string:orderid>",methods=["GET"])
def order(orderid):
    if orderid=="0":
        order=Order()
        orderid=order.id
        return redirect(url_for('orders.order', orderid=orderid, user=current_user))
    else:
        order=Order.objects(id=orderid)
        print(order.to_json())
        # for product_list in order.products:
        #     # print(product_list.product["cb"],product_list.product["name"],product_list.product["lab"],product_list["quant"],product_list["quant"]*product_list.product["price"])
        #     print(product_list)
        
        return render_template("order.html",user=current_user,order=order)

@orders.route("/saveorder/<string:orderid>", methods=["POST"])
def saveorder(orderid):
    order=Order.objects(id=orderid)
    order.save()
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
def autocomplete():
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
        return product
    else:
        return str