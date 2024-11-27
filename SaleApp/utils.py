import json, os
from sqlalchemy.sql import extract
from sqlalchemy import func

from SaleApp import app, db
from SaleApp.models import Category, Product, User, Receipt, ReceiptDetails, UserRole
import hashlib
from flask_login import current_user

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
    user = User(name= name, username= username,
                password= password, email= kwargs.get('email'),
                avatar= kwargs.get("avatar"))
    db.session.add(user)
    db.session.commit()

def check_login(username, password, role=UserRole.USER):
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

def add_receipt(cart):
    if cart:
        r = Receipt(user=current_user)
        db.session.add(r)

        for c in cart.values():
            d = ReceiptDetails(quantity=c['quantity'], unit_price=c['price'],
                               receipt=r, product_id=c['id'])
            db.session.add(d)

        db.session.commit()

def category_stats():
    # return Category.query.join(Product, Product.category_id.__eq__(Category.id), isouter= True)\
    #         .add_columns(func.count(Product.id)).group_by(Category.id, Category.name).all()
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Category.id.__eq__(Product.category_id), isouter= True)\
        .group_by(Category.id, Category.name).all()

def product_stats(kw=None, from_date=None, to_date=None):
    p = db.session.query(Product.id, Product.name,
                         func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price))\
                    .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id), isouter= True)\
                    .join(Receipt, Receipt.id.__eq__(ReceiptDetails.receipt_id))\
                    .group_by(Product.id, Product.name)
    if kw:
        p= p.filter(Product.name.contains(kw))
    if from_date:
        p= p.filter(Receipt.created_date.__ge__(from_date))
    if to_date:
        p= p.filter(Receipt.created_date.__le__(to_date))


    return p.all()

def product_month_stats(year):
    return (db.session.query(extract('month', Receipt.created_date),
                            func.sum(ReceiptDetails.quantity * ReceiptDetails.unit_price))\
                .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id))\
                .filter(extract('year', Receipt.created_date)== year)\
                .group_by(extract('month', Receipt.created_date))\
                .order_by(extract('month', Receipt.created_date))\
                .all())