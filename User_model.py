from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import *
from sqlalchemy import func
from sqlalchemy import *
db = SQLAlchemy()


class Users(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_name = db.Column(db.String(50), nullable=False, unique=True)
    user_password = db.Column(db.String(40), nullable=False)
    user_wallet = db.Column(db.Integer(), nullable=False)

    __table_args__ = (
        db.UniqueConstraint('user_name', 'user_password',
                            name='uq_user_username_password'),
    )

    Users_in_carts = db.relationship(
        'Cart', backref='cart_user')

    def __repr__(self):
        return f"( id : {self.user_id}, name : {self.user_name} )"


class Cart(db.Model):
    """
            user --- one to many --- Cart  # a cart can be created by only one user  
            product -- one to many --- Cart # every cart row has only one product   
    """
    cart_id = db.Column(db.Integer(), primary_key=True)
    cart_user_id = db.Column(db.Integer(), db.ForeignKey(
        'users.user_id'), nullable=False)
    product_id = db.Column(db.Integer(),
                           db.ForeignKey('product.product_id'), nullable=True)  # fk for product
    # no of packs of that product
    no_of_items = db.Column(db.String(50), nullable=False) 

    def __repr__(self):
        return f"( id : {self.product_id}, no of items : {self.no_of_items})"


class Admin(db.Model):
    admin_id = db.Column(db.Integer(), primary_key=True, unique=True)
    admin_username = db.Column(db.String(50), nullable=False, unique=True)
    admin_password = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"(name : {self.admin_username}  password : {self.admin_password} )"


class Category(db.Model):
    category_id = db.Column(db.Integer(), primary_key=True, unique=True)
    category_name = db.Column(db.String(50),  nullable=False)
    img_file = db.Column(
        db.String(100),  nullable=False, default='default_category.jpg')
    
    category_product_list = db.relationship(
        'Product', backref='product_category')

    def __repr__(self):
        return f"(category name : {self.category_name} , category id : {self.category_id} )"




class Product(db.Model):
    product_id = db.Column(db.Integer(), primary_key=True,
                           unique=True, nullable=False)
    product_name = db.Column(
        db.String(60), nullable=False)  # like basmati rice
    img_file = db.Column(
        db.String(100),  nullable=False, default='default_product.jpg')
    # it is good in protein and fiber
    product_desc = db.Column(db.Text(), nullable=False)
    product_stock = db.Column(
        db.Integer(), nullable=False)  # 10 ~ pack available
    product_mfg = db.Column(db.Date(), nullable=False)  # 2023-5-24
    product_exp = db.Column(db.Date(), nullable=False)  # 2023-5-30
    product_price = db.Column(
        db.Integer(), nullable=False)  # 100 ~ 100Rs per pack
    # 1000 gm per kg or 1ltr some thing like that
    product_pack_details = db.Column(db.String(20), nullable=False)
    product_category_id = db.Column(
        db.Integer(), db.ForeignKey('category.category_id'), nullable=True, unique=False )   
    
    product_cart = db.relationship(                        
        'Cart', backref='cart_product')

    def __repr__(self):
        return f"(Product name : {self.product_name} , category id : {self.product_category_id} , price : {self.product_price})"
    # foreign key to the product to the section or catorgy



class Sold_Product(db.Model):
    product_id = db.Column(db.Integer(), primary_key=True, 
                           unique=True, nullable=False)
    product_name = db.Column(
        db.String(60), nullable=False)  # like basmati rice

    sold_date = db.Column(db.Date(), nullable=False)  # 2023-5-24
    sold_items = db.Column(db.String(50), nullable=False)
    product_price = db.Column(
        db.Integer(), nullable=False)  # 100 ~ 100Rs per pack
    product_category = db.Column(db.String(50), nullable=True, unique=False)

    def __repr__(self):
        return f"(Product name : {self.product_name} , category id : {self.product_category} , price : {self.product_price})"
    # foreign key to the product to the section or catorgy