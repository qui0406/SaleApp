import json, os
from SaleApp import app, db
from SaleApp.models import Category, Product, User
import hashlib

def read_json(path):
    # f= open(path, "r")
    # data= json.load(f)
    # f.close()
    # return data

    with open(path, "r") as f:
        return json.load(f)

def load_categories():
    return Category.query.all()
    #return read_json(os.path.join(app.root_path, 'data/categories.json'))

def load_products(cate_id=None, kw=None, fromPrice=None, toPrice=None, page =1):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))
    if kw:
        products = products.filter(Product.name.contains(kw))
    if fromPrice:
        products = products.filter(Product.price.__ge__(fromPrice))
    if toPrice:
        products = products.filter(Product.price.__le__(toPrice))
    page_size = app.config['PAGE_SIZE']
    start= (page -1)*page_size
    end = start + page_size

    return products.slice(start, end).all()
    # products= read_json(os.path.join(app.root_path, 'data/products.json'))
    #
    # if cate_id:
    #     products = [p for p in products if p["category_id"]==int(cate_id)]
    #
    # if kw:
    #     products = [p for p in products if p["name"].lower().find(kw.lower())>=0]
    #
    # if fromPrice:
    #     products = [p for p in products if p["price"]>= float(fromPrice)]
    #
    # if toPrice:
    #     products = [p for p in products if p["price"] <= float(fromPrice)]
    # return products

def get_product_by_id(product_id):
    return Product.query.get(product_id)
    # products= read_json(os.path.join(app.root_path, 'data/products.json'))
    #
    # for p in products:
    #     if p['id']==product_id:
    #         return p

def count_products():
    return Product.query.filter(Product.active.__eq__(True)).count()

def add_user(name, username, password, **kwargs):
    password= str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
    user = User(name=name, username= username,
                password=password, email=kwargs.get('email'),
                avatar= kwargs.get("avatar"))
    db.session.add(user)
    db.session.commit()

def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def count_cart(cart):
    total_quantity, total_amount =0, 0

    if cart:
        for c in cart.values():
            total_quantity+= c['quantity']
            total_amount+= c['quantity']* c['price']

    return{
        'total_quantity': total_quantity,
        'total_amount': total_amount

    }