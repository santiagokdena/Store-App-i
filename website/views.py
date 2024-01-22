from flask import Blueprint, render_template,request,jsonify,json,redirect,flash,url_for
from flask_login import login_required, current_user
from .models import Product, Order,  ProductOrdered
from wtforms import Form, StringField, validators,FloatField,IntegerField,SelectField
from flask_wtf import FlaskForm
from pprint import PrettyPrinter 
from datetime  import  datetime as dt
import mongoengine as me
views=Blueprint('views',__name__)
class ProductRegistrationForm(Form):
    labs=['technoquimicas', 'MK', 'BAYER']
    cb=StringField("Codigo de barras",validators=[validators.InputRequired()])
    name=StringField("Nombre",validators=[validators.InputRequired()])
    # lab=StringField("Laboratorio",validators=[validators.InputRequired()])
    lab=SelectField("Laboratorio",choices=labs)
    price=IntegerField("Precio",validators=[validators.InputRequired()])
    util=IntegerField("Utilidad(%)",validators=[validators.InputRequired()])
    quant=IntegerField("Cantidad",validators=[validators.InputRequired()])
    form=StringField("Forma farmacéutica",validators=[validators.InputRequired()])
    conc=StringField("Concentración",validators=[validators.InputRequired()])
    



@views.route("/deleteregister/<string:getid>",methods=["POST"])
def delete_register(id):
    product=Product.objects(cb=id)
    product.quant+=1
    if product.count()==1:
        return render_template('orders.html',user=current_user)
    else:
        print("error")
        return jsonify(
            {'error':"No se encontro ningun producto con los valores de los campos proporcionados"}                
        )
@views.route('/orders',methods=['GET','POST']) 
@login_required
def orders():
    #si hay un POST, entonces que esta funcion  sepa. Poner un if(request==GET)
    
    orders=Order.objects
    return render_template("orders.html",user=current_user,orders=orders)


@views.route('/inventory',methods=['GET','POST'])
@login_required
def inventory():
    form=ProductRegistrationForm(request.form)
    product=Product.objects(cb=form.cb.data).first()
    products= Product.objects.fields()
    print(products)

    if request.method=="POST":
        print("enviado")
    if request.method=="POST" and form.validate():
        if not product:
            productsave=Product(name=form.name.data,lab=form.lab.data,price=form.price.data,util=form.util.data,cb=form.cb.data,quant=form.quant.data,conc=form.conc.data,form=form.form.data)
            productsave.save()
            return redirect(url_for('views.inventory',user=current_user, products=products,form=form))
        else:
            form.cb.errors.append("Este producto ya esta en el inventario")
            return render_template("inventory.html",user=current_user, products=products,form=form)
    return render_template("inventory.html",user=current_user, products=products,form=form)
@views.route('/statistics',methods=['GET','POST'])
@login_required
def statistics():
    return render_template("statistics.html",user=current_user)
@views.route('/missing',methods=['GET','POST'])
@login_required
def missing():
    return render_template("missing.html",user=current_user)
@views.route('/inventory/updateproduct', methods=['POST'])
def updateproduct():
    pk = request.form['pk']
    namepost = request.form['name']
    value = request.form['value']
    product_rs = Product.objects(id=pk).first()
    if not product_rs:
        return json.dumps({'error':'data not found'})
    else:
        if namepost == 'id':
            product_rs.update(cb=value)
        elif namepost == 'name':
            product_rs.update(name=value)
        elif namepost == 'lab':
            if value in ProductRegistrationForm.labs:
                product_rs.update(lab=value)
        elif namepost == 'quant':
            product_rs.update(quant=value)
        elif namepost == 'price':
            product_rs.update(price=value)
        elif namepost == 'util':
            product_rs.update(util=value)
    return json.dumps({'status':'OK'})
@views.route('/delete/<string:getid>',methods=['POST','GET'])
def delete_product(getid):
    form=ProductRegistrationForm(request.form)
    product = Product.objects(cb=getid).first()
    products=Product.objects.all()
    if not product:
        return jsonify({'error': 'data not found'})
    else:
        product.delete() 
    return render_template('inventory.html',user=current_user, products=products,form=form)


