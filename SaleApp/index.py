import math

from flask_login import login_user, logout_user

from SaleApp import app
from flask import render_template, request, redirect, url_for, session, jsonify
import utils
import cloudinary.uploader

@app.route("/")
def home():
    cate_id = request.args.get('category_id')
    kw= request.args.get('keyword')
    page= request.args.get('page', 1)
    counter =utils.count_products()

    products= utils.load_products(cate_id=cate_id, kw=kw, page=int(page))
    return render_template('index.html',
                           products=products, pages= math.ceil(counter/app.config['PAGE_SIZE']))

@app.context_processor
def common_response():
    return {
        "categories": utils.load_categories(),
        "cart_stats": utils.count_cart(session.get('cart'))
    }

@app.route("/register", methods=["get", "post"])
def user_register():
    err_msg=''
    if request.method.__eq__("POST"):
        name = request.form.get("name")
        username= request.form.get("username")
        email= request.form.get("email")
        password= request.form.get("password")
        confirm = request.form.get("confirm")
        avatar_path=None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path= res["secure_url"]
                utils.add_user(name=name, username=username, email=email, password=password, avatar=avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg="Mat khau khong khop"

        except Exception as ex:
            err_msg='He thong dang co loi: '+ str(ex)

    return render_template("register.html", err_msg=err_msg)

@app.route("/user-login", methods=["get", "post"])
def user_signin():
    err_msg=''
    if request.method.__eq__("POST"):
        username= request.form.get("username")
        password= request.form.get("password")

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg="Username hoac password khong chinh xac!!!"
    return render_template("login.html", err_msg=err_msg)

@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))

@app.route("/api/add-cart", methods=["post"])
def add_to_cart():

    data= request.json
    id= str(data.get('id'))
    name= data.get('name')
    price=data.get('price')



    cart= session.get('cart')
    if not cart:
        cart={}

    if id in cart:
        cart[id]['quantity']= cart[id]['quantity']+1
    else:
        cart[id]= {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart']=cart

    return jsonify(utils.count_cart(cart))

@app.route('/cart')
def cart():
    return render_template('cart.html', stats= utils.count_cart(session['cart']))

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product= utils.get_product_by_id(product_id)
    return render_template('product_detail.html', product=product)

if __name__ == "__main__":
    app.run(debug=True)