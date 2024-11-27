from SaleApp import app, db
from flask_admin import Admin, expose, AdminIndexView
from SaleApp.models import Category, Product, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user
from flask_admin import BaseView
from flask import redirect, request
import utils
from datetime import datetime

class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__('ADMIN')

class ProductView(ModelView):
    can_view_details = True
    can_export = True
    column_exclude_list = ['images']
    column_labels = {
        'name': 'Ten SP',
        'description': 'Mo ta',
        'price': 'Gia'
    }
    column_searchable_list = ['name', 'description']

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accesible(self):
        return current_user.is_authenticated

class StatsView(BaseView):
    @expose('/')

    def index(self):
        kw = request.args.get('kw')
        from_date= request.args.get('from_date')
        to_date= request.args.get('to_date')
        year= request.args.get('year', datetime.now().year)
        return self.render('admin/stats.html',month_stats= utils.product_month_stats(year=year),
                           stats= utils.product_stats(kw=kw,from_date=from_date,to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role== UserRole.ADMIN

class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats= utils.category_stats())

admin= Admin(app=app, name='E-commerce Administration', template_mode='bootstrap4', index_view= MyAdminIndex())

admin.add_view(AuthenticatedModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
admin.add_view(StatsView(name='Stats'))
admin.add_view(LogoutView(name='Logout'))
