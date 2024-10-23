import math
from SaleApp import app, login
from flask import render_template, request, redirect, url_for
import utils
from flask_login import login_user
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

@app.route("/products")
def product_list():
    cate_id= request.args.get("category_id")
    kw= request.args.get("keyword")
    fromPrice= request.args.get("fromPrice")
    toPrice= request.args.get("toPrice")

    products = utils.load_products(cate_id=cate_id,
                                   kw=kw,
                                   fromPrice=fromPrice,
                                   toPrice=toPrice)

    return render_template("products.html", products=products )

@app.context_processor
def common_response():
    return {
        "categories": utils.load_categories()
    }

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product= utils.get_product_by_id(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/register', methods= ['get', 'post'])
def user_register():
    err_msg=''
    if request.method.__eq__('POST'):
        name= request.form.get('name')
        username= request.form.get('username')
        password = request.form.get('password')
        email= request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path= None
    try:
        if password.strip().__eq__(confirm.strip()):
            avatar= request.files.get('avatar')
            if avatar:
                res= cloudinary.uploader.upload(avatar)
                avatar_path=res['secure_url']
            utils.add_user(name=name, username=username, password=password, email=email, avatar=avatar_path)
            return redirect(url_for('user-signin'))
        else:
            err_msg= 'Mat khau khong khop'
    except Exception as ex:
        err_msg='He thong dang co loi!!! ' + str(ex)
    else:
        return redirect(url_for('home'))

    return render_template('register.html', err_msg=err_msg)

@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg=''
    if request.method.__eq__("POST"):
        username= request.form.get('username')
        password= request.form.get('password')

        user= utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect(url_for('home'))
        else:
            err_msg='Username hoac password khong chinh xac'
    return render_template('login.html', err_msg=err_msg)

@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)

if __name__ == "__main__":
    from SaleApp.admin import *
    app.run(debug=True)