from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from SaleApp import db
from datetime import datetime
from SaleApp import app
from enum import Enum as UserEnum
from flask_login import UserMixin

class BaseModel(db.Model):
    __abstract__ = True
    #bat khong tao bang
    id= Column(Integer, primary_key= True, autoincrement= True)
class UserRole(UserEnum):
    ADMIN = 1
    USER = 2

class User(BaseModel, UserMixin):
    name= Column(String(50), nullable=False)
    username= Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar= Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name

class Category(BaseModel):
    __tablename__ = 'category'
    name= Column(String(20), nullable=False)
    products= relationship('Product', backref='category', lazy=True)
    # backref: doi tuong trong Product se them 1 category
    # lazy: lay dung thong tin cua danh muc thoi

    def __str__(self):
        return self.name

class Product(BaseModel):
    __tablename__ ='product'
    name= Column(String(50), nullable= False)
    description = Column(String(255))
    price = Column(Float, default=0)
    image= Column(String(100))
    active= Column(Boolean, default=True)
    created_date= Column(DateTime, default=datetime.now())
    category_id= Column(Integer, ForeignKey(Category.id), nullable=False) # su dung ten lop doi tuong
    #category_id = Column(Integer, ForeignKey('category.id')) #su dung ten bang du lieu
    def __str__(self):
        return self.name

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # c1 = Category(name= 'Dien thoai')
        # c2= Category(name= 'May tinh bang')
        # c3= Category(name= 'Dong ho thong minh')
        #
        # db.session.add(c1)
        # db.session.add(c2)
        # db.session.add(c3)
        #
        # db.session.commit()

        # products= [{
        #   "id": 1,
        #   "name": "iPhone 7 Plus",
        #   "description": "Apple, 32GB, RAM: 3GB, iOS13",
        #   "price": 17000000,
        #   "image": "images/p1.png",
        #   "category_id": 1
        # }, {
        #   "id": 2,
        #   "name": "iPad Pro 2020",
        #   "description": "Apple, 128GB, RAM: 6GB",
        #   "price": 37000000,
        #   "image": "images/p2.png",
        #   "category_id": 2
        # }, {
        #   "id": 3,
        #   "name": "Galaxy Note 10 Plus",
        #   "description": "Samsung, 64GB, RAML: 6GB",
        #   "price": 24000000,
        #   "image": "images/p3.png",
        #   "category_id": 1
        # }]
        #
        # for p in products:
        #     pro = Product(name=p['name'], price= p['price'], image= p['image'],
        #                   description= p['description'], category_id= p['category_id'])
        #     db.session.add(pro)
        #
        # db.session.commit()