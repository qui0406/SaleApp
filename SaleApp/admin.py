from SaleApp import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from SaleApp.models import Category, Product

admin= Admin(app=app, name="E-commerce Administration", template_mode='bootstrap4')

class ProductView(ModelView):
    can_view_details = True
    can_export = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
   # column_exclude_list = ['image', 'active', 'Created-date']
    column_labels = {
        'name': 'Ten san pham',
        'description': 'Mo ta',
        'price': 'Gia ban',
        'image': 'Anh dai dien',
        'category': 'Danh muc'
    }
    column_sortable_list = ['id', 'name', 'price']
admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))
